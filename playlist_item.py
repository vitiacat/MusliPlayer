from dataclasses import dataclass


@dataclass
class PlaylistItem(object):

    url: str
    name: str
    duration: int
    is_url: bool = False
