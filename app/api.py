from fastapi import APIRouter, HTTPException, Request
from title_belt_nhl.schedule import Schedule

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

    if team_id == schedule.belt_holder:
        context = {
            "request": request,
            "belt_holder": NhlTeams[holder].value,
            "numGames": 0,
            "team": NhlTeams[team_id],
            "season": schedule.get_season_pretty(),
            "games": [],
        }
    else:
        path_games = schedule.find_nearest_path_games()
        num_games = len(path_games)

        context = {
            "request": request,
            "belt_holder": NhlTeams[holder].value,
            "numGames": num_games,
            "team": NhlTeams[team_id],
            "season": schedule.get_season_pretty(),
            "games": path_games,
        }

    return templates.TemplateResponse("team.html", context)

@router.get("/teams")
def get_teams():
    return [t for t in NhlTeams]
