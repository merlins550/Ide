import pandas as pd
import numpy as np
import random

# Set a seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define parameters for data generation
num_users = 100
num_products = 50
num_ratings = 1000

product_categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports']
product_descriptions_templates = {
    'Electronics': ["High-performance {product_name} with advanced features.", "Compact and portable {product_name} for everyday use.", "Innovative {product_name} with smart connectivity."],
    'Books': ["Bestselling {product_name} by a renowned author.", "Classic {product_name} for avid readers.", "Engaging {product_name} that explores deep themes."],
    'Clothing': ["Comfortable and stylish {product_name} for all seasons.", "Durable {product_name} made from premium materials.", "Trendy {product_name} to elevate your wardrobe."],
    'Home & Kitchen': ["Essential {product_name} for modern kitchens.", "Versatile {product_name} to simplify home tasks.", "Elegant {product_name} to enhance your living space."],
    'Sports': ["Professional-grade {product_name} for peak performance.", "Lightweight {product_name} for outdoor adventures.", "Ergonomic {product_name} designed for comfort."]
}

# Generate user and product IDs
user_ids = [f'user_{i+1}' for i in range(num_users)]
product_ids = [f'product_{i+1}' for i in range(num_products)]

# Generate product details
product_details = []
for i in range(num_products):
    product_id = f'product_{i+1}'
    category = random.choice(product_categories)
    product_name = f'Item {i+1}'
    description = random.choice(product_descriptions_templates[category]).format(product_name=product_name)
    product_details.append({'product_id': product_id, 'product_category': category, 'product_description': description})

products_df = pd.DataFrame(product_details)

# Generate ratings
ratings_data = []
for _ in range(num_ratings):
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    rating = random.randint(1, 5)
    ratings_data.append({'user_id': user_id, 'product_id': product_id, 'rating': rating})

ratings_df = pd.DataFrame(ratings_data)

# Merge ratings with product details to get a complete dataset
df = pd.merge(ratings_df, products_df, on='product_id', how='left')

# Save to CSV
df.to_csv('simulated_data.csv', index=False)

print("Simulated data generated and saved to simulated_data.csv")