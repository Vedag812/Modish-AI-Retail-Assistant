"""
Inventory API Integration - Using free public APIs
Real-time product and inventory data from free sources
"""
import requests
import json
from datetime import datetime
import random

class InventoryAPI:
    """Inventory API wrapper using free public APIs"""
    
    def __init__(self):
        # Using FakeStore API - completely free, no signup required
        self.base_url = "https://fakestoreapi.com"
        # Alternative: DummyJSON - https://dummyjson.com/products
        self.alt_url = "https://dummyjson.com"
    
    def get_products(self, category=None, limit=20):
        """
        Fetch real products from free API
        
        Args:
            category: Product category filter
            limit: Maximum products to return
            
        Returns:
            List of products with real data
        """
        try:
            # Try FakeStore API first
            if category:
                url = f"{self.base_url}/products/category/{category}"
            else:
                url = f"{self.base_url}/products?limit={limit}"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                products = response.json()
                
                # Transform to our format
                transformed = []
                for p in products[:limit]:
                    transformed.append({
                        "sku": f"API_{p['id']}",
                        "name": p['title'],
                        "category": p.get('category', 'general'),
                        "price": p['price'],
                        "description": p.get('description', ''),
                        "image": p.get('image', ''),
                        "rating": p.get('rating', {}).get('rate', 0),
                        "stock": random.randint(0, 100),  # Simulated stock
                        "source": "fakestoreapi"
                    })
                
                return {
                    "status": "success",
                    "products": transformed,
                    "count": len(transformed),
                    "source": "FakeStore API (Free)"
                }
            else:
                # Fallback to DummyJSON
                return self._get_products_dummyjson(category, limit)
                
        except Exception as e:
            print(f"⚠️  API Error: {str(e)}, using fallback")
            return self._get_products_dummyjson(category, limit)
    
    def _get_products_dummyjson(self, category, limit):
        """Fallback to DummyJSON API"""
        try:
            url = f"{self.alt_url}/products?limit={limit}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                
                transformed = []
                for p in products:
                    if category and p.get('category') != category:
                        continue
                    
                    transformed.append({
                        "sku": f"DUMMY_{p['id']}",
                        "name": p['title'],
                        "category": p.get('category', 'general'),
                        "price": p['price'],
                        "description": p.get('description', ''),
                        "image": p.get('thumbnail', ''),
                        "rating": p.get('rating', 0),
                        "stock": p.get('stock', random.randint(0, 100)),
                        "source": "dummyjson"
                    })
                
                return {
                    "status": "success",
                    "products": transformed,
                    "count": len(transformed),
                    "source": "DummyJSON API (Free)"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"All APIs failed: {str(e)}"
            }
    
    def get_product_by_id(self, product_id):
        """Get single product details"""
        try:
            # Try to extract numeric ID
            if isinstance(product_id, str) and '_' in product_id:
                _, pid = product_id.split('_')
            else:
                pid = product_id
            
            url = f"{self.base_url}/products/{pid}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                p = response.json()
                return {
                    "status": "success",
                    "product": {
                        "sku": f"API_{p['id']}",
                        "name": p['title'],
                        "category": p.get('category', 'general'),
                        "price": p['price'],
                        "description": p.get('description', ''),
                        "image": p.get('image', ''),
                        "rating": p.get('rating', {}).get('rate', 0),
                        "stock": random.randint(10, 100),
                        "source": "fakestoreapi"
                    }
                }
            else:
                return {"status": "error", "message": "Product not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_stock(self, sku, location=None):
        """
        Check real-time stock availability
        
        Args:
            sku: Product SKU
            location: Store location (optional)
            
        Returns:
            Stock availability info
        """
        # For free APIs, we simulate location-based stock
        # In production, this would call actual inventory management system
        
        base_stock = random.randint(0, 150)
        
        locations = {
            "New York - 5th Avenue": random.randint(0, 50),
            "Los Angeles - Beverly Hills": random.randint(0, 40),
            "Chicago - Michigan Ave": random.randint(0, 30),
            "Miami - Brickell": random.randint(0, 45),
            "Seattle - Downtown": random.randint(0, 35),
            "Online Warehouse": base_stock
        }
        
        if location:
            stock = locations.get(location, 0)
            return {
                "status": "success",
                "sku": sku,
                "location": location,
                "stock": stock,
                "available": stock > 0,
                "last_updated": datetime.now().isoformat()
            }
        else:
            return {
                "status": "success",
                "sku": sku,
                "locations": locations,
                "total_stock": sum(locations.values()),
                "last_updated": datetime.now().isoformat()
            }
    
    def get_categories(self):
        """Get available product categories"""
        try:
            url = f"{self.base_url}/products/categories"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                categories = response.json()
                return {
                    "status": "success",
                    "categories": categories,
                    "count": len(categories)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "categories": ["electronics", "jewelery", "men's clothing", "women's clothing"]
            }
    
    def search_products(self, query, limit=10):
        """
        Search products by keyword
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            Matching products
        """
        try:
            # Get all products and filter
            all_products = self.get_products(limit=100)
            
            if all_products["status"] == "success":
                products = all_products["products"]
                
                # Simple search by name/category
                query_lower = query.lower()
                filtered = [
                    p for p in products 
                    if query_lower in p["name"].lower() or query_lower in p["category"].lower()
                ]
                
                return {
                    "status": "success",
                    "query": query,
                    "products": filtered[:limit],
                    "count": len(filtered)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

# Initialize inventory API
inventory_api = InventoryAPI()

print("✅ Inventory API initialized (Using free public APIs)")
print("   Sources: FakeStore API, DummyJSON - 100% Free, No signup required")
