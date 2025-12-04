"""
PostgreSQL Database Integration
Real-time database using PostgreSQL (Free & Open Source)
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import json

class PostgreSQLDB:
    """PostgreSQL database wrapper for retail sales system"""
    
    def __init__(self, connection_string=None):
        """
        Initialize PostgreSQL connection
        
        Args:
            connection_string: PostgreSQL connection string
                Format: postgresql://user:password@host:port/database
                
        For local PostgreSQL:
            postgresql://postgres:password@localhost:5432/retail_sales
            
        For free cloud PostgreSQL (ElephantSQL, Supabase, etc.):
            Use the connection string from your provider
        """
        self.connection_string = connection_string or os.getenv('DATABASE_URL') or os.getenv('POSTGRESQL_URL')
        
        if not self.connection_string:
            # Default to local PostgreSQL
            self.connection_string = "postgresql://postgres:postgres@localhost:5432/retail_sales"
            print("⚠️  Using default local PostgreSQL connection")
            print("   To use cloud database, set POSTGRESQL_URL in .env")
        
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.connection_string)
            self.conn.autocommit = True
            print(f"✅ Connected to PostgreSQL database")
            return True
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            print("\n💡 Free PostgreSQL Options:")
            print("   1. LOCAL: Install PostgreSQL locally (100% free)")
            print("      Download: https://www.postgresql.org/download/")
            print("   2. CLOUD: Use free tier from:")
            print("      - ElephantSQL: https://www.elephantsql.com/ (Free tier: 20MB)")
            print("      - Supabase: https://supabase.com/ (Free tier: 500MB)")
            print("      - Neon: https://neon.tech/ (Free tier: 3GB)")
            return False
    
    def create_tables(self):
        """Create all necessary tables"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Customers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    loyalty_tier VARCHAR(20) DEFAULT 'bronze',
                    loyalty_points INTEGER DEFAULT 0,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    sku VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    category VARCHAR(50),
                    description TEXT,
                    current_price DECIMAL(10, 2),
                    original_price DECIMAL(10, 2),
                    rating DECIMAL(3, 2),
                    reviews_count INTEGER DEFAULT 0,
                    image_url VARCHAR(500),
                    source VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Inventory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id SERIAL PRIMARY KEY,
                    sku VARCHAR(20) REFERENCES products(sku),
                    location VARCHAR(100),
                    quantity INTEGER DEFAULT 0,
                    reserved INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(sku, location)
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id VARCHAR(20) PRIMARY KEY,
                    customer_id VARCHAR(20) REFERENCES customers(customer_id),
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'pending',
                    total_amount DECIMAL(10, 2),
                    payment_method VARCHAR(50),
                    payment_status VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Order items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id SERIAL PRIMARY KEY,
                    order_id VARCHAR(20) REFERENCES orders(order_id),
                    sku VARCHAR(20) REFERENCES products(sku),
                    quantity INTEGER,
                    price DECIMAL(10, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Transactions table (for payments)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id VARCHAR(50) PRIMARY KEY,
                    order_id VARCHAR(20) REFERENCES orders(order_id),
                    customer_id VARCHAR(20) REFERENCES customers(customer_id),
                    amount DECIMAL(10, 2),
                    payment_method VARCHAR(50),
                    status VARCHAR(20),
                    provider VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Reviews table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id SERIAL PRIMARY KEY,
                    sku VARCHAR(20) REFERENCES products(sku),
                    customer_id VARCHAR(20) REFERENCES customers(customer_id),
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.close()
            print("✅ PostgreSQL tables created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def insert_customer(self, customer_data):
        """Insert or update customer"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO customers (customer_id, name, email, phone, loyalty_tier, loyalty_points)
                VALUES (%(customer_id)s, %(name)s, %(email)s, %(phone)s, %(loyalty_tier)s, %(loyalty_points)s)
                ON CONFLICT (customer_id) 
                DO UPDATE SET 
                    loyalty_tier = EXCLUDED.loyalty_tier,
                    loyalty_points = EXCLUDED.loyalty_points
                RETURNING customer_id
            """, customer_data)
            
            result = cursor.fetchone()
            cursor.close()
            return {"status": "success", "customer_id": result[0]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def insert_product(self, product_data):
        """Insert or update product"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO products (sku, name, category, description, current_price, 
                                     original_price, rating, reviews_count, image_url, source)
                VALUES (%(sku)s, %(name)s, %(category)s, %(description)s, %(price)s,
                       %(price)s, %(rating)s, 0, %(image)s, %(source)s)
                ON CONFLICT (sku)
                DO UPDATE SET
                    current_price = EXCLUDED.current_price,
                    rating = EXCLUDED.rating,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING sku
            """, product_data)
            
            result = cursor.fetchone()
            cursor.close()
            return {"status": "success", "sku": result[0]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_inventory(self, sku, location, quantity):
        """Update inventory for a product at a location"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (sku, location, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (sku, location)
                DO UPDATE SET
                    quantity = EXCLUDED.quantity,
                    last_updated = CURRENT_TIMESTAMP
                RETURNING id
            """, (sku, location, quantity))
            
            result = cursor.fetchone()
            cursor.close()
            return {"status": "success", "id": result[0]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_inventory(self, sku, location=None):
        """Get inventory for a product"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            if location:
                cursor.execute("""
                    SELECT * FROM inventory 
                    WHERE sku = %s AND location = %s
                """, (sku, location))
                result = cursor.fetchone()
            else:
                cursor.execute("""
                    SELECT * FROM inventory 
                    WHERE sku = %s
                """, (sku,))
                result = cursor.fetchall()
            
            cursor.close()
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_order(self, order_data):
        """Create a new order"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO orders (order_id, customer_id, status, total_amount, 
                                  payment_method, payment_status)
                VALUES (%(order_id)s, %(customer_id)s, %(status)s, %(total_amount)s,
                       %(payment_method)s, %(payment_status)s)
                RETURNING order_id
            """, order_data)
            
            result = cursor.fetchone()
            cursor.close()
            return {"status": "success", "order_id": result[0]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_customer(self, customer_id):
        """Get customer details"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM customers WHERE customer_id = %s
            """, (customer_id,))
            
            result = cursor.fetchone()
            cursor.close()
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_products(self, query, limit=20):
        """Search products by name or category"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM products
                WHERE name ILIKE %s OR category ILIKE %s
                ORDER BY rating DESC
                LIMIT %s
            """, (f"%{query}%", f"%{query}%", limit))
            
            results = cursor.fetchall()
            cursor.close()
            return {"status": "success", "data": results, "count": len(results)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ PostgreSQL connection closed")

# Global database instance
db = None

def init_postgresql():
    """Initialize PostgreSQL database"""
    global db
    db = PostgreSQLDB()
    
    if db.conn:
        db.create_tables()
        return db
    return None

print("✅ PostgreSQL module loaded")
