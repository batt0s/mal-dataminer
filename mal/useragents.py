import random

USERAGENTS = "/home/battos/Projects/AniReco/mal/useragents.txt"

def get_useragent() -> str:
    with open(USERAGENTS, "r") as file:
        useragents = file.readlines()
    return random.choice(useragents).strip()