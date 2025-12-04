def generate_unique_sku(product, faker):
    category = product['category'][:3]
    random_id = faker.unique.random_number(digits=6)
    return f"{category}-{random_id}".upper()