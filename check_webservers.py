#!/usr/bin/env python3
#######################################################################################################
############################################ BEGIN IMPORTS ############################################
#######################################################################################################
# Import sys module for interacting with command line arguments and other system functionality
import sys
# Import requests module for sending HTTP requests
import requests
#######################################################################################################
########################################### BEGIN FUNCTIONS ###########################################
#######################################################################################################
# Defines a function, read_servers, that takes one argument (file_path). file_path is expected to be a 
# string (e.g. "/usr/local/nagios/etc/webserver_list.txt"). The purpose of this function is to open a
# file and read each line (removing leading and trailing whitespace), ignoring empty lines, returning
# a list of clean, non-empty lines.
def read_servers(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]
# Defines a function, check_server_status, that takes two arguments url, and timeout. url is the URL
# that the function will test while timeout, optional, defines how long to wait for a response
# default (3 seconds). The purpose of this function is to test if a webserver is up using an HTTP request.
def check_server_status(url, timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False
# Defines a function, main. The purpose of this function is to run the actual server checks.
def main():
    # Ensures a file path was passed in (Script Name/Path = 2)
    if len(sys.argv) !=2:
        print("UNKNOWN - Usage: check_webservers.py <server_list.txt.")
        sys.exit(3)
    # Sets server_file to the argument file path.
    server_file = sys.argv[1]
    servers = read_servers(server_file)
    # Checks for servers that are offline and adds to the offline list.
    offline = []
    for server in servers:
        if not check_server_status(server):
            offline.append(server)
    total = len(servers)
    down = len(offline)
    # Test if any/all or no servers are down and prints.
    if down == total:
        print(f"CRITICAL - ALL {total} web servers are offline: {', '.join(offline)}")
        sys.exit(2)
    elif down > 0:
        print(f"WARNING - {down}/{total} web servers are offline: {', '.join(offline)}")
        sys.exit(1)
    else:
        print(f"OK - All {total} web servers are online")
        sys.exit(0)
# Calls main if executed from main.
if __name__ == "__main__":
    main()