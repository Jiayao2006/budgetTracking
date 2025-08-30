"""
Test script to verify spending endpoints work correctly
Run this locally to test the API
"""
import os
import sys
import requests
from datetime import date

# Add backend directory to path if script is run from project root
if os.path.exists("backend") and not os.path.exists("app"):
    os.chdir("backend")
    sys.path.insert(0, ".")

def test_spending_api():
    """Test the spending API endpoints"""
    
    # Configuration
    base_url = "http://localhost:8081"  # or your local server port
    admin_email = "admin@budgettracker.com"
    admin_password = "admin123"
    
    print(f"Testing API at: {base_url}")
    
    # Step 1: Login
    print("\n1. Testing login...")
    login_response = requests.post(f"{base_url}/api/auth/login", json={
        "email": admin_email,
        "password": admin_password
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token_data = login_response.json()
    token = token_data["access_token"]
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # Headers for authenticated requests
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test get spendings
    print("\n2. Testing get spendings...")
    get_response = requests.get(f"{base_url}/api/spendings", headers=headers)
    
    if get_response.status_code != 200:
        print(f"❌ Get spendings failed: {get_response.status_code}")
        print(f"Response: {get_response.text}")
    else:
        spendings = get_response.json()
        print(f"✅ Get spendings successful, count: {len(spendings)}")
    
    # Step 3: Test create spending
    print("\n3. Testing create spending...")
    test_spending = {
        "amount": 25.50,
        "category": "Food",
        "location": "Test Restaurant",
        "description": "Test spending from API test",
        "date": str(date.today())
    }
    
    create_response = requests.post(f"{base_url}/api/spendings", 
                                  json=test_spending, 
                                  headers=headers)
    
    if create_response.status_code not in [200, 201]:
        print(f"❌ Create spending failed: {create_response.status_code}")
        print(f"Response: {create_response.text}")
    else:
        new_spending = create_response.json()
        print(f"✅ Create spending successful, ID: {new_spending.get('id')}")
        print(f"   Amount: ${new_spending.get('amount')}, Location: {new_spending.get('location')}")
    
    # Step 4: Test dashboard
    print("\n4. Testing dashboard...")
    dashboard_response = requests.get(f"{base_url}/api/spendings/dashboard", headers=headers)
    
    if dashboard_response.status_code != 200:
        print(f"❌ Dashboard failed: {dashboard_response.status_code}")
        print(f"Response: {dashboard_response.text}")
    else:
        dashboard_data = dashboard_response.json()
        print(f"✅ Dashboard successful")
        print(f"   Total spending: ${dashboard_data.get('total_spending', 0)}")
        print(f"   Monthly transactions: {dashboard_data.get('monthly_transactions', 0)}")
    
    # Step 5: Test get spendings again to verify the new one is there
    print("\n5. Testing get spendings again...")
    get_response2 = requests.get(f"{base_url}/api/spendings", headers=headers)
    
    if get_response2.status_code == 200:
        spendings2 = get_response2.json()
        print(f"✅ Get spendings successful, new count: {len(spendings2)}")
        if len(spendings2) > len(spendings):
            print("✅ New spending was properly saved!")
        else:
            print("⚠️ New spending might not have been saved")
    
    print("\n🎉 API test completed!")

if __name__ == "__main__":
    test_spending_api()
