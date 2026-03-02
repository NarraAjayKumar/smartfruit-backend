import requests

def test_profile():
    base_url = "http://172.23.132.237:8000"
    
    print("--- SmartFruit AI Profile Validation ---")
    
    # 1. Test POST update
    print("Testing Profile Update...")
    data = {
        "name": "Validation Farmer",
        "avatar": "agriculture",
        "notificationsEnabled": "false"
    }
    r = requests.post(f"{base_url}/profile", data=data)
    if r.status_code == 200:
        print(f"  [SUCCESS] Updated: {r.json()['name']}")
    else:
        print(f"  [ERROR] Update failed: {r.status_code}")
        return

    # 2. Test GET fetch
    print("Testing Profile Fetch...")
    r = requests.get(f"{base_url}/profile")
    if r.status_code == 200:
        res = r.json()
        if res['name'] == "Validation Farmer":
            print(f"  [SUCCESS] Fetch verified: {res['name']}")
        else:
            print(f"  [ERROR] Data mismatch: {res['name']} != Validation Farmer")
    else:
        print(f"  [ERROR] Fetch failed: {r.status_code}")

if __name__ == "__main__":
    test_profile()
