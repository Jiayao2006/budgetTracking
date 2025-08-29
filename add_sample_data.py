import requests
import json
from datetime import datetime, timedelta

# Sample spending data
sample_data = [
    {"amount": 25.50, "date": "2025-08-29", "category": "Food", "location": "McDonald's", "description": "Lunch"},
    {"amount": 120.00, "date": "2025-08-29", "category": "Groceries", "location": "Walmart", "description": "Weekly groceries"},
    {"amount": 45.75, "date": "2025-08-28", "category": "Transportation", "location": "Gas Station", "description": "Gas for car"},
    {"amount": 15.99, "date": "2025-08-28", "category": "Entertainment", "location": "Netflix", "description": "Monthly subscription"},
    {"amount": 89.99, "date": "2025-08-27", "category": "Shopping", "location": "Amazon", "description": "Books and supplies"},
    {"amount": 12.50, "date": "2025-08-27", "category": "Food", "location": "Starbucks", "description": "Coffee"},
    {"amount": 200.00, "date": "2025-08-26", "category": "Bills", "location": "Electric Company", "description": "Monthly electric bill"},
    {"amount": 35.00, "date": "2025-08-26", "category": "Food", "location": "Pizza Hut", "description": "Dinner"},
    {"amount": 67.45, "date": "2025-08-25", "category": "Groceries", "location": "Target", "description": "Household items"},
    {"amount": 8.99, "date": "2025-08-25", "category": "Entertainment", "location": "Spotify", "description": "Music subscription"}
]

def add_sample_data():
    base_url = "http://localhost:8000"
    
    for item in sample_data:
        try:
            response = requests.post(f"{base_url}/spendings/", json=item)
            if response.status_code == 200:
                print(f"✓ Added: ${item['amount']} at {item['location']}")
            else:
                print(f"✗ Failed to add: {item['location']} - {response.status_code}")
        except Exception as e:
            print(f"✗ Error adding {item['location']}: {e}")

if __name__ == "__main__":
    print("Adding sample spending data...")
    add_sample_data()
    print("Done!")
