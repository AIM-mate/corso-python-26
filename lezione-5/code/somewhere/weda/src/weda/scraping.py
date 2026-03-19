from weda.gemini_manager import GeminiManager

import requests
from importlib import resources
import pandas as pd
from io import StringIO

URL = "https://www.ilmeteo.it/portale/archivio-meteo/{city}/{year}/{month}"
MONTHS = [
    "Gennaio",
    "Febbraio",
    "Marzo",
    "Aprile",
    "Maggio",
    "Giugno",
    "Luglio",
    "Agosto",
    "Settembre",
    "Ottobre",
    "Novembre",
    "Dicembre",
]

# funzioni che iniziano con "_" sono per convenzione private
def _get_prompt():
    # prendiamo le risorse, passando la posizione del file
    # in import assuluto del pacchetto es. 'module.submodule'
    # e il nome del file
    with resources.path("weda.data", "prompt.txt") as f:
        prompt_path = f

    with open(prompt_path, "r") as f:
        prompt = f.read()
    
    return prompt

PROMPT = _get_prompt()

def _get_month(month: str | int):
    if isinstance(month, int):
        assert month >= 1 and month <= 12, f"Month must be between 1 and 12, is {month}"
        return MONTHS[month + 1]
    else:
        assert month in MONTHS, f"Month ({month}) must be one of {MONTHS}"
        return month


def get_weather_predictions(city: str, year: int, month: str | int):
    month = _get_month(month)
    url = URL.format(city=city, month=month, year=year)

    print(f"GET: {url}")
    resp = requests.get(url)

    if resp.status_code != 200:
        raise ValueError(f"Requesto to {url} returned status code {resp.status_code}")

    print("Correctly retrieved content")

    content = resp.text
    print(content[:200])

    prompt = PROMPT.replace("{HTML_input}", content)
    csv_str = GeminiManager.run_prompt(prompt)

    print(csv_str)
    df = pd.read_csv(StringIO(csv_str))
    print("CSV correctly loaded")
    return df