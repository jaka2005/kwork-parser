import json
from dataclasses import dataclass
from typing import Dict, TypeAlias

import requests
from bs4 import BeautifulSoup

from config import KWORK_URL, PROJECTS_URL
from src.database import DatabaseWorker


@dataclass
class Kwork:
    title: str
    description: str
    price: int


Kworks: TypeAlias = Dict[int, Kwork]


# NOTE: may be useful in the future
def parse_kwork(id: int) -> Kwork:
    response = requests.get(KWORK_URL.format(id=id))
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    script_soup: BeautifulSoup = soup.find_all("script", type="application/ld+json")[-1]

    if not script_soup.string:
        raise Exception

    data = json.loads(script_soup.string.replace("\n", "\\r\\n"))

    return Kwork(
        data["name"],
        data["description"],
        int(float(data["offers"]["price"])),
    )


def get_kworks(category: int, page: int = 1) -> Kworks:
    response = requests.get(PROJECTS_URL, params={"c": category, "page": page})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    if not soup.head:
        raise Exception

    scripts = soup.head.find_all("script")
    js_script = ""
    for script in scripts:
        if script.text.startswith("window.ORIGIN_URL"):
            js_script = script.text
            break

    start_pointer = 0
    json_data = ""
    in_literal = False
    for current_pointer in range(len(js_script)):
        if js_script[current_pointer] == '"' and js_script[current_pointer - 1] != "\\":
            in_literal = not in_literal
            continue

        if in_literal or js_script[current_pointer] != ";":
            continue

        line = js_script[start_pointer:current_pointer].strip()
        if line.startswith("window.stateData"):
            json_data = line[17:]
            break

        start_pointer = current_pointer + 1

    data = json.loads(json_data)

    kworks: Kworks = dict()
    for raw_kwork in data["wantsListData"]["wants"]:
        kworks[raw_kwork["id"]] = Kwork(
            title=raw_kwork["name"],
            description=raw_kwork["description"],
            price=int(float(raw_kwork["priceLimit"])),
        )

    return kworks


def get_new_kworks(category: int) -> Kworks:
    kworks = get_kworks(category)
    new_ids = DatabaseWorker().add_projects(list(kworks.keys()))
    return {id: kwork for id, kwork in kworks.items() if id in new_ids}
