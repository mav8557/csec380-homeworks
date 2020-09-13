"""
Anonymous Proxy Scanner
Scans IP ranges for working anonymous proxies

course: CSEC-380 Principles of Web Application Security
author: Michael Vaughan
"""

# Imports
import argparse
import netaddr
import requests
import sys

def check(hostname: str, port: int, myip: str) -> bool:
    """
    Check a given hostname and port to see if there is
    an anonymous proxy running.

    @args

    hostname: the IP or DNS hostname of the target host
    port: the TCP port to connect to

    @return
    Returns True if there is an anonymous proxy
    at that hostname and port. False otherwise.
    """
    proxies = {
        "http": f"http://{hostname}:{port}",
    }

    try:
        req = requests.get("http://ifconfig.me", proxies=proxies, timeout=4)
    except requests.exceptions.ProxyError:
        return False
    except :
        return False

    return req.status_code == 200 and req.text == hostname

def main():
    """
    Grab command line arguments and start scanning for proxies
    """
    parser = argparse.ArgumentParser(description="Anonymous Proxy Scanner")
    parser.add_argument("-r", "--range", required=True, help="IP range to run on")
    args = parser.parse_args()

    myip = requests.get("http://ifconfig.me").text

    try:
        begin, end = args.range.split('-')
    except ValueError:
        print("Enter a range like so: <IP1>-<IP2>, ex: 10.0.0.1-10.0.1.0", file=sys.stderr)
        exit(1)

    begin, end = netaddr.IPAddress(begin), netaddr.IPAddress(end)
    for ip in range(int(begin), int(end)+1):
        print("Testing..", netaddr.IPAddress(ip))
        for port in [80,8080,8000,3128]:
            if check(str(netaddr.IPAddress(ip)), port, myip):
                print(f"WORKING: {netaddr.IPAddress(ip)}:{port}")


if __name__ == "__main__":
    main()
