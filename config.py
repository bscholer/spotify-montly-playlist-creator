from typing import List, Type, Protocol

from pydantic import BaseModel, StrBytes


class PeriodPlaylistConfig(BaseModel):
    period: str
    only_process_current_period: bool = True
    playlist_name: str
    playlist_description: str
    public: bool = False
    collaborative: bool = False
    minimum_tracks: int = 2
    alliteration_word_list: List[str] = []


class Config(BaseModel):
    period_playlists: List[PeriodPlaylistConfig]


def load_config():
    with open('config.json', 'r') as f:
        return Config.parse_raw(f.read())
