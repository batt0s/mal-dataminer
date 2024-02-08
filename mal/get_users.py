import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from typing import List
import time


USERS_URL = "https://myanimelist.net/users.php"
USERS_FILE = "/home/battos/Projects/AniReco/mal/user_crawler/users.txt"


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url=url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_users(soup: BeautifulSoup) -> List[str]:
    def get_user(a_tag) -> str:
        href = a_tag.get('href')
        if href and '/profile/' in href:
            username = a_tag.text
            return username
        else:
            return ''
    
    users = []
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        username = get_user(a_tag)
        users.append(username)
    return list(filter(None, users))

def add_username_to_file(filepath: str, username: str):
    try:
        with open(filepath, 'r') as f:
            users = set(f.read().split(","))
            
        if username in users:
            return
        
        with open(filepath, 'a') as f:
            f.write(username + ",")
    except Exception as e:
        print(f"Hata: {e}")

def add_users_to_file(filepath: str, users: List[str]):
    for username in users:
        add_username_to_file(filepath=filepath,
                             username=username)

def crawl_users(url: str, filepath: str, iteration: int):
    for i in range(iteration):
        try:
            soup = get_soup(url=url)
        except HTTPError as err:
            print(f"There is an error: {str(err)}")
            if err.response.status_code in [405, 429]:
                print("Going to sleep for 1min.")
                time.sleep(60)
            else:
                continue
        users = get_users(soup=soup)
        add_users_to_file(filepath=filepath,
                          users=users)
        print(f"Completed iteration {i}")
        time.sleep(1)