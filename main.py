from typing import Optional

from fastapi import FastAPI, HTTPException
from title_belt_nhl.schedule import Schedule

from .models import NhlTeams


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Try /belt_holder or /teams"}

@app.get("/belt_holder")
async def get_belt_holder():
    schedule = Schedule(team, season)
    holder = schedule.belt_holder

    return {"holder": holder, "season": schedule.season}

@app.get("/teams/{team_id}")
async def get_belt_opportunity(team_id: NhlTeams):
    if team_id not in NhlTeams:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    schedule = Schedule(team, season)
    holder = schedule.belt_holder

    path = schedule.find_nearest_path([holder], holder)
    games = path.split("vs")

    return {
        "holder": holder,
        "numGames": len(games) - 1,
        "team": team,
        "path": path,
    }

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Success!"}
