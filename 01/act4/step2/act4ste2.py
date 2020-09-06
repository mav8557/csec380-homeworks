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

def check(hostname: str, port: int) -> bool:
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
        "https": f"https://{hostname}:{port}",
    }

    try:
        req = requests.get("http://ifconfig.me", proxies=proxies, timeout=60)
    except requests.exceptions.ProxyError:
        return False
    except :
        # TODO: maybe rerun with longer timeout?
        return False

    return req.status_code == 200

def main():
    """
    Grab command line arguments and start scanning for proxies
    """
    parser = argparse.ArgumentParser(description="Anonymous Proxy Scanner")
    # args.add_argument("-r", "--range", required=True, help="IP range to run on")
    args = parser.parse_args()
    if check("176.56.107.198", 35186):
        print("Working Proxy")


if __name__ == "__main__":
    main()
