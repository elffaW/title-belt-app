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
        "belt_holder": NhlTeams[holder],
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
            "belt_holder": NhlTeams[holder],
            "numGames": 0,
            "team": NhlTeams[team_id],
            "season": schedule.get_season_pretty(),
            "games": [],
        }
    else:
        path_games = schedule.find_nearest_path_games()
        num_games = len(path_games)
        sorted_path = []
        for match_list in path_games:
            sorted_path.append(sorted(match_list, key=lambda g: g.on_shortest_path, reverse=True))
        # for depth, match_list in enumerate(path_games):
        #     print(f"{depth}: {len(match_list)}")
        #     for match in match_list:
        #         on_path = "*" if match.on_shortest_path else ""
        #         print(
        #             f"\t{match.date_obj} | {match.belt_holder} -> {match} {on_path}"
        #         )

        context = {
            "request": request,
            "belt_holder": NhlTeams[holder],
            "numGames": num_games,
            "team": NhlTeams[team_id],
            "season": schedule.get_season_pretty(),
            "games": sorted_path,
        }

    return templates.TemplateResponse("team.html", context)

@router.get("/schedule/{team_id}")
def get_schedule(team_id: str, request: Request):
    if team_id not in [t for t in NhlTeams.__members__.keys()]:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    games = Schedule(team_id).get_matches_for_team(team_id)

    context = {
        "request": request,
        "team": NhlTeams[team_id],
        "schedule": games,
    }

    return templates.TemplateResponse("schedule.html", context)

@router.get("/teams")
def get_teams():
    return [t for t in NhlTeams]
