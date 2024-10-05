#!/usr/bin/env python3
import requests
import json

def get_headers(auth_email, auth_key):
    return {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json",
    }

def get_zone_id(auth_email, auth_key, domain):
    url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"
    headers = get_headers(auth_email, auth_key)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        handle_error(response)
        return None
    else:
        return response.json()["result"][0]["id"]

def get_record_id(auth_email, auth_key, domain, hostname):
    zone_id = get_zone_id(auth_email, auth_key, domain)
    if zone_id is None:
        return None
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={hostname}.{domain}"
    headers = get_headers(auth_email, auth_key)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        handle_error(response)
        return None
    else:
        return response.json()["result"][0]["id"]

def update_dns_record(auth_email, auth_key, domain, hostname):
    zone_id = get_zone_id(auth_email, auth_key, domain)
    record_id = get_record_id(auth_email, auth_key, domain, hostname)
    if zone_id is not None and record_id is not None:
        new_ip = requests.get('https://api.ipify.org').text
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        headers = get_headers(auth_email, auth_key)
        data = {
            "type": "A",
            "name": hostname,
            "content": new_ip,
            "ttl": 1,
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            handle_error(response)
        else:
            print("DNS record updated successfully")   
            print("FQDN:" + hostname + "." + domain) 
            print("IP:  "+ new_ip )

def handle_error(response):
    error_message = response.json()['errors'][0]['message']
    print(f"Error: {error_message}")

if __name__ == "__main__":
    # CUSTOMIZE THESE VARIABLES --- START --- !!! 
    auth_email = "test@test.com"
    auth_key = "vc1t2419kt25e9gur0df4n73frkae2a4id4ej"
    domain = "sample-domain.com"
    hostname = "servername"
    # CUSTOMIZE THESE VARIABLES ---  END --- !!! 

    print(f"Updating DNS record: {hostname}.{domain}")
    update_dns_record(auth_email, auth_key, domain, hostname)
