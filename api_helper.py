import requests
from datetime import datetime
from app import app
from models import db, Event


def get_all_NBA_events_current_season():
    current_season_str = str(datetime.now().year) + "-" + str(datetime.now().year + 1)
    res = requests.get(
        f"https://www.thesportsdb.com/api/v1/json/{app.config['API_KEY']}/eventsseason.php?id=4387&s={current_season_str}"
    )

    return res.json()


def add_api_results_to_db():
    res = get_all_NBA_events_current_season()
    new_events = []
    for r in res["events"]:
        new_events.append(
            Event(
                sportsdb_id=r["idEvent"],
                title=r["strEvent"],
                home_team=r["strHomeTeam"],
                away_team=r["strAwayTeam"],
                datetime=r["strTimestamp"],
                date=r["dateEvent"],
            )
        )
    db.session.add_all(new_events)
    db.session.commit()
