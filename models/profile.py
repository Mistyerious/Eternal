from json import loads
from os import getcwd
from util.helper import get_dict_from_list_by_key

class Profile:
    id: int
    profile_id: int
    balance: int
    class_id: int
    class_name: str
    rank_id: int
    rank_name: str

    def __init__(self, profile_dict: dict) -> None:
        for key in profile_dict:
            setattr(self, key, profile_dict[key])

        with open(f'{getcwd()}/game_data/classes.json', encoding='utf_8') as content:
            class_data = loads(content.read())

        if self.rank_id == 0:
            self.rank_name = "Not Reached"
        else:
            rank_data = get_dict_from_list_by_key(seq=class_data[str(self.class_id)]["ranks"], key="id")
            self.rank_name = rank_data.get(self.rank_id)["name"]
        self.class_name = class_data[str(self.class_id)]["name"]
