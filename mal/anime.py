from mal.mal import get_mal, TOKEN, BASE_URL
from dataclasses import dataclass
from typing import List
from requests.exceptions import HTTPError


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
    def from_json(cls, json_obj):
        return cls(
            id=json_obj['id'],
            title=json_obj['title'],
            picture=json_obj['main_picture']['medium'],
            title_en=json_obj['alternative_titles']['en'],
            title_ja=json_obj['alternative_titles']['ja'],
            start_date=json_obj['start_date'],
            end_date=json_obj['end_date'],
            synopsis=json_obj['synopsis'],
            mean_score=json_obj['mean'],
            rank=json_obj['rank'],
            popularity=json_obj['popularity'],
            nsfw=True if json_obj['nsfw'] != "white" else False,
            media_type=json_obj['media_type'],
            status=json_obj['status'],
            genres=[genre['name'] for genre in json_obj['genres']],
            num_episodes=json_obj['num_episodes'],
            source=json_obj['source'],
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


def get_anime(anime_id: int) -> Anime:
    anime_url = lambda id: BASE_URL + f"/anime/{id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,media_type,status,genres,num_episodes,source,average_episode_duration,rating,studios,statistics"
    try:
        response = get_mal(anime_url(anime_id), access_token=TOKEN)
    except HTTPError as err:
        # TODO
        print("HTTP Error: ", err)
        raise HTTPError
    try:
        anime = Anime.from_json(response)
    except KeyError as err:
        # TODO
        print("Key error: ", err)
        raise ValueError
    return anime
