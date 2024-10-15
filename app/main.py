import functools

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Schedule
from title_belt_nhl.service.nhl_api import getFullSchedule

from app import templates
from app import api
from app.models import NhlTeams

app = FastAPI()

app.include_router(api.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@functools.cache
def _build_full_page_context(request: Request):
    teams = [t for t in NhlTeams]
    schedule = Schedule("")
    holder = schedule.belt_holder
    selected_team = holder
    
    leagueSchedule = getFullSchedule(schedule.season)

    return {
        "request": request,
        "belt_holder": NhlTeams[holder],
        "numGames": -1,
        "teams": teams,
        "team": selected_team,
        "season": schedule.get_season_pretty(),
        "schedule": [],
        "next_bout": schedule.find_match(holder, schedule.from_date),
        "belt_path": Schedule.find_belt_path(leagueSchedule),
    }


@app.get("/")
async def root(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("home.html", context)

@app.get("/rankings")
def get_rankings(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("teams_ranking.html", context)

@app.get("/teams")
def get_rankings(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("teams_next_chance.html", context)

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Success!"}
