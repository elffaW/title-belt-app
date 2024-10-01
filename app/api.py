from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Schedule
from title_belt_nhl.utils import ExcelDate

from app import templates
from app.models import NhlTeams

router = APIRouter(prefix="/api")

@router.get("/belt_holder")
async def get_belt_holder(request: Request):
    schedule = Schedule("")
    holder = schedule.belt_holder

    context = {
        "request": request,
        "belt_holder": NhlTeams[holder].value,
        "season": schedule.season,
    }
    return templates.TemplateResponse("home.html", context)

@router.get("/path/{team_id}")
async def get_path_to_belt(team_id: str, request: Request):
    if team_id not in [t for t in NhlTeams.__members__.keys()]:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    schedule = Schedule(team_id)
    holder = schedule.belt_holder

    path = schedule.find_nearest_path([holder], holder)
    games = path.split("vs")
    num_games = len(games) - 1

    path_games = path.split("] ->")
    path_games = [g.replace("]", "").replace("[", "") for g in path_games]

    # path_games = schedule.games[:num_games]
    # path_games = []
    # for game in schedule.games:
    #     useful_date = ExcelDate(serial_date=game.date)
    #     game.date_obj = useful_date.date_obj
    #     path_games.append(game)
    #     if game.home == holder or game.away == holder:
    #         break    

    context = {
        "request": request,
        "belt_holder": NhlTeams[holder].value,
        "numGames": num_games,
        "path": path,
        "team": NhlTeams[team_id],
        "season": schedule.season,
        "games": path_games,
    }
    return templates.TemplateResponse("team.html", context)

@router.get("/teams")
def get_teams():
    return [t for t in NhlTeams]
