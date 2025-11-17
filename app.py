import requests
from fastapi import FastAPI

app = FastAPI()

BASE = "https://api.sofascore.com/api/v1"

def get_stats(match_id):
    url = f"{BASE}/event/{match_id}/statistics"
    r = requests.get(url)
    return r.json()

def get_games_by_date(date):
    url = f"{BASE}/sport/football/scheduled-events/{date}"
    r = requests.get(url)
    return r.json()

@app.get("/jogos/{date}")
def jogos_do_dia(date: str):
    return get_games_by_date(date)

@app.get("/estatisticas/{match_id}")
def estatisticas(match_id: int):
    data = get_stats(match_id)

    stats = {
        "escanteios": {},
        "chutes_totais": {},
        "chutes_no_alvo": {},
        "cartoes_amarelos": {},
        "cartoes_vermelhos": {}
    }

    for group in data.get("statistics", []):
        for item in group.get("statisticsItems", []):
            name = item.get("name")
            home = item.get("home")
            away = item.get("away")

            if name == "Corner kicks":
                stats["escanteios"] = {"casa": home, "fora": away}
            if name == "Shots":
                stats["chutes_totais"] = {"casa": home, "fora": away}
            if name == "Shots on target":
                stats["chutes_no_alvo"] = {"casa": home, "fora": away}
            if name == "Yellow cards":
                stats["cartoes_amarelos"] = {"casa": home, "fora": away}
            if name == "Red cards":
                stats["cartoes_vermelhos"] = {"casa": home, "fora": away}

    return stats
