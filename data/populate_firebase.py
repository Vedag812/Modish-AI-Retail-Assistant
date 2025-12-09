"""
Populate Firebase Firestore with 1200+ Indian products
Balanced across 12 categories (100+ products each)

Usage: python data/populate_firebase.py
"""
import random
import sys
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 12 Categories - Each will have 100+ products
CATEGORIES = {
    "Electronics": {
        "price_range": (2999, 79999),
        "products": [
            "Smart LED TV 32 inch", "Smart LED TV 43 inch", "Smart LED TV 55 inch", "4K Ultra HD TV 50 inch",
            "Android TV 32 inch", "Android TV 43 inch", "OLED TV 55 inch", "QLED TV 65 inch",
            "Bluetooth Earbuds", "TWS Earbuds", "Wireless Neckband", "Over-Ear Headphones", "Gaming Headset",
            "Soundbar 2.1 Channel", "Soundbar with Subwoofer", "Portable Bluetooth Speaker", "Party Speaker",
            "Home Theatre System", "Smart Speaker with Alexa", "Smart Speaker with Google",
            "Smartphone 6GB RAM", "Smartphone 8GB RAM", "5G Smartphone", "Gaming Phone", "Budget Smartphone",
            "Tablet 10 inch", "Tablet 11 inch", "E-Reader", "Kids Tablet",
            "Laptop i3 8GB", "Laptop i5 16GB", "Laptop Ryzen 5", "Gaming Laptop", "Ultrabook",
            "Chromebook", "2-in-1 Laptop", "Business Laptop",
            "DSLR Camera", "Mirrorless Camera", "Action Camera", "Dash Cam", "Security Camera",
            "Webcam HD", "Webcam 4K", "Instant Camera",
            "Smartwatch", "Fitness Band", "GPS Smartwatch", "Kids Smartwatch",
            "Wireless Charger", "Fast Charger 65W", "Laptop Charger", "Universal Adapter",
            "External SSD 500GB", "External SSD 1TB", "Pen Drive 64GB", "Pen Drive 128GB",
            "Mouse Wireless", "Keyboard Wireless", "Gaming Mouse", "Mechanical Keyboard",
            "Monitor 24 inch", "Monitor 27 inch", "Curved Monitor", "Portable Monitor",
            "Router WiFi 6", "Mesh Router", "Range Extender", "4G Dongle",
            "Printer All-in-One", "Printer Laser", "UPS 600VA", "UPS 1000VA",
            "Air Purifier", "Dehumidifier", "Room Heater", "Tower Fan", "Air Cooler",
        ]
    },
    "Home & Kitchen": {
        "price_range": (199, 14999),
        "products": [
            "Non-stick Tawa", "Non-stick Kadhai", "Non-stick Frying Pan", "Pressure Cooker 3L",
            "Pressure Cooker 5L", "Induction Cooker", "Gas Stove 2 Burner", "Gas Stove 4 Burner",
            "Idli Maker", "Dosa Tawa", "Appam Pan", "Kadhai Set", "Cookware Set 5pc",
            "Stainless Steel Handi", "Biryani Pot", "Casserole Set",
            "Mixer Grinder 500W", "Mixer Grinder 750W", "Juicer Mixer Grinder", "Hand Blender",
            "Electric Kettle 1L", "Electric Kettle 1.5L", "Coffee Maker", "Espresso Machine",
            "Air Fryer", "Air Fryer Oven", "OTG Oven 20L", "OTG Oven 30L", "Microwave Solo",
            "Microwave Convection", "Sandwich Maker", "Toaster", "Roti Maker", "Rice Cooker",
            "Food Processor", "Wet Grinder", "Dough Maker", "Egg Boiler",
            "Container Set Airtight", "Spice Box", "Steel Container Set", "Glass Container Set",
            "Water Bottle Steel", "Tiffin Box", "Lunch Box Set", "Pickle Jar",
            "Vacuum Cleaner", "Robot Vacuum", "Steam Mop", "Handheld Vacuum",
            "Bedsheet Double", "Bedsheet King Size", "Comforter", "Duvet Cover", "Pillow Set",
            "Mattress Protector", "Cushion Cover Set", "Curtains",
            "Towel Set", "Bath Mat", "Shower Curtain", "Soap Dispenser", "Toilet Brush Set",
            "Dining Table 4 Seater", "Dining Table 6 Seater", "Study Table", "Computer Table",
            "Shoe Rack", "Bookshelf", "TV Unit", "Wardrobe Organizer",
            "LED Bulb 9W Pack", "LED Bulb 12W Pack", "LED Tube Light", "Ceiling Fan",
            "Table Lamp", "Floor Lamp", "Decorative Lights", "Night Lamp",
            "Wall Clock", "Photo Frame Set", "Wall Hanging", "Artificial Plant", "Vase Set",
        ]
    },
    "Clothing - Men": {
        "price_range": (299, 4999),
        "products": [
            "Kurta Cotton", "Kurta Silk", "Kurta Pajama Set", "Sherwani", "Nehru Jacket",
            "Dhoti", "Lungi Cotton", "Pathani Suit",
            "T-shirt Round Neck", "T-shirt V Neck", "T-shirt Polo", "T-shirt Printed",
            "Casual Shirt", "Denim Shirt", "Linen Shirt", "Flannel Shirt",
            "Jeans Slim Fit", "Jeans Regular Fit", "Jeans Stretch", "Cargo Pants",
            "Chinos", "Formal Trousers", "Track Pants", "Joggers", "Shorts",
            "Formal Shirt White", "Formal Shirt Blue", "Formal Shirt Striped",
            "Blazer", "Suit 2 Piece", "Suit 3 Piece", "Waistcoat",
            "Sweater", "Cardigan", "Hoodie", "Sweatshirt", "Jacket Casual",
            "Jacket Leather", "Winter Jacket", "Puffer Jacket", "Windcheater",
            "Vest Cotton Pack", "Brief Pack", "Boxer Pack", "Thermal Set",
            "Night Suit", "Pajama Set", "Robe",
            "Sports T-shirt", "Track Suit", "Gym Shorts", "Compression Tights",
        ]
    },
    "Clothing - Women": {
        "price_range": (399, 7999),
        "products": [
            "Saree Cotton", "Saree Silk", "Saree Georgette", "Saree Chiffon", "Saree Banarasi",
            "Salwar Suit Cotton", "Salwar Suit Chanderi", "Anarkali Suit", "Palazzo Suit",
            "Kurti Cotton", "Kurti Rayon", "Kurti Silk", "Kurti Printed", "Kurti Embroidered",
            "Lehenga Choli", "Ghagra Choli", "Sharara Set", "Dupatta",
            "Top Casual", "Top Formal", "Blouse", "Tunic", "Crop Top",
            "Dress Casual", "Dress Party", "Maxi Dress", "Mini Dress", "Midi Dress",
            "Jeans Skinny", "Jeans Bootcut", "Jeggings", "Palazzo Pants",
            "Skirt A-line", "Skirt Pencil", "Shorts Denim", "Capri",
            "Formal Shirt", "Blazer Women", "Jumpsuit",
            "Cardigan", "Sweater", "Hoodie Women", "Sweatshirt",
            "Jacket Casual", "Jacket Denim", "Winter Coat", "Shrug",
            "Bra Cotton", "Bra Padded", "Sports Bra", "Panty Set",
            "Night Suit", "Night Gown", "Pajama Set Women",
            "Yoga Pants", "Gym Wear Set", "Sports Top",
        ]
    },
    "Footwear": {
        "price_range": (299, 7999),
        "products": [
            "Running Shoes Men", "Walking Shoes Men", "Training Shoes Men", "Sports Shoes Men",
            "Cricket Shoes", "Football Boots", "Badminton Shoes",
            "Sneakers Men", "Canvas Shoes Men", "Loafers Men", "Slip-on Men",
            "Flip Flops Men", "Sandals Men", "Floaters Men", "Slippers Men",
            "Formal Shoes Black", "Formal Shoes Brown", "Oxford Shoes", "Derby Shoes",
            "Brogues", "Monk Straps",
            "Mojari Men", "Kolhapuri Chappal Men", "Juttis Men",
            "Running Shoes Women", "Walking Shoes Women", "Sports Shoes Women", "Gym Shoes Women",
            "Sneakers Women", "Canvas Shoes Women", "Loafers Women", "Slip-on Women",
            "Flip Flops Women", "Sandals Women", "Flats Women", "Bellies",
            "Heels Stiletto", "Heels Block", "Heels Kitten", "Wedges", "Platform Heels",
            "Mojari Women", "Kolhapuri Women", "Juttis Women", "Ethnic Flats",
            "School Shoes Kids", "Sports Shoes Kids", "Sandals Kids", "Flip Flops Kids",
            "Light Up Shoes Kids", "Velcro Shoes Kids",
            "Ankle Boots Men", "Chelsea Boots", "Hiking Boots", "Ankle Boots Women",
        ]
    },
    "Beauty & Personal Care": {
        "price_range": (49, 2999),
        "products": [
            "Face Wash", "Face Wash Neem", "Face Wash Charcoal", "Facewash Vitamin C",
            "Face Scrub", "Face Pack", "Face Serum", "Face Moisturizer", "Face Cream",
            "Night Cream", "Sunscreen SPF 30", "Sunscreen SPF 50", "Toner", "Face Mist",
            "Under Eye Cream", "Lip Balm", "Lip Scrub",
            "Shampoo", "Shampoo Anti-Dandruff", "Shampoo Keratin", "Shampoo Onion",
            "Conditioner", "Hair Mask", "Hair Oil Coconut", "Hair Oil Almond",
            "Hair Oil Bhringraj", "Hair Serum", "Hair Gel", "Hair Wax", "Hair Spray",
            "Body Lotion", "Body Wash", "Body Scrub", "Body Oil", "Hand Cream",
            "Foot Cream", "Deo Spray Men", "Deo Spray Women", "Deo Roll-on",
            "Perfume Men", "Perfume Women", "Attar",
            "Foundation", "Compact Powder", "Loose Powder", "Primer",
            "Lipstick Matte", "Lipstick Liquid", "Lip Gloss", "Lip Liner",
            "Eyeliner", "Kajal", "Mascara", "Eyeshadow Palette",
            "Blush", "Highlighter", "Bronzer", "Contour Kit",
            "Nail Polish", "Nail Art Kit", "Makeup Remover", "Makeup Brush Set",
            "Beard Oil", "Beard Balm", "Trimmer", "Shaving Foam", "After Shave",
            "Razor", "Shaving Kit",
            "Multivitamin", "Vitamin C Tablets", "Biotin", "Protein Powder",
            "Collagen Powder", "Fish Oil", "Ayurvedic Chyawanprash",
        ]
    },
    "Grocery & Gourmet": {
        "price_range": (29, 1499),
        "products": [
            "Basmati Rice 1kg", "Basmati Rice 5kg", "Brown Rice 1kg", "Sona Masoori Rice 5kg",
            "Wheat Atta 5kg", "Wheat Atta 10kg", "Multigrain Atta", "Besan 1kg",
            "Maida 1kg", "Rava 1kg", "Poha 500g", "Rice Flour 1kg",
            "Toor Dal 1kg", "Chana Dal 1kg", "Moong Dal 1kg", "Urad Dal 1kg",
            "Masoor Dal 1kg", "Rajma 1kg", "Kabuli Chana 1kg", "Black Chana 1kg",
            "Sunflower Oil 1L", "Mustard Oil 1L", "Groundnut Oil 1L", "Coconut Oil 1L",
            "Olive Oil 500ml", "Rice Bran Oil 1L", "Sesame Oil 500ml", "Ghee 1kg",
            "Turmeric Powder 200g", "Red Chilli Powder 200g", "Coriander Powder 200g",
            "Cumin Powder 100g", "Garam Masala 100g", "Sambar Masala 100g",
            "Biryani Masala 100g", "Chicken Masala 100g", "Kitchen King Masala",
            "Black Pepper 100g", "Cardamom 50g", "Cinnamon 100g", "Cloves 50g",
            "Tea Powder 500g", "Tea Leaves Premium", "Green Tea 100 bags",
            "Coffee Powder 200g", "Instant Coffee 100g", "Filter Coffee Powder",
            "Sugar 2kg", "Sugar 5kg", "Brown Sugar 500g", "Jaggery 1kg",
            "Honey 500g", "Honey 1kg", "Organic Honey 250g",
            "Namkeen Mixture 400g", "Bhujia 400g", "Chakli 300g", "Murukku 300g",
            "Chips 150g", "Biscuits Cream", "Biscuits Chocolate", "Cookies 300g",
            "Dry Fruits Mix 500g", "Almonds 250g", "Cashews 250g", "Raisins 250g",
            "Mango Juice 1L", "Orange Juice 1L", "Mixed Fruit Juice 1L",
            "Soft Drink 2L", "Sparkling Water 1L",
            "Instant Noodles Pack", "Pasta 500g", "Vermicelli 500g", "Oats 1kg",
            "Breakfast Cereal 500g", "Cornflakes 500g", "Muesli 500g",
            "Tomato Ketchup 500g", "Mayonnaise 250g", "Peanut Butter 400g",
            "Jam Mixed Fruit 500g", "Pickle Mango 400g", "Pickle Mixed 400g",
        ]
    },
    "Sports & Fitness": {
        "price_range": (199, 9999),
        "products": [
            "Cricket Bat English Willow", "Cricket Bat Kashmir Willow", "Cricket Ball Leather",
            "Cricket Ball Tennis", "Cricket Gloves", "Cricket Pads", "Cricket Helmet",
            "Cricket Kit Bag", "Cricket Stumps Set",
            "Badminton Racket", "Badminton Racket Set", "Shuttlecock Feather", "Shuttlecock Nylon",
            "Badminton Net",
            "Football Size 5", "Football Goal Net", "Football Shin Guards", "Football Gloves",
            "Tennis Racket", "Tennis Balls Pack", "Table Tennis Bat", "TT Balls Pack", "TT Table",
            "Dumbbell Set", "Dumbbell 5kg Pair", "Dumbbell 10kg Pair", "Kettlebell",
            "Barbell Set", "Weight Plates", "Resistance Bands Set", "Pull Up Bar",
            "Ab Roller", "Push Up Board", "Skipping Rope", "Hand Gripper",
            "Yoga Mat 6mm", "Yoga Mat 8mm", "Yoga Block", "Yoga Strap", "Yoga Wheel",
            "Foam Roller", "Acupressure Mat",
            "Bicycle Adult", "Bicycle Kids", "Cycling Helmet", "Cycling Gloves",
            "Bicycle Lock", "Bicycle Pump", "Bottle Cage",
            "Swimming Goggles", "Swimming Cap", "Swim Shorts", "Swimsuit Women",
            "Ear Plugs Swimming", "Kickboard",
            "Camping Tent 2 Person", "Camping Tent 4 Person", "Sleeping Bag", "Hiking Backpack",
            "Trekking Pole", "Torch Rechargeable", "Binoculars", "Compass",
            "Knee Cap", "Ankle Support", "Wrist Support", "Back Support Belt",
            "Carrom Board", "Chess Board", "Frisbee", "Volleyball", "Basketball",
        ]
    },
    "Toys & Baby": {
        "price_range": (149, 4999),
        "products": [
            "Baby Diaper Pack S", "Baby Diaper Pack M", "Baby Diaper Pack L", "Baby Diaper Pack XL",
            "Baby Wipes", "Baby Powder", "Baby Oil", "Baby Lotion", "Baby Shampoo",
            "Baby Soap", "Diaper Rash Cream",
            "Baby Bottle 250ml", "Baby Bottle Set", "Sipper Cup", "Feeding Spoon Set",
            "Breast Pump Manual", "Breast Pump Electric", "Sterilizer", "Bottle Warmer",
            "Baby Food Maker",
            "Baby Stroller", "Baby Carrier", "Baby Walker", "Baby Bouncer", "Baby Swing",
            "Car Seat Baby", "Baby Crib", "Baby Bedding Set", "Baby Blanket",
            "Baby Mosquito Net",
            "Baby Romper", "Baby Dress", "Baby T-shirt Pack", "Baby Pajama Set",
            "Baby Bib Set", "Baby Cap Set", "Baby Mittens Set", "Baby Booties",
            "Building Blocks 100pc", "Building Blocks 200pc", "STEM Kit", "Science Kit",
            "Alphabet Puzzle", "Number Puzzle", "Shape Sorter", "Stacking Rings",
            "Abacus", "Globe Educational", "Flash Cards Set",
            "Action Figure Superhero", "Action Figure Set", "Doll Set", "Barbie Doll",
            "Kitchen Playset", "Doctor Playset", "Tool Kit Toy",
            "Remote Control Car", "Remote Control Helicopter", "Train Set", "Die Cast Cars Set",
            "Ride-on Car", "Bicycle Kids 16 inch", "Tricycle",
            "Monopoly", "Scrabble", "Ludo", "Snakes and Ladders", "Jenga", "UNO Cards",
            "Chess Set", "Carrom Board Kids",
            "Swing Set", "Slide Kids", "Ball Pit", "Sandbox", "Bubbles Set",
            "Teddy Bear", "Teddy Bear Giant", "Soft Toy Bunny", "Soft Toy Elephant",
            "Baby Rattle Set", "Musical Toy",
        ]
    },
    "Automotive": {
        "price_range": (149, 14999),
        "products": [
            "Car Seat Cover Set", "Car Seat Cover Leather", "Steering Wheel Cover",
            "Dashboard Mat", "Gear Knob Cover", "Handbrake Cover", "Floor Mat Set",
            "Car Cushion Lumbar", "Neck Pillow Car",
            "Car Cover", "Car Cover Waterproof", "Mud Flaps", "Door Guard", "Bumper Guard",
            "Roof Rack", "Car Antenna",
            "Car Shampoo", "Car Polish", "Car Wax", "Glass Cleaner", "Dashboard Polish",
            "Tyre Shine", "Scratch Remover", "Car Perfume", "Car Air Freshener",
            "Microfiber Cloth Set", "Chamois Leather", "Car Duster",
            "Car Charger", "Car Charger Fast", "Phone Holder Magnetic", "Phone Holder Vent",
            "Dash Cam 1080p", "Dash Cam 4K", "Reverse Camera", "Parking Sensor Kit",
            "Car Bluetooth Kit", "FM Transmitter", "Car Speaker Set", "Subwoofer Car",
            "Tyre Inflator", "Jump Starter", "Car Vacuum Cleaner", "Car Tool Kit",
            "Puncture Repair Kit", "Tow Rope", "First Aid Kit Car", "Fire Extinguisher Car",
            "Bike Helmet Full Face", "Bike Helmet Half Face", "Bike Helmet Open Face",
            "Riding Jacket", "Riding Gloves", "Riding Boots", "Knee Guards", "Elbow Guards",
            "Bike Cover", "Bike Lock", "Bike Phone Holder", "Tank Bag",
            "Bike Mirror", "Bike Grip", "Bike LED Light",
            "Engine Oil 1L", "Engine Oil 4L", "Brake Fluid", "Coolant 1L",
            "Battery Car", "Battery Bike", "Spark Plug",
        ]
    },
    "Mobile Accessories": {
        "price_range": (99, 3999),
        "products": [
            "Phone Case Clear", "Phone Case Rugged", "Phone Case Leather", "Phone Case Silicone",
            "Phone Case Designer", "Phone Case Wallet", "Phone Case Armor",
            "Back Cover Soft", "Back Cover Hard", "Bumper Case",
            "Tempered Glass", "Tempered Glass Privacy", "Screen Protector Matte",
            "Camera Lens Protector", "Full Coverage Screen Guard",
            "Charger 18W", "Charger 33W", "Charger 65W", "Charger 120W",
            "Wireless Charger Pad", "Wireless Charger Stand", "Car Charger 20W",
            "Car Charger Dual", "Travel Adapter",
            "USB C Cable 1m", "USB C Cable 2m", "Lightning Cable", "Micro USB Cable",
            "Cable 3-in-1", "Braided Cable", "Fast Charging Cable",
            "Power Bank 10000mAh", "Power Bank 20000mAh", "Power Bank 30000mAh",
            "Power Bank Slim", "Power Bank Solar", "Power Bank Wireless",
            "Earphones Wired", "Earphones Type C", "TWS Earbuds Budget", "TWS Earbuds Premium",
            "Neckband Wireless", "Headphones Over-Ear", "Gaming Earphones",
            "Earbuds Case", "Ear Tips Replacement",
            "Phone Stand Desktop", "Phone Stand Adjustable", "Tripod Phone", "Ring Holder",
            "Pop Socket", "Car Mount Vent", "Car Mount Dashboard", "Bike Phone Mount",
            "Memory Card 32GB", "Memory Card 64GB", "Memory Card 128GB", "Memory Card 256GB",
            "OTG Adapter", "Card Reader",
            "Selfie Stick", "Selfie Stick with Tripod", "Ring Light", "Gimbal Phone",
            "Lens Kit Phone", "Microphone Phone",
            "Game Controller Phone", "Trigger Phone", "Cooling Fan Phone",
            "Screen Cleaning Kit", "Cleaning Cloth",
        ]
    },
    "Books & Stationery": {
        "price_range": (49, 1999),
        "products": [
            "Novel Bestseller", "Fiction Thriller", "Fiction Romance", "Fiction Mystery",
            "Classic Literature", "Short Stories Collection", "Poetry Collection",
            "Self Help Book", "Biography", "Autobiography", "Business Book",
            "Finance Book", "Leadership Book", "Motivational Book", "Spirituality Book",
            "NCERT Class 10 Set", "NCERT Class 12 Set", "JEE Preparation Book",
            "NEET Preparation Book", "UPSC Preparation Set", "SSC Preparation Book",
            "CAT Preparation Book", "GRE Preparation Book",
            "Engineering Textbook", "Medical Textbook", "Law Book",
            "Picture Book Kids", "Story Book Kids", "Activity Book", "Coloring Book",
            "Fairy Tales Collection", "Comics", "Encyclopedia Kids",
            "English Grammar Book", "Hindi Learning Book", "French Learning Book",
            "German Learning Book", "Dictionary English", "Thesaurus",
            "Notebook Ruled A4", "Notebook A5 Pack", "Spiral Notebook", "Long Book",
            "Register 200 Pages", "Diary 2025", "Planner 2025", "Journal",
            "Pen Set", "Ball Pen Pack 10", "Gel Pen Pack", "Fountain Pen",
            "Pencil Pack", "Mechanical Pencil Set", "Marker Set", "Highlighter Set",
            "Sketch Pen Set", "Color Pencil Set 24", "Crayon Set 24", "Oil Pastels",
            "Stapler", "Punch Machine", "Paper Clips Box", "Binder Clips",
            "Sticky Notes", "File Folder Set", "Envelope Pack", "Tape Dispenser",
            "Scissors Office", "Glue Stick Pack", "Correction Pen",
            "Watercolor Set", "Acrylic Paint Set", "Canvas Board Pack", "Paint Brushes Set",
            "Sketch Pad A3", "Drawing Book A4",
            "School Bag Kids", "School Bag Teen", "College Backpack", "Laptop Bag",
            "Sling Bag", "Pencil Pouch", "Geometry Box",
        ]
    }
}

