from mal.mal import get_mal, TOKEN, BASE_URL
from dataclasses import dataclass
from typing import List, Dict, Any
from requests.exceptions import HTTPError
import csv


@dataclass
class Anime:
    id: int
    title: str
    picture: str
    title_en: str
    title_ja: str
    start_date: str
    end_date: str
    synopsis: str
    mean_score: float
    rank: int
    popularity: int
    nsfw: bool
    media_type: str
    status: str
    genres: List[str]
    num_episodes: int
    source: str
    average_episode_duration_seconds: int
    rating: str
    studios: List[str]
    num_list_users: int
    num_scoring_users: int
    watching: int
    completed: int
    on_hold: int
    dropped: int
    plan_to_watch: int

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]):
        return cls(
            id=json_obj['id'],
            title=json_obj['title'],
            picture=json_obj['main_picture']['medium'],
            title_en=json_obj['alternative_titles']['en'],
            title_ja=json_obj['alternative_titles']['ja'],
            start_date=json_obj['start_date'],
            end_date=json_obj['end_date'] if 'end_date' in json_obj else "",
            synopsis=json_obj['synopsis'],
            mean_score=json_obj['mean'],
            rank=json_obj['rank'] if 'rank' in json_obj else "",
            popularity=json_obj['popularity'],
            nsfw=True if json_obj['nsfw'] != "white" else False,
            media_type=json_obj['media_type'],
            status=json_obj['status'],
            genres=[genre['name'] for genre in json_obj['genres']],
            num_episodes=json_obj['num_episodes'],
            source=json_obj['source'] if 'source' in json_obj else "",
            average_episode_duration_seconds=json_obj['average_episode_duration'],
            rating=json_obj['rating'],
            studios=[studio['name'] for studio in json_obj['studios']],
            num_list_users=json_obj['num_list_users'],
            num_scoring_users=json_obj['num_scoring_users'],
            watching=int(json_obj['statistics']['status']['watching']),
            completed=int(json_obj['statistics']['status']['completed']),
            on_hold=int(json_obj['statistics']['status']['on_hold']),
            dropped=int(json_obj['statistics']['status']['dropped']),
            plan_to_watch=int(json_obj['statistics']['status']['plan_to_watch']),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        anime = {
            "id": self.id,
            "title": self.title,
            "picture": self.picture,
            "title_en": self.title_en,
            "title_ja": self.title_ja,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "synopsis": self.synopsis.replace("\n", " "),
            "mean_score": self.mean_score,
            "rank": self.rank,
            "popularity": self.popularity,
            "nsfw": self.nsfw,
            "media_type": self.media_type,
            "status": self.status,
            "genres": self.genres,
            "num_episodes": self.num_episodes,
            "source": self.source,
            "average_episode_duration_seconds": self.average_episode_duration_seconds,
            "rating": self.rating,
            "studios": self.studios,
            "num_list_users": self.num_list_users,
            "num_scoring_users": self.num_scoring_users,
            "watching": self.watching,
            "completed": self.completed,
            "on_hold": self.on_hold,
            "dropped": self.dropped,
            "plan_to_watch": self.plan_to_watch,
        }
        return anime


def get_anime(anime_id: int) -> Anime:
    anime_url = lambda id: BASE_URL + f"/anime/{id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,media_type,status,genres,num_episodes,source,average_episode_duration,rating,studios,statistics"
    try:
        response = get_mal(anime_url(anime_id), access_token=TOKEN)
    except HTTPError as err:
        # TODO
        print("HTTP Error: ", err)
        raise err
    try:
        anime = Anime.from_json(response)
    except KeyError as err:
        # TODO
        print("Key error: ", err)
        raise err
    return anime


def write_anime_list_to_csv(csv_file: str,
                            anime_list: List[Anime],
                            write_headers: bool = False):
    if write_headers:
        mode = "w"
    else:
        mode = "a"
    with open(csv_file, mode, newline='', encoding='utf-8') as csv_file:
        fieldnames = [
            "id",
            "title",
            "picture",
            "title_en",
            "title_ja",
            "start_date",
            "end_date",
            "synopsis",
            "mean_score",
            "rank",
            "popularity",
            "nsfw",
            "media_type",
            "status",
            "genres",
            "num_episodes",
            "source",
            "average_episode_duration_seconds",
            "rating",
            "studios",
            "num_list_users",
            "num_scoring_users",
            "watching",
            "completed",
            "on_hold",
            "dropped",
            "plan_to_watch"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if write_headers:
            writer.writeheader()
        for anime in anime_list:
            row = anime.to_dict()
            writer.writerow(row)

            
def gather_animes_and_write_to_csv(csv_file: str,
                                   start_id: int,
                                   stop_id: int,
                                   new_file: bool = False):
    for id in range(start_id, stop_id):
        try:
            anime = get_anime(id)
        except HTTPError as err:
            if err.response.status_code == 404:
                print(f"Anime with ID {id} not found, skipping.")
                continue
        if id == start_id and new_file:
            write_anime_list_to_csv(csv_file=csv_file,
                                    anime_list=[anime],
                                    write_headers=True)
            continue
        write_anime_list_to_csv(csv_file=csv_file,
                                anime_list=[anime])