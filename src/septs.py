#/usr/bin/python3

import os
import sys 

services = []

logo = r"""                                                                                
         ______       ______        _____    _________________          ______  
     ___|\     \  ___|\     \   ___|\    \  /                 \     ___|\     \ 
    |    |\     \|     \     \ |    |\    \ \______     ______/    |    |\     \
    |    |/____/||     ,_____/||    | |    |   \( /    /  )/       |    |/____/|
 ___|    \|   | ||     \--'\_|/|    |/____/|    ' |   |   '     ___|    \|   | |
|    \    \___|/ |     /___/|  |    ||    ||      |   |        |    \    \___|/ 
|    |\     \    |     \____|\ |    ||____|/     /   //        |    |\     \    
|\ ___\|_____|   |____ '     /||____|           /___//         |\ ___\|_____|   
| |    |     |   |    /_____/ ||    |          |`   |          | |    |     |   
 \|____|_____|   |____|     | /|____|          |____|           \|____|_____|   
    \(    )/       \( |_____|/   \(              \(                \(    )/     
     '    '         '    )/       '               '                 '    '      
                         '                                                      

Super Easy Pentest Script || Version 1.01
"""

if sys.argv[1] == "-h":
    print("Usage: python septs.py <host>")
    print("Options:")
    print("-h: show this help menu")
    print("-v: show version")
    sys.exit(0)
elif sys.argv[1] == "-v":
    print("Version 1.01")
    sys.exit(0)
elif sys.argv[1] == None:
    print("Usage: python septs.py <host>")
    sys.exit(0)
host = sys.argv[1]

def nmap():
    print("[*] Running nmap...")
    os.system("nmap -sV -sC -oN nmap.txt " + host + " >/dev/null")
    print("[*] saved nmap scan to nmap.txt")
    parse()

def parse():
    ports = []
    print("[*] Parsing nmap scan...")
    with open("nmap.txt", "r") as f:
        for line in f:
            if line =="Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn":
                print("[*] Host seems down. Exiting...")
                sys.exit(0)
            elif "open" in line:
                service = line.split("/")[1]
                print("[*] Found open port: " + line.split("/")[0], service)
                ports.append(line.split("/")[0])
    f.close()
    search_for_services(None,None)

def search_for_services(http_done, samba_done):
    # check is the services list is empty
    found_http = False
    found_samba = False
    if services == []:
        with open("nmap.txt", "r") as f:
            for line in f:
                if found_http == True:
                    continue
                if found_samba == True:
                    continue
                else:
                    if "http" in line:
                        print("[*] Found http service")
                        found_http = True
                        services.append("http")
                    if "smb" in line:
                        print("[*] Found samba service")
                        found_samba = True
                        services.append("samba")
        f.close()
    # make sure that each service is only run once
    for x in services:
        if x == "http" and http_done == None:
            http()
            http_done = True
        if x == "samba" and samba_done == None:
            samba()
            samba_done = True

def samba():
    # find samba shares
    print("[*] Running enum4linux...")
    os.system("enum4linux -a " + host + " > enum4linux.txt")
    print("[*] saved enum4linux scan to enum4linux.txt")
    print("[*] Parsing enum4linux scan...")
    with open("enum4linux.txt", "r") as f:
        for line in f:
            if "Disk" in line:
                print("[*] Found share: " + line.split(" ")[1])
    f.close()

        
def check_tools():
    print("[*] Checking for tools...")
    if os.path.isfile("/usr/bin/gobuster"):
        print("[*] Gobuster found")
    else:
        print("[*] Gobuster not found")
        print("[*] Gobuster can be installed with: apt install gobuster")
        print("[*] Exiting...")
        sys.exit(0)
    if os.path.isfile("/usr/bin/nmap"):
        print("[*] Nmap found")
    else:
        print("[*] Nmap not found")
        print("[*] Nmap can be installed with: apt install nmap")
        print("[*] Exiting...")
        sys.exit(0)
    if os.path.isfile("/usr/bin/enum4linux"):
        print("[*] Enum4linux found")
    else:
        print("[*] Enum4linux not found")
        print("[*] Enum4linux can be installed with: apt install enum4linux")
        print("[*] Exiting...")
        sys.exit(0)
    if os.path.isfile("/usr/bin/hydra"):
        print("[*] Hydra found")
    else:
        print("[*] Hydra not found")
        print("[*] Hydra can be installed with: apt install hydra")
        print("[*] Exiting...")
        sys.exit(0)
    print("[*] All tools found")
    nmap()

def http():
    print("[*] finding wordlist...")
    check_wordlist_exists()
    print("[*] Running gobuster...")
    os.system("gobuster dir -u " + host + " -w /usr/share/wordlists/dirb/common.txt -o gobuster.txt > /dev/null")
    print("[*] saved gobuster scan to gobuster.txt")
    print("[*] Parsing gobuster scan...")
    gobuster_parser()
    search_for_services(True, None)


def gobuster_parser():
    found_directory = []
    with open("gobuster.txt", "r") as f:
        for line in f:
            if "--> " in line:
                print("[*] Found directory: " + line.split(" ")[0])
                found_directory.append(line.split(" ")[0])
    f.close()
    return

def search_directory(found_directory):
    print("[*] checking for intresting things ... ")
    for x in found_directory:
        os.system("curl " + host + x + " > " + x + ".txt")
        with open(x + ".txt", "r") as f:
            if "login" in f:
                print("[*] Found login page: " + x)
                brute_force_login(x)

def brute_force_login(x):
   print("[*] would you like to do a dictionary attack? or a brute force attack?")
   print("[*] 1. Dictionary attack")
   print("[*] 2. Brute force attack")
   what_to_do = input("[*] Enter your choice: ")
   if what_to_do == "1":
        print("[*] todo")
   elif what_to_do == "2":
        print("[*]todo")
   else:
        os.system("clear")
        print("[*] Invalid choice")
        brute_force_login(x)


def check_wordlist_exists():
    notFound = False
    if os.path.isfile("/usr/share/wordlists/dirb/common.txt"):
        print("[*] Wordlist found")
        print("[*] Starting gobuster scan...")
    else:
        print("[*] Wordlist not found")
        print("[*] Downloading wordlist...")
        os.system("wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt > /dev/null")
        notFound = True



def main():
    print(logo)
    print("-----------------------------")
    check_tools()

if __name__ == "__main__":
    main()