# Indian Brands for variety
BRANDS = {
    "Electronics": ["Samsung", "LG", "Sony", "OnePlus", "Xiaomi", "boAt", "JBL", "realme", "ASUS", "HP", "Dell", "Lenovo"],
    "Home & Kitchen": ["Prestige", "Pigeon", "Hawkins", "Bajaj", "Philips", "Morphy Richards", "Borosil", "Milton"],
    "Clothing - Men": ["Allen Solly", "Van Heusen", "Peter England", "Raymond", "Jockey", "Levi's", "US Polo", "Louis Philippe"],
    "Clothing - Women": ["Biba", "W", "Aurelia", "Libas", "Global Desi", "FabIndia", "Zara", "H&M"],
    "Footwear": ["Bata", "Relaxo", "Sparx", "Campus", "Nike", "Adidas", "Puma", "Red Tape", "Woodland"],
    "Beauty & Personal Care": ["Lakme", "Maybelline", "L'Oreal", "Himalaya", "Biotique", "Mamaearth", "Nivea", "Dove"],
    "Grocery & Gourmet": ["Fortune", "Aashirvaad", "Tata", "Patanjali", "MTR", "Saffola", "Dabur", "Amul"],
    "Sports & Fitness": ["SG", "SS", "Nivia", "Cosco", "Yonex", "Vector X", "KOBO", "Boldfit"],
    "Toys & Baby": ["Funskool", "Fisher-Price", "Huggies", "Pampers", "Himalaya Baby", "Chicco", "Lego", "Hot Wheels"],
    "Automotive": ["Bosch", "3M", "Amaron", "Exide", "Minda", "Philips", "CEAT", "MRF"],
    "Mobile Accessories": ["Mi", "Spigen", "Portronics", "Ambrane", "pTron", "Anker", "Belkin", "UGREEN"],
    "Books & Stationery": ["Classmate", "Navneet", "Doms", "Faber-Castell", "Camlin", "Nataraj", "Penguin", "Arihant"]
}

