import requests
r = requests.get("http://scanme.nmap.org")
print(r.status_code)