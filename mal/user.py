import csv
import time
import logging
from typing import List
from mal.mal import get_mal, BASE_URL, TOKEN
from dataclasses import dataclass
from requests.exceptions import HTTPError
from mal.useragents import get_useragent


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")


ANIMELISTS_CSV = "/home/battos/Projects/AniReco/data/animelists.csv"


@dataclass
class Anime:
    id: int
    title: str


@dataclass
class User:
    username: str


@dataclass
class AnimeListItem:
    user: User
    anime: Anime
    status: str
    score: int


@dataclass
class AnimeList:
    user: User
    anime_list: List[AnimeListItem]

    def __add__(self, other):
        if not isinstance(other, AnimeList):
            raise ValueError
        if self.user.username != other.user.username:
            raise ValueError
        new_animelist = AnimeList(user=self.user)
        new_anime_list = self.anime_list + other.anime_list
        new_animelist.anime_list = new_anime_list
        return new_animelist

    def filter_by_status(self, status: str):
        filtered_anime_list = []
        for item in self.anime_list:
            if item.status == status:
                filtered_anime_list.append(item)
        return AnimeList(user=self.user, anime_list=filtered_anime_list)

    def only_wathced(self):
        data = []
        watched = self.filter_by_status("completed")
        for ani in watched.anime_list:
            if ani.score == 0:
                continue
            data.append(ani)
        return AnimeList(user=self.user, anime_list=data)


def get_user_animelist(username: str,
                       limit: int = 100) -> AnimeList:
    global TOKEN
    url = BASE_URL + f'/users/{username}/animelist'
    params = {
        'fields': 'list_status,score',
        'limit': limit,
        'nsfw': 'true',
    }
    headers = {
        "User-Agent": get_useragent(),
    }
    data = []
    error_counter = 0
    while True:
        try:
            response = get_mal(url=url,
                               access_token=TOKEN,
                               params=params,
                               extra_headers=headers)
            data += response["data"]
            if 'next' not in response["paging"]:
                break
            url = response['paging']['next']
        except HTTPError as err:
            # TODO if there is a error, make it wait on another thread so others dont wait (? idk if it will work)
            logging.error(str(err))
            if err.response.status_code == 429:
                logging.info("Too many requests. Sleeping 5 mins.")
                time.sleep(5*60)
            # logging.info("Propably because of too many requests, going to sleep for 1 minutes")
            error_counter += 1
            if error_counter == 2:
                logging.warning("Repeated error. Skipping user.")
                return
            # time.sleep(1*60)
            time.sleep(1)
            continue
        except KeyError as err:
            logging.error(f"Key error: {str(err)}")
            print(response)
            logging.info("Sleeping 5 mins.")
            time.sleep(5*60)
            return
    user = User(username=username)
    anime_list = []
    for d in data:
        node = d['node']
        list_status = d['list_status']
        anime = Anime(id=node['id'],
                      title=node['title'])
        list_item = AnimeListItem(user=user,
                                  anime=anime,
                                  status=list_status['status'],
                                  score=list_status['score'])
        anime_list.append(list_item)
    animelist = AnimeList(user=user, anime_list=anime_list)
    return animelist.only_wathced()


def write_animelist_to_new_csv(animelist: AnimeList, filename: str):
    with open(filename, "w", newline='', encoding='utf-8') as csv_file:
        fieldnames = ['username', 'anime_id', 'anime_title', 'score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in animelist.anime_list:
            row = {
                'username': item.user.username,
                'anime_id': item.anime.id,
                'anime_title': item.anime.title,
                'score': item.score,
            }
            writer.writerow(row)

def add_to_csv(filename: str, animelist: AnimeList):
    with open(filename, "a", newline='', encoding='utf-7') as csv_file:
        fieldnames = ['username', 'anime_id', 'anime_title', 'score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for item in animelist.anime_list:
            row = {
                'username': item.user.username,
                'anime_id': item.anime.id,
                'anime_title': item.anime.title,
                'score': item.score,
            }
            writer.writerow(row)

def get_userlists_and_write_to_csv(users_filepath: str, csv_filepath: str):
    users = []
    with open(users_filepath, "r") as users_file:
        users = users_file.read().split(",")
    for user in users:
        try:
            animelist = get_user_animelist(username=user, limit=250)
            add_to_csv(filename=csv_filepath, animelist=animelist)
        except Exception as e:
            logging.error(str(e))