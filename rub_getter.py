import requests
import json
from time import sleep
from os import environ as env

def get_rates():
    r = requests.get("https://openexchangerates.org/api/latest.json?app_id=d562383f71df44ff96805dacc354c032")
    data = json.loads(r.text)

    return data["rates"]

while True:
    rates = get_rates()
    rates_keys = list(rates.keys())
    rub = rates["RUB"]
    rub_rates = {}

    for rk in rates_keys:
        if rk != "RUB":
            rub_rates.update({rk:(rub/rates[rk])})

    requests.patch("https://rubisintheass.firebaseio.com/RUB.json", data=json.dumps(rub_rates))

    sleep(3600)