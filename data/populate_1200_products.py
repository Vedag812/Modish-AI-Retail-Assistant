"""
Populate Neon PostgreSQL with 1200+ Indian products
Balanced across 12 categories (100+ products each)

Usage: python data/populate_1200_products.py
"""
import random
import sys
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.db import get_db

# 12 Categories - Each will have 100+ products
CATEGORIES = {
    "Electronics": {
        "price_range": (2999, 79999),
        "products": [
            # TVs
            "Smart LED TV 32 inch", "Smart LED TV 43 inch", "Smart LED TV 55 inch", "4K Ultra HD TV 50 inch",
            "Android TV 32 inch", "Android TV 43 inch", "OLED TV 55 inch", "QLED TV 65 inch",
            # Audio
            "Bluetooth Earbuds", "TWS Earbuds", "Wireless Neckband", "Over-Ear Headphones", "Gaming Headset",
            "Soundbar 2.1 Channel", "Soundbar with Subwoofer", "Portable Bluetooth Speaker", "Party Speaker",
            "Home Theatre System", "Smart Speaker with Alexa", "Smart Speaker with Google",
            # Phones & Tablets
            "Smartphone 6GB RAM", "Smartphone 8GB RAM", "5G Smartphone", "Gaming Phone", "Budget Smartphone",
            "Tablet 10 inch", "Tablet 11 inch", "E-Reader", "Kids Tablet",
            # Laptops
            "Laptop i3 8GB", "Laptop i5 16GB", "Laptop Ryzen 5", "Gaming Laptop", "Ultrabook",
            "Chromebook", "2-in-1 Laptop", "Business Laptop",
            # Cameras
            "DSLR Camera", "Mirrorless Camera", "Action Camera", "Dash Cam", "Security Camera",
            "Webcam HD", "Webcam 4K", "Instant Camera",
            # Wearables
            "Smartwatch", "Fitness Band", "GPS Smartwatch", "Kids Smartwatch",
            # Accessories
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
            # Cookware
            "Non-stick Tawa", "Non-stick Kadhai", "Non-stick Frying Pan", "Pressure Cooker 3L",
            "Pressure Cooker 5L", "Induction Cooker", "Gas Stove 2 Burner", "Gas Stove 4 Burner",
            "Idli Maker", "Dosa Tawa", "Appam Pan", "Kadhai Set", "Cookware Set 5pc",
            "Stainless Steel Handi", "Biryani Pot", "Casserole Set",
            # Appliances
            "Mixer Grinder 500W", "Mixer Grinder 750W", "Juicer Mixer Grinder", "Hand Blender",
            "Electric Kettle 1L", "Electric Kettle 1.5L", "Coffee Maker", "Espresso Machine",
            "Air Fryer", "Air Fryer Oven", "OTG Oven 20L", "OTG Oven 30L", "Microwave Solo",
            "Microwave Convection", "Sandwich Maker", "Toaster", "Roti Maker", "Rice Cooker",
            "Food Processor", "Wet Grinder", "Dough Maker", "Egg Boiler",
            # Storage
            "Container Set Airtight", "Spice Box", "Steel Container Set", "Glass Container Set",
            "Water Bottle Steel", "Tiffin Box", "Lunch Box Set", "Pickle Jar",
            # Cleaning
            "Vacuum Cleaner", "Robot Vacuum", "Steam Mop", "Handheld Vacuum",
            # Bedroom
            "Bedsheet Double", "Bedsheet King Size", "Comforter", "Duvet Cover", "Pillow Set",
            "Mattress Protector", "Cushion Cover Set", "Curtains",
            # Bathroom
            "Towel Set", "Bath Mat", "Shower Curtain", "Soap Dispenser", "Toilet Brush Set",
            # Furniture
            "Dining Table 4 Seater", "Dining Table 6 Seater", "Study Table", "Computer Table",
            "Shoe Rack", "Bookshelf", "TV Unit", "Wardrobe Organizer",
            # Lighting
            "LED Bulb 9W Pack", "LED Bulb 12W Pack", "LED Tube Light", "Ceiling Fan",
            "Table Lamp", "Floor Lamp", "Decorative Lights", "Night Lamp",
            # Decor
            "Wall Clock", "Photo Frame Set", "Wall Hanging", "Artificial Plant", "Vase Set",
        ]
    },
    "Clothing - Men": {
        "price_range": (299, 4999),
        "products": [
            # Ethnic
            "Kurta Cotton", "Kurta Silk", "Kurta Pajama Set", "Sherwani", "Nehru Jacket",
            "Dhoti", "Lungi Cotton", "Pathani Suit",
            # Casual
            "T-shirt Round Neck", "T-shirt V Neck", "T-shirt Polo", "T-shirt Printed",
            "Casual Shirt", "Denim Shirt", "Linen Shirt", "Flannel Shirt",
            "Jeans Slim Fit", "Jeans Regular Fit", "Jeans Stretch", "Cargo Pants",
            "Chinos", "Formal Trousers", "Track Pants", "Joggers", "Shorts",
            # Formal
            "Formal Shirt White", "Formal Shirt Blue", "Formal Shirt Striped",
            "Blazer", "Suit 2 Piece", "Suit 3 Piece", "Waistcoat",
            # Winter
            "Sweater", "Cardigan", "Hoodie", "Sweatshirt", "Jacket Casual",
            "Jacket Leather", "Winter Jacket", "Puffer Jacket", "Windcheater",
            # Inner & Sleep
            "Vest Cotton Pack", "Brief Pack", "Boxer Pack", "Thermal Set",
            "Night Suit", "Pajama Set", "Robe",
            # Sports
            "Sports T-shirt", "Track Suit", "Gym Shorts", "Compression Tights",
        ]
    },
    "Clothing - Women": {
        "price_range": (399, 7999),
        "products": [
            # Ethnic
            "Saree Cotton", "Saree Silk", "Saree Georgette", "Saree Chiffon", "Saree Banarasi",
            "Salwar Suit Cotton", "Salwar Suit Chanderi", "Anarkali Suit", "Palazzo Suit",
            "Kurti Cotton", "Kurti Rayon", "Kurti Silk", "Kurti Printed", "Kurti Embroidered",
            "Lehenga Choli", "Ghagra Choli", "Sharara Set", "Dupatta",
            # Western
            "Top Casual", "Top Formal", "Blouse", "Tunic", "Crop Top",
            "Dress Casual", "Dress Party", "Maxi Dress", "Mini Dress", "Midi Dress",
            "Jeans Skinny", "Jeans Bootcut", "Jeggings", "Palazzo Pants",
            "Skirt A-line", "Skirt Pencil", "Shorts Denim", "Capri",
            "Formal Shirt", "Blazer Women", "Jumpsuit",
            # Winter
            "Cardigan", "Sweater", "Hoodie Women", "Sweatshirt",
            "Jacket Casual", "Jacket Denim", "Winter Coat", "Shrug",
            # Inner & Sleep
            "Bra Cotton", "Bra Padded", "Sports Bra", "Panty Set",
            "Night Suit", "Night Gown", "Pajama Set Women",
            # Activewear
            "Yoga Pants", "Gym Wear Set", "Sports Top",
        ]
    },
    "Footwear": {
        "price_range": (299, 7999),
        "products": [
            # Men Sports
            "Running Shoes Men", "Walking Shoes Men", "Training Shoes Men", "Sports Shoes Men",
            "Cricket Shoes", "Football Boots", "Badminton Shoes",
            # Men Casual
            "Sneakers Men", "Canvas Shoes Men", "Loafers Men", "Slip-on Men",
            "Flip Flops Men", "Sandals Men", "Floaters Men", "Slippers Men",
            # Men Formal
            "Formal Shoes Black", "Formal Shoes Brown", "Oxford Shoes", "Derby Shoes",
            "Brogues", "Monk Straps",
            # Men Ethnic
            "Mojari Men", "Kolhapuri Chappal Men", "Juttis Men",
            # Women Sports
            "Running Shoes Women", "Walking Shoes Women", "Sports Shoes Women", "Gym Shoes Women",
            # Women Casual
            "Sneakers Women", "Canvas Shoes Women", "Loafers Women", "Slip-on Women",
            "Flip Flops Women", "Sandals Women", "Flats Women", "Bellies",
            # Women Heels
            "Heels Stiletto", "Heels Block", "Heels Kitten", "Wedges", "Platform Heels",
            # Women Ethnic
            "Mojari Women", "Kolhapuri Women", "Juttis Women", "Ethnic Flats",
            # Kids
            "School Shoes Kids", "Sports Shoes Kids", "Sandals Kids", "Flip Flops Kids",
            "Light Up Shoes Kids", "Velcro Shoes Kids",
            # Boots
            "Ankle Boots Men", "Chelsea Boots", "Hiking Boots", "Ankle Boots Women",
        ]
    },
    "Beauty & Personal Care": {
        "price_range": (49, 2999),
        "products": [
            # Skincare
            "Face Wash", "Face Wash Neem", "Face Wash Charcoal", "Facewash Vitamin C",
            "Face Scrub", "Face Pack", "Face Serum", "Face Moisturizer", "Face Cream",
            "Night Cream", "Sunscreen SPF 30", "Sunscreen SPF 50", "Toner", "Face Mist",
            "Under Eye Cream", "Lip Balm", "Lip Scrub",
            # Haircare
            "Shampoo", "Shampoo Anti-Dandruff", "Shampoo Keratin", "Shampoo Onion",
            "Conditioner", "Hair Mask", "Hair Oil Coconut", "Hair Oil Almond",
            "Hair Oil Bhringraj", "Hair Serum", "Hair Gel", "Hair Wax", "Hair Spray",
            # Body Care
            "Body Lotion", "Body Wash", "Body Scrub", "Body Oil", "Hand Cream",
            "Foot Cream", "Deo Spray Men", "Deo Spray Women", "Deo Roll-on",
            "Perfume Men", "Perfume Women", "Attar",
            # Makeup
            "Foundation", "Compact Powder", "Loose Powder", "Primer",
            "Lipstick Matte", "Lipstick Liquid", "Lip Gloss", "Lip Liner",
            "Eyeliner", "Kajal", "Mascara", "Eyeshadow Palette",
            "Blush", "Highlighter", "Bronzer", "Contour Kit",
            "Nail Polish", "Nail Art Kit", "Makeup Remover", "Makeup Brush Set",
            # Men's Grooming
            "Beard Oil", "Beard Balm", "Trimmer", "Shaving Foam", "After Shave",
            "Razor", "Shaving Kit",
            # Wellness
            "Multivitamin", "Vitamin C Tablets", "Biotin", "Protein Powder",
            "Collagen Powder", "Fish Oil", "Ayurvedic Chyawanprash",
        ]
    },
    "Grocery & Gourmet": {
        "price_range": (29, 1499),
        "products": [
            # Rice & Grains
            "Basmati Rice 1kg", "Basmati Rice 5kg", "Brown Rice 1kg", "Sona Masoori Rice 5kg",
            "Wheat Atta 5kg", "Wheat Atta 10kg", "Multigrain Atta", "Besan 1kg",
            "Maida 1kg", "Rava 1kg", "Poha 500g", "Rice Flour 1kg",
            # Pulses
            "Toor Dal 1kg", "Chana Dal 1kg", "Moong Dal 1kg", "Urad Dal 1kg",
            "Masoor Dal 1kg", "Rajma 1kg", "Kabuli Chana 1kg", "Black Chana 1kg",
            # Oils
            "Sunflower Oil 1L", "Mustard Oil 1L", "Groundnut Oil 1L", "Coconut Oil 1L",
            "Olive Oil 500ml", "Rice Bran Oil 1L", "Sesame Oil 500ml", "Ghee 1kg",
            # Spices
            "Turmeric Powder 200g", "Red Chilli Powder 200g", "Coriander Powder 200g",
            "Cumin Powder 100g", "Garam Masala 100g", "Sambar Masala 100g",
            "Biryani Masala 100g", "Chicken Masala 100g", "Kitchen King Masala",
            "Black Pepper 100g", "Cardamom 50g", "Cinnamon 100g", "Cloves 50g",
            # Tea & Coffee
            "Tea Powder 500g", "Tea Leaves Premium", "Green Tea 100 bags",
            "Coffee Powder 200g", "Instant Coffee 100g", "Filter Coffee Powder",
            # Sugar & Sweeteners
            "Sugar 2kg", "Sugar 5kg", "Brown Sugar 500g", "Jaggery 1kg",
            "Honey 500g", "Honey 1kg", "Organic Honey 250g",
            # Snacks
            "Namkeen Mixture 400g", "Bhujia 400g", "Chakli 300g", "Murukku 300g",
            "Chips 150g", "Biscuits Cream", "Biscuits Chocolate", "Cookies 300g",
            "Dry Fruits Mix 500g", "Almonds 250g", "Cashews 250g", "Raisins 250g",
            # Beverages
            "Mango Juice 1L", "Orange Juice 1L", "Mixed Fruit Juice 1L",
            "Soft Drink 2L", "Sparkling Water 1L",
            # Ready to Eat
            "Instant Noodles Pack", "Pasta 500g", "Vermicelli 500g", "Oats 1kg",
            "Breakfast Cereal 500g", "Cornflakes 500g", "Muesli 500g",
            # Sauces & Spreads
            "Tomato Ketchup 500g", "Mayonnaise 250g", "Peanut Butter 400g",
            "Jam Mixed Fruit 500g", "Pickle Mango 400g", "Pickle Mixed 400g",
        ]
    },
    "Sports & Fitness": {
        "price_range": (199, 9999),
        "products": [
            # Cricket
            "Cricket Bat English Willow", "Cricket Bat Kashmir Willow", "Cricket Ball Leather",
            "Cricket Ball Tennis", "Cricket Gloves", "Cricket Pads", "Cricket Helmet",
            "Cricket Kit Bag", "Cricket Stumps Set",
            # Badminton
            "Badminton Racket", "Badminton Racket Set", "Shuttlecock Feather", "Shuttlecock Nylon",
            "Badminton Net",
            # Football
            "Football Size 5", "Football Goal Net", "Football Shin Guards", "Football Gloves",
            # Tennis & TT
            "Tennis Racket", "Tennis Balls Pack", "Table Tennis Bat", "TT Balls Pack", "TT Table",
            # Gym Equipment
            "Dumbbell Set", "Dumbbell 5kg Pair", "Dumbbell 10kg Pair", "Kettlebell",
            "Barbell Set", "Weight Plates", "Resistance Bands Set", "Pull Up Bar",
            "Ab Roller", "Push Up Board", "Skipping Rope", "Hand Gripper",
            # Yoga
            "Yoga Mat 6mm", "Yoga Mat 8mm", "Yoga Block", "Yoga Strap", "Yoga Wheel",
            "Foam Roller", "Acupressure Mat",
            # Cycling
            "Bicycle Adult", "Bicycle Kids", "Cycling Helmet", "Cycling Gloves",
            "Bicycle Lock", "Bicycle Pump", "Bottle Cage",
            # Swimming
            "Swimming Goggles", "Swimming Cap", "Swim Shorts", "Swimsuit Women",
            "Ear Plugs Swimming", "Kickboard",
            # Outdoor
            "Camping Tent 2 Person", "Camping Tent 4 Person", "Sleeping Bag", "Hiking Backpack",
            "Trekking Pole", "Torch Rechargeable", "Binoculars", "Compass",
            # Protective Gear
            "Knee Cap", "Ankle Support", "Wrist Support", "Back Support Belt",
            # Other Sports
            "Carrom Board", "Chess Board", "Frisbee", "Volleyball", "Basketball",
        ]
    },
    "Toys & Baby": {
        "price_range": (149, 4999),
        "products": [
            # Baby Care
            "Baby Diaper Pack S", "Baby Diaper Pack M", "Baby Diaper Pack L", "Baby Diaper Pack XL",
            "Baby Wipes", "Baby Powder", "Baby Oil", "Baby Lotion", "Baby Shampoo",
            "Baby Soap", "Diaper Rash Cream",
            # Feeding
            "Baby Bottle 250ml", "Baby Bottle Set", "Sipper Cup", "Feeding Spoon Set",
            "Breast Pump Manual", "Breast Pump Electric", "Sterilizer", "Bottle Warmer",
            "Baby Food Maker",
            # Baby Gear
            "Baby Stroller", "Baby Carrier", "Baby Walker", "Baby Bouncer", "Baby Swing",
            "Car Seat Baby", "Baby Crib", "Baby Bedding Set", "Baby Blanket",
            "Baby Mosquito Net",
            # Baby Clothes
            "Baby Romper", "Baby Dress", "Baby T-shirt Pack", "Baby Pajama Set",
            "Baby Bib Set", "Baby Cap Set", "Baby Mittens Set", "Baby Booties",
            # Educational Toys
            "Building Blocks 100pc", "Building Blocks 200pc", "STEM Kit", "Science Kit",
            "Alphabet Puzzle", "Number Puzzle", "Shape Sorter", "Stacking Rings",
            "Abacus", "Globe Educational", "Flash Cards Set",
            # Action & Dolls
            "Action Figure Superhero", "Action Figure Set", "Doll Set", "Barbie Doll",
            "Kitchen Playset", "Doctor Playset", "Tool Kit Toy",
            # Vehicles
            "Remote Control Car", "Remote Control Helicopter", "Train Set", "Die Cast Cars Set",
            "Ride-on Car", "Bicycle Kids 16 inch", "Tricycle",
            # Board Games
            "Monopoly", "Scrabble", "Ludo", "Snakes and Ladders", "Jenga", "UNO Cards",
            "Chess Set", "Carrom Board Kids",
            # Outdoor Toys
            "Swing Set", "Slide Kids", "Ball Pit", "Sandbox", "Bubbles Set",
            # Soft Toys
            "Teddy Bear", "Teddy Bear Giant", "Soft Toy Bunny", "Soft Toy Elephant",
            "Baby Rattle Set", "Musical Toy",
        ]
    },
    "Automotive": {
        "price_range": (149, 14999),
        "products": [
            # Car Interior
            "Car Seat Cover Set", "Car Seat Cover Leather", "Steering Wheel Cover",
            "Dashboard Mat", "Gear Knob Cover", "Handbrake Cover", "Floor Mat Set",
            "Car Cushion Lumbar", "Neck Pillow Car",
            # Car Exterior
            "Car Cover", "Car Cover Waterproof", "Mud Flaps", "Door Guard", "Bumper Guard",
            "Roof Rack", "Car Antenna",
            # Car Care
            "Car Shampoo", "Car Polish", "Car Wax", "Glass Cleaner", "Dashboard Polish",
            "Tyre Shine", "Scratch Remover", "Car Perfume", "Car Air Freshener",
            "Microfiber Cloth Set", "Chamois Leather", "Car Duster",
            # Car Electronics
            "Car Charger", "Car Charger Fast", "Phone Holder Magnetic", "Phone Holder Vent",
            "Dash Cam 1080p", "Dash Cam 4K", "Reverse Camera", "Parking Sensor Kit",
            "Car Bluetooth Kit", "FM Transmitter", "Car Speaker Set", "Subwoofer Car",
            # Car Tools
            "Tyre Inflator", "Jump Starter", "Car Vacuum Cleaner", "Car Tool Kit",
            "Puncture Repair Kit", "Tow Rope", "First Aid Kit Car", "Fire Extinguisher Car",
            # Bike Accessories
            "Bike Helmet Full Face", "Bike Helmet Half Face", "Bike Helmet Open Face",
            "Riding Jacket", "Riding Gloves", "Riding Boots", "Knee Guards", "Elbow Guards",
            "Bike Cover", "Bike Lock", "Bike Phone Holder", "Tank Bag",
            "Bike Mirror", "Bike Grip", "Bike LED Light",
            # Maintenance
            "Engine Oil 1L", "Engine Oil 4L", "Brake Fluid", "Coolant 1L",
            "Battery Car", "Battery Bike", "Spark Plug",
        ]
    },
    "Mobile Accessories": {
        "price_range": (99, 3999),
        "products": [
            # Cases & Covers
            "Phone Case Clear", "Phone Case Rugged", "Phone Case Leather", "Phone Case Silicone",
            "Phone Case Designer", "Phone Case Wallet", "Phone Case Armor",
            "Back Cover Soft", "Back Cover Hard", "Bumper Case",
            # Screen Protection
            "Tempered Glass", "Tempered Glass Privacy", "Screen Protector Matte",
            "Camera Lens Protector", "Full Coverage Screen Guard",
            # Chargers
            "Charger 18W", "Charger 33W", "Charger 65W", "Charger 120W",
            "Wireless Charger Pad", "Wireless Charger Stand", "Car Charger 20W",
            "Car Charger Dual", "Travel Adapter",
            # Cables
            "USB C Cable 1m", "USB C Cable 2m", "Lightning Cable", "Micro USB Cable",
            "Cable 3-in-1", "Braided Cable", "Fast Charging Cable",
            # Power Banks
            "Power Bank 10000mAh", "Power Bank 20000mAh", "Power Bank 30000mAh",
            "Power Bank Slim", "Power Bank Solar", "Power Bank Wireless",
            # Audio
            "Earphones Wired", "Earphones Type C", "TWS Earbuds Budget", "TWS Earbuds Premium",
            "Neckband Wireless", "Headphones Over-Ear", "Gaming Earphones",
            "Earbuds Case", "Ear Tips Replacement",
            # Holders & Stands
            "Phone Stand Desktop", "Phone Stand Adjustable", "Tripod Phone", "Ring Holder",
            "Pop Socket", "Car Mount Vent", "Car Mount Dashboard", "Bike Phone Mount",
            # Storage
            "Memory Card 32GB", "Memory Card 64GB", "Memory Card 128GB", "Memory Card 256GB",
            "OTG Adapter", "Card Reader",
            # Camera Accessories
            "Selfie Stick", "Selfie Stick with Tripod", "Ring Light", "Gimbal Phone",
            "Lens Kit Phone", "Microphone Phone",
            # Gaming
            "Game Controller Phone", "Trigger Phone", "Cooling Fan Phone",
            # Cleaning
            "Screen Cleaning Kit", "Cleaning Cloth",
        ]
    },
    "Books & Stationery": {
        "price_range": (49, 1999),
        "products": [
            # Fiction
            "Novel Bestseller", "Fiction Thriller", "Fiction Romance", "Fiction Mystery",
            "Classic Literature", "Short Stories Collection", "Poetry Collection",
            # Non-Fiction
            "Self Help Book", "Biography", "Autobiography", "Business Book",
            "Finance Book", "Leadership Book", "Motivational Book", "Spirituality Book",
            # Academic
            "NCERT Class 10 Set", "NCERT Class 12 Set", "JEE Preparation Book",
            "NEET Preparation Book", "UPSC Preparation Set", "SSC Preparation Book",
            "CAT Preparation Book", "GRE Preparation Book",
            "Engineering Textbook", "Medical Textbook", "Law Book",
            # Children
            "Picture Book Kids", "Story Book Kids", "Activity Book", "Coloring Book",
            "Fairy Tales Collection", "Comics", "Encyclopedia Kids",
            # Language Learning
            "English Grammar Book", "Hindi Learning Book", "French Learning Book",
            "German Learning Book", "Dictionary English", "Thesaurus",
            # Notebooks
            "Notebook Ruled A4", "Notebook A5 Pack", "Spiral Notebook", "Long Book",
            "Register 200 Pages", "Diary 2025", "Planner 2025", "Journal",
            # Writing
            "Pen Set", "Ball Pen Pack 10", "Gel Pen Pack", "Fountain Pen",
            "Pencil Pack", "Mechanical Pencil Set", "Marker Set", "Highlighter Set",
            "Sketch Pen Set", "Color Pencil Set 24", "Crayon Set 24", "Oil Pastels",
            # Office Supplies
            "Stapler", "Punch Machine", "Paper Clips Box", "Binder Clips",
            "Sticky Notes", "File Folder Set", "Envelope Pack", "Tape Dispenser",
            "Scissors Office", "Glue Stick Pack", "Correction Pen",
            # Art Supplies
            "Watercolor Set", "Acrylic Paint Set", "Canvas Board Pack", "Paint Brushes Set",
            "Sketch Pad A3", "Drawing Book A4",
            # Bags
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


def generate_products():
    """Generate 1200+ products balanced across categories"""
    products = []
    sku_num = 1001
    
    # Target ~100 products per category
    for category, data in CATEGORIES.items():
        base_products = data["products"]
        price_range = data["price_range"]
        brands = BRANDS.get(category, ["Generic"])
        
        # Generate variations until we have ~100 products
        target_count = max(100, len(base_products))
        count = 0
        
        while count < target_count:
            for base in base_products:
                if count >= target_count:
                    break
                    
                # Add brand and variant
                brand = random.choice(brands)
                variant = random.choice(VARIANTS)
                
                # Some products get brand prefix, some don't
                if random.random() > 0.5:
                    name = f"{brand} {base}{variant}"
                else:
                    name = f"{base}{variant}"
                
                # Generate realistic price
                min_p, max_p = price_range
                price = round(random.uniform(min_p, max_p), 2)
                
                # Round to nice numbers sometimes
                if random.random() > 0.7:
                    price = round(price / 100) * 100 - 1  # e.g., 2999, 4999
                
                rating = round(random.uniform(3.5, 5.0), 1)
                reviews = random.randint(10, 15000)
                
                sku = f"IND{sku_num}"
                sku_num += 1
                
                products.append({
                    "sku": sku,
                    "name": name.strip(),
                    "category": category,
                    "current_price": max(price, min_p),  # Ensure min price
                    "rating": rating,
                    "reviews_count": reviews
                })
                count += 1
    
    return products


def clear_old_data(conn):
    """Clear old product data"""
    cursor = conn.cursor()
    print("🗑️  Clearing old product and inventory data...")
    try:
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("   ✅ Old data cleared")
    except Exception as e:
        print(f"   ⚠️ Warning: {e}")
        conn.rollback()


def insert_products(conn, products):
    """Insert products into database"""
    cursor = conn.cursor()
    print(f"\n📦 Inserting {len(products)} products...")
    
    batch_size = 100
    for i in range(0, len(products), batch_size):
        batch = products[i:i+batch_size]
        for p in batch:
            cursor.execute("""
                INSERT INTO products (sku, name, category, current_price, rating, reviews_count, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (sku) DO UPDATE SET
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    current_price = EXCLUDED.current_price,
                    rating = EXCLUDED.rating,
                    reviews_count = EXCLUDED.reviews_count
            """, (p["sku"], p["name"], p["category"], p["current_price"], p["rating"], p["reviews_count"]))
        conn.commit()
        print(f"   ✅ Inserted {min(i+batch_size, len(products))}/{len(products)} products")


def insert_inventory(conn, products):
    """Insert inventory across warehouses"""
    cursor = conn.cursor()
    print(f"\n🏪 Adding inventory across {len(WAREHOUSES)} warehouses...")
    
    batch_size = 500
    total = len(products) * len(WAREHOUSES)
    count = 0
    
    for p in products:
        for warehouse in WAREHOUSES:
            # Mumbai has more stock
            if warehouse == "Mumbai Warehouse":
                qty = random.randint(50, 500)
            else:
                qty = random.randint(10, 200)
            
            cursor.execute("""
                INSERT INTO inventory (sku, location, quantity, last_updated)
                VALUES (%s, %s, %s, NOW())
                ON CONFLICT (sku, location) DO UPDATE SET 
                    quantity = EXCLUDED.quantity,
                    last_updated = NOW()
            """, (p["sku"], warehouse, qty))
            count += 1
        
        if count % batch_size == 0:
            conn.commit()
            print(f"   ✅ Inserted {count}/{total} inventory entries")
    
    conn.commit()
    print(f"   ✅ Inserted {count}/{total} inventory entries")


def main():
    print("\n" + "="*60)
    print("🚀 POPULATING 1200+ INDIAN PRODUCTS")
    print("="*60)
    
    conn = get_db()
    
    # Clear old data
    clear_old_data(conn)
    
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
    insert_products(conn, products)
    
    # Insert inventory
    insert_inventory(conn, products)
    
    # Final counts
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    prod_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM inventory")
    inv_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    cust_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*60)
    print("🎉 DATABASE POPULATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n   📦 Products: {prod_count}")
    print(f"   🏪 Inventory entries: {inv_count}")
    print(f"   👥 Customers: {cust_count}")
    print(f"   🏭 Warehouses: {len(WAREHOUSES)}")
    print(f"   📁 Categories: {len(CATEGORIES)}")
    print()


if __name__ == "__main__":
    main()
