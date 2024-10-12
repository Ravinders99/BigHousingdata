import random
from faker import Faker
import json
from decimal import Decimal

# Initialize Faker for generating random data
fake = Faker()

# Regions and Provinces for Canadian housing
regions = ["Atlantic", "Central", "Prairies", "West Coast", "Northern"]
provinces = [
    "Nova Scotia", "Ontario", "Quebec", "British Columbia", 
    "Alberta", "Manitoba", "Saskatchewan", "Newfoundland and Labrador",
    "Prince Edward Island", "New Brunswick", "Yukon", "Nunavut", "Northwest Territories"
]

# Sample facilities
facilities_list = [
    "Hospital", "School", "University", "Supermarket", 
    "Community Center", "Shopping Mall", "Park", "Library"
]

# Function to generate random housing data
def generate_housing_data(num_entries=5):
    housing_entries = []
    for i in range(1, num_entries + 1):
        entry = {
            "population": random.randint(1000, 100000),  # Random population size
            "housing_size": random.randint(800, 4000),   # Housing size in square feet
            "area": round(random.uniform(10.0, 100.0), 2),  # Area in square kilometers
            "region": random.choice(regions),
            "province": random.choice(provinces),
            "latitude": float(fake.latitude()),  # Make sure latitude is float
            "longitude": float(fake.longitude()),  # Make sure longitude is float
            "area_population": random.randint(1000, 500000),  # Population of the surrounding area
            "facilities": random.sample(facilities_list, random.randint(2, 5))  # Random facilities
        }
        housing_entries.append(entry)
    return housing_entries

# Function to generate nested JSON structure with year range and increasing data entries per year
def generate_housing_json_structure(year_range, category, num_records_per_year):
    housing_data = {
        "prizes": []
    }
    
    for year in year_range:
        # Increase the number of housing entries as the year increases
        entries_per_prize = (year - min(year_range)) + 1  # Entries start at 1 for the first year, increase with each year
        
        for i in range(1, num_records_per_year + 1):
            prize_entry = {
                "year": str(year),
                "category": category,
                "id": f"{year}-{i}",
                "data": generate_housing_data(entries_per_prize)  # Increase entries as year increases
            }
            housing_data["prizes"].append(prize_entry)
    
    return housing_data

# Custom JSON encoder to handle non-serializable data types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)

# Define year range from 2014 to 2024
year_range = range(2014, 2025)

# Generate housing data with nested structure
# For example, we generate 500 prizes for each year
nested_housing_data = generate_housing_json_structure(year_range, "housing", 500)

# Save the generated data into a JSON file
with open('large_housing_data_with_years.json', 'w') as f:
    json.dump(nested_housing_data, f, indent=4, cls=CustomJSONEncoder)

print("Large housing data has been saved to large_housing_data_with_years.json")
