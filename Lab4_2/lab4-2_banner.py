#!/usr/bin/env python3
# lab4-2_banner.py
import socket, sys, json, time

def grab_banner_tcp(host, port, timeout=2.0, send_bytes=None, read_size=1024):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    banner = ""
    try:
        s.connect((host, port))
        if send_bytes:
            s.sendall(send_bytes)
        try:
            data = s.recv(read_size)
            banner += data.decode(errors='replace')
        except socket.timeout:
            pass
        s.close()
        return True, banner.strip()[:1000]
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python lab2_banner.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    # Common probes for HTTP-like services (HTTP/1.0 simple request)
    probes = {
        "generic": None,
        "http_get": b"GET / HTTP/1.0\r\nHost: example\r\n\r\n",
        "smtp_helo": b"HELO example.com\r\n",
        "ssh": None
    }

    # try HTTP first
    ok, banner = grab_banner_tcp(host, port, send_bytes=probes["http_get"])
    if ok and banner:
        print("Banner (HTTP probe):")
        print(banner)
    else:
        ok, banner = grab_banner_tcp(host, port, send_bytes=probes["smtp_helo"])
        if ok and banner:
            print("Banner (SMTP probe):")
            print(banner)
        else:
            ok, banner = grab_banner_tcp(host, port, send_bytes=probes["generic"])
            print("Generic probe result:")
            print(banner)

    service = ""
    if port == 22:
        service = "SSH"
    elif port == 80:
        service = "HTTP"
    elif port == 443:
        service = "HTTPS"
    elif port == 25 or port == 465 or port == 587:
        service = "SMTP"

    with open("banners.csv", "a") as f:
        banner_part = banner.split("\n")
        f.write(f"\n{host},{port},{service},{banner_part[0]}")