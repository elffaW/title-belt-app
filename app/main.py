from datetime import date, timedelta
import functools

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Match, Schedule
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
    from_date = date.today() - timedelta(days=1)
    schedule = Schedule("")
    holder = schedule.belt_holder
    selected_team = holder
    
    league_schedule = getFullSchedule(schedule.season)

    return {
        "request": request,
        "belt_holder": NhlTeams[holder],
        "numGames": -1,
        "teams": teams,
        "team": selected_team,
        "season": schedule.get_season_pretty(),
        "schedule": schedule,
        "next_bout": schedule.find_match(holder, schedule.from_date),
        "belt_path": Schedule.find_belt_path(league_schedule),
    }


@app.get("/")
async def root(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("home.html", context)

@app.get("/rankings")
def get_rankings(request: Request):
    context = _build_full_page_context(request)
    belt_path: list[Match] = context["belt_path"]
    rankings_dict = {}
    for i, game in enumerate(belt_path):
        days_between_games = (date.today() - game.date_obj).days
        if i < len(belt_path) - 1:
            days_between_games = belt_path[i+1].serial_date - game.serial_date
        if i == len(belt_path) - 1 and len(belt_path) == 82:
            # last game of season, don't continue adding belt days
            days_between_games = 1
        if game.home_score > game.away_score:
            if not rankings_dict.get(game.home):
                rankings_dict[game.home] = 0
            rankings_dict[game.home] += days_between_games
        elif game.away_score > game.home_score:
            if not rankings_dict.get(game.away):
                rankings_dict[game.away] = 0
            rankings_dict[game.away] += days_between_games

    context["rankings"] = dict(sorted(rankings_dict.items(), key=lambda item: item[1], reverse=True))

    return templates.TemplateResponse("teams_ranking.html", context)

@app.get("/teams")
def get_rankings(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("teams_next_chance.html", context)

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Success!"}