VARIANTS = ["", " - Premium", " - Value Pack", " - Combo", " - Pro", " - Lite", " - Plus", " - XL", " - Mini"]

WAREHOUSES = [
    "Mumbai Warehouse",
    "Delhi Warehouse", 
    "Bengaluru Warehouse",
    "Chennai Warehouse",
    "Hyderabad Warehouse"
]

CUSTOMERS = [
    {"customer_id": "CUST2001", "name": "Amit Verma", "email": "amit.verma@gmail.com", "phone": "+91-9000000001", "location": "Mumbai, Maharashtra", "loyalty_tier": "Platinum", "loyalty_points": 4200},
    {"customer_id": "CUST2002", "name": "Neha Reddy", "email": "neha.reddy@gmail.com", "phone": "+91-9000000002", "location": "Bengaluru, Karnataka", "loyalty_tier": "Gold", "loyalty_points": 2100},
    {"customer_id": "CUST2003", "name": "Rohit Sharma", "email": "rohit.sharma@gmail.com", "phone": "+91-9000000003", "location": "Delhi, NCR", "loyalty_tier": "Silver", "loyalty_points": 950},
    {"customer_id": "CUST2004", "name": "Priya Singh", "email": "priya.singh@gmail.com", "phone": "+91-9000000004", "location": "Chennai, Tamil Nadu", "loyalty_tier": "Gold", "loyalty_points": 1800},
    {"customer_id": "CUST2005", "name": "Suresh Kumar", "email": "suresh.kumar@gmail.com", "phone": "+91-9000000005", "location": "Hyderabad, Telangana", "loyalty_tier": "Bronze", "loyalty_points": 300},
    {"customer_id": "CUST2006", "name": "Anjali Gupta", "email": "anjali.gupta@gmail.com", "phone": "+91-9000000006", "location": "Pune, Maharashtra", "loyalty_tier": "Gold", "loyalty_points": 2400},
    {"customer_id": "CUST2007", "name": "Vikram Patel", "email": "vikram.patel@gmail.com", "phone": "+91-9000000007", "location": "Ahmedabad, Gujarat", "loyalty_tier": "Silver", "loyalty_points": 1100},
    {"customer_id": "CUST2008", "name": "Sana Khan", "email": "sana.khan@gmail.com", "phone": "+91-9000000008", "location": "Lucknow, Uttar Pradesh", "loyalty_tier": "Bronze", "loyalty_points": 400},
    {"customer_id": "CUST2009", "name": "Manish Desai", "email": "manish.desai@gmail.com", "phone": "+91-9000000009", "location": "Vadodara, Gujarat", "loyalty_tier": "Gold", "loyalty_points": 1750},
    {"customer_id": "CUST2010", "name": "Kavya Nair", "email": "kavya.nair@gmail.com", "phone": "+91-9000000010", "location": "Kochi, Kerala", "loyalty_tier": "Silver", "loyalty_points": 980},
    {"customer_id": "CUST2011", "name": "Arjun Mehta", "email": "arjun.mehta@gmail.com", "phone": "+91-9000000011", "location": "Jaipur, Rajasthan", "loyalty_tier": "Gold", "loyalty_points": 2000},
    {"customer_id": "CUST2012", "name": "Meera Iyer", "email": "meera.iyer@gmail.com", "phone": "+91-9000000012", "location": "Coimbatore, Tamil Nadu", "loyalty_tier": "Bronze", "loyalty_points": 150},
    {"customer_id": "CUST2013", "name": "Kabir Khan", "email": "kabir.khan@gmail.com", "phone": "+91-9000000013", "location": "Bhopal, Madhya Pradesh", "loyalty_tier": "Silver", "loyalty_points": 860},
    {"customer_id": "CUST2014", "name": "Ritika Bose", "email": "ritika.bose@gmail.com", "phone": "+91-9000000014", "location": "Kolkata, West Bengal", "loyalty_tier": "Gold", "loyalty_points": 1900},
    {"customer_id": "CUST2015", "name": "Aditya Rao", "email": "aditya.rao@gmail.com", "phone": "+91-9000000015", "location": "Mysuru, Karnataka", "loyalty_tier": "Bronze", "loyalty_points": 230},
    {"customer_id": "CUST2016", "name": "Sneha Kapoor", "email": "sneha.kapoor@gmail.com", "phone": "+91-9000000016", "location": "Gurgaon, Haryana", "loyalty_tier": "Gold", "loyalty_points": 2600},
    {"customer_id": "CUST2017", "name": "Praveen Kumar", "email": "praveen.kumar@gmail.com", "phone": "+91-9000000017", "location": "Chandigarh, Punjab", "loyalty_tier": "Silver", "loyalty_points": 720},
    {"customer_id": "CUST2018", "name": "Isha Malhotra", "email": "isha.malhotra@gmail.com", "phone": "+91-9000000018", "location": "Indore, Madhya Pradesh", "loyalty_tier": "Gold", "loyalty_points": 1550},
    {"customer_id": "CUST2019", "name": "Soham Patil", "email": "soham.patil@gmail.com", "phone": "+91-9000000019", "location": "Nagpur, Maharashtra", "loyalty_tier": "Bronze", "loyalty_points": 410},
    {"customer_id": "CUST2020", "name": "Nisha Sharma", "email": "nisha.sharma@gmail.com", "phone": "+91-9000000020", "location": "Ranchi, Jharkhand", "loyalty_tier": "Silver", "loyalty_points": 640},
    {"customer_id": "CUST2021", "name": "Ankit Joshi", "email": "ankit.joshi@gmail.com", "phone": "+91-9000000021", "location": "Dehradun, Uttarakhand", "loyalty_tier": "Gold", "loyalty_points": 2100},
    {"customer_id": "CUST2022", "name": "Pooja Yadav", "email": "pooja.yadav@gmail.com", "phone": "+91-9000000022", "location": "Patna, Bihar", "loyalty_tier": "Bronze", "loyalty_points": 120},
    {"customer_id": "CUST2023", "name": "Harish Chandra", "email": "harish.chandra@gmail.com", "phone": "+91-9000000023", "location": "Surat, Gujarat", "loyalty_tier": "Silver", "loyalty_points": 880},
    {"customer_id": "CUST2024", "name": "Geeta Rani", "email": "geeta.rani@gmail.com", "phone": "+91-9000000024", "location": "Jodhpur, Rajasthan", "loyalty_tier": "Bronze", "loyalty_points": 270},
    {"customer_id": "CUST2025", "name": "Vivek Nambiar", "email": "vivek.nambiar@gmail.com", "phone": "+91-9000000025", "location": "Thiruvananthapuram, Kerala", "loyalty_tier": "Gold", "loyalty_points": 2350},
    {"customer_id": "CUST2026", "name": "Latha R", "email": "latha.r@gmail.com", "phone": "+91-9000000026", "location": "Mangalore, Karnataka", "loyalty_tier": "Silver", "loyalty_points": 980},
    {"customer_id": "CUST2027", "name": "Ramesh Babu", "email": "ramesh.babu@gmail.com", "phone": "+91-9000000027", "location": "Vijayawada, Andhra Pradesh", "loyalty_tier": "Bronze", "loyalty_points": 360},
    {"customer_id": "CUST2028", "name": "Shweta Goyal", "email": "shweta.goyal@gmail.com", "phone": "+91-9000000028", "location": "Faridabad, Haryana", "loyalty_tier": "Gold", "loyalty_points": 1980},
    {"customer_id": "CUST2029", "name": "Karan B", "email": "karan.b@gmail.com", "phone": "+91-9000000029", "location": "Noida, Uttar Pradesh", "loyalty_tier": "Silver", "loyalty_points": 740},
    {"customer_id": "CUST2030", "name": "Tulsi Das", "email": "tulsi.das@gmail.com", "phone": "+91-9000000030", "location": "Dibrugarh, Assam", "loyalty_tier": "Bronze", "loyalty_points": 95},
    {"customer_id": "CUST2031", "name": "Vedant Shah", "email": "vedant.shah@gmail.com", "phone": "+91-9000000031", "location": "Mumbai, Maharashtra", "loyalty_tier": "Platinum", "loyalty_points": 5000},
    {"customer_id": "CUST2032", "name": "Riya Patel", "email": "riya.patel@gmail.com", "phone": "+91-9000000032", "location": "Ahmedabad, Gujarat", "loyalty_tier": "Gold", "loyalty_points": 2200},
]

