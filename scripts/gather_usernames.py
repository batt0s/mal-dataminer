from mal.get_users import crawl_users

USERS_URL = "https://myanimelist.net/users.php"
USERS_FILE = "users.txt"

crawl_users(url=USERS_URL, filepath=USERS_FILE, iteration=1)