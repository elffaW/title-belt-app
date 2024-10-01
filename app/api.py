from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Schedule

from app import templates
from app.models import NhlTeams

router = APIRouter(prefix="/api")

@router.get("/belt_holder")
async def get_belt_holder():
    schedule = Schedule("")
    holder = schedule.belt_holder

    return {"holder": holder, "season": schedule.season}

@router.get("/path/{team_id}")
async def get_path_to_belt(team_id: NhlTeams):
    if team_id not in NhlTeams:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    schedule = Schedule(team_id)
    holder = schedule.belt_holder

    path = schedule.find_nearest_path([holder], holder)
    games = path.split("vs")

    return {
        "holder": holder,
        "numGames": len(games) - 1,
        "team": team_id,
        "path": path,
    }

@router.get("/teams")
def get_teams():
    return [t for t in NhlTeams]