# Timed promotions with valid_from and valid_until dates
PROMOTIONS = [
    {
        "promo_code": "WELCOME50", 
        "code": "WELCOME50",
        "description": "₹50 off on first order", 
        "discount_percent": 10.0, 
        "discount_amount": 50.0, 
        "min_order": 0,
        "min_purchase": 0,
        "valid_from": None,  # Always valid (no start date)
        "valid_until": None  # Never expires
    },
    {
        "promo_code": "DIWALI20", 
        "code": "DIWALI20",
        "description": "20% off for Diwali sale - Limited time!", 
        "discount_percent": 20.0, 
        "discount_amount": None, 
        "min_order": 500,
        "min_purchase": 500,
        "valid_from": "2025-10-15",  # Diwali season start
        "valid_until": "2025-12-31"  # Valid till end of year
    },
    {
        "promo_code": "FESTIVE100", 
        "code": "FESTIVE100",
        "description": "Flat ₹100 off above ₹2000 - Festival Season", 
        "discount_percent": 5.0, 
        "discount_amount": 100.0, 
        "min_order": 2000,
        "min_purchase": 2000,
        "valid_from": "2025-11-01",
        "valid_until": "2025-12-25"  # Till Christmas
    },
    {
        "promo_code": "NEWUSER", 
        "code": "NEWUSER",
        "description": "15% off for new users", 
        "discount_percent": 15.0, 
        "discount_amount": None, 
        "min_order": 0,
        "min_purchase": 0,
        "valid_from": None,  # Always valid
        "valid_until": None  # Never expires
    },
    {
        "promo_code": "FLAT500", 
        "code": "FLAT500",
        "description": "₹500 off above ₹5000 - Weekend Special", 
        "discount_percent": 10.0, 
        "discount_amount": 500.0, 
        "min_order": 5000,
        "min_purchase": 5000,
        "valid_from": "2025-12-01",
        "valid_until": "2025-12-31"
    },
    {
        "promo_code": "FLASH50",
        "code": "FLASH50",
        "description": "Flash Sale - 50% off! Only today!", 
        "discount_percent": 50.0, 
        "discount_amount": None, 
        "min_order": 1000,
        "min_purchase": 1000,
        "valid_from": "2025-12-05",  # Today only
        "valid_until": "2025-12-05"  # Expires today
    },
    {
        "promo_code": "EXPIRED10",
        "code": "EXPIRED10",
        "description": "10% off - EXPIRED promotion for testing", 
        "discount_percent": 10.0, 
        "discount_amount": None, 
        "min_order": 0,
        "min_purchase": 0,
        "valid_from": "2025-01-01",
        "valid_until": "2025-11-30"  # Already expired
    },
    {
        "promo_code": "NEWYEAR25",
        "code": "NEWYEAR25",
        "description": "25% off - Coming soon for New Year!", 
        "discount_percent": 25.0, 
        "discount_amount": None, 
        "min_order": 1500,
        "min_purchase": 1500,
        "valid_from": "2025-12-25",  # Not yet active
        "valid_until": "2026-01-07"
    },
]


def generate_products():
    """Generate 1200+ products balanced across categories"""
    products = []
    sku_num = 1001
    
    for category, data in CATEGORIES.items():
        base_products = data["products"]
        price_range = data["price_range"]
        brands = BRANDS.get(category, ["Generic"])
        
        target_count = max(100, len(base_products))
        count = 0
        
        while count < target_count:
            for base in base_products:
                if count >= target_count:
                    break
                    
                brand = random.choice(brands)
                variant = random.choice(VARIANTS)
                
                if random.random() > 0.5:
                    name = f"{brand} {base}{variant}"
                else:
                    name = f"{base}{variant}"
                
                min_p, max_p = price_range
                price = round(random.uniform(min_p, max_p), 2)
                
                if random.random() > 0.7:
                    price = round(price / 100) * 100 - 1
                
                rating = round(random.uniform(3.5, 5.0), 1)
                reviews = random.randint(10, 15000)
                
                sku = f"IND{sku_num}"
                sku_num += 1
                
                products.append({
                    "sku": sku,
                    "name": name.strip(),
                    "category": category,
                    "current_price": max(price, min_p),
                    "rating": rating,
                    "reviews_count": reviews
                })
                count += 1
    
    return products


def populate_firebase():
    """Populate Firebase with all data"""
    from utils.firebase_db import get_db, create_product, create_customer, update_inventory, create_promotion
    
    print("\n" + "="*60)
    print("🚀 POPULATING FIREBASE WITH 1200+ INDIAN PRODUCTS")
    print("="*60)
    
    db = get_db()
    
    # Generate products
    print("\n🏭 Generating products...")
    products = generate_products()
    print(f"   ✅ Generated {len(products)} products")
    
    # Show category distribution
    print("\n📊 Category Distribution:")
    from collections import Counter
    cat_counts = Counter(p["category"] for p in products)
    for cat, count in sorted(cat_counts.items()):
        print(f"   • {cat}: {count} products")
    
    # Insert products
    print(f"\n📦 Inserting {len(products)} products into Firebase...")
    batch_size = 100
    for i in range(0, len(products), batch_size):
        batch = products[i:i+batch_size]
        for p in batch:
            create_product(p)
        print(f"   ✅ Inserted {min(i+batch_size, len(products))}/{len(products)} products")
    
    # Insert customers
    print(f"\n👥 Inserting {len(CUSTOMERS)} customers...")
    for c in CUSTOMERS:
        c['browsing_history'] = []
        c['purchase_history'] = []
        c['preferences'] = {}
        create_customer(c)
    print(f"   ✅ Inserted {len(CUSTOMERS)} customers")
    
    # Insert inventory
    print(f"\n🏪 Adding inventory across {len(WAREHOUSES)} warehouses...")
    inv_count = 0
    for p in products:
        for warehouse in WAREHOUSES:
            if warehouse == "Mumbai Warehouse":
                qty = random.randint(50, 500)
            else:
                qty = random.randint(10, 200)
            update_inventory(p["sku"], warehouse, qty)
            inv_count += 1
        if inv_count % 500 == 0:
            print(f"   ✅ Inserted {inv_count} inventory entries")
    print(f"   ✅ Inserted {inv_count} inventory entries")
    
    # Insert promotions
    print(f"\n🎁 Adding promotions...")
    for promo in PROMOTIONS:
        create_promotion(promo)
    print(f"   ✅ Inserted {len(PROMOTIONS)} promotions")
    
    print("\n" + "="*60)
    print("🎉 FIREBASE POPULATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n   📦 Products: {len(products)}")
    print(f"   🏪 Inventory entries: {inv_count}")
    print(f"   👥 Customers: {len(CUSTOMERS)}")
    print(f"   🏭 Warehouses: {len(WAREHOUSES)}")
    print(f"   📁 Categories: {len(CATEGORIES)}")
    print(f"   🎁 Promotions: {len(PROMOTIONS)}")
    print()


if __name__ == "__main__":
    populate_firebase()
