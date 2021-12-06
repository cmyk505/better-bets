from flask import Flask, request, session, render_template
from faker import Faker
from models import User, Event
from helpers import convert_to_named_tuple

from app import db, app
import requests


def get_event_result(id, key):
    """Call out to datadb API to get the result of an individual event"""
    required_fields = [
        "idEvent",
        "strEvent",
        "strHomeTeam",
        "strAwayTeam",
        "intHomeScore",
        "intAwayScore",
        "strTimestamp",
        "strStatus",
        "dateEvent",
    ]

    api_url = (
        f"https://www.thesportsdb.com/api/v1/json/{key}/lookupevent.php?id={str(id)}"
    )
    data = requests.get(api_url).json()["events"][0]

    if data["strStatus"] == "FT" or data["strStatus"] == "AOT":
        event_info = {x: data[x] for x in required_fields}

        if event_info["intHomeScore"] > event_info["intAwayScore"]:
            event_info.update({"winner": event_info["strHomeTeam"]})
        else:
            event_info.update({"winner": event_info["strAwayTeam"]})
        event_info.update({"resolved": "true"})
    else:
        return False

    return event_info


def run_tasks(db, key):
    """Function run on a scheduled basis to 1) get unresolved events from DB
    2) call out to API to check for any resolution for those events 3) based on
    response from API, update resolved events in database 4) update user balances
    based on results"""
    # Below query gets all unresolved events with bets
    unresolved_events = convert_to_named_tuple(
        db.session.execute(
            "SELECT sportsdb_id FROM event WHERE resolved = 'f' OR (resolved = 't' AND home_score IS NULL)"
        )
    )
    if len(unresolved_events) == 0:
        return
    # Then need to make API call
    update_list = []
    for e in unresolved_events:
        res = get_event_result(e.sportsdb_id, key)
        if res:
            if int(res["intHomeScore"]) > 0:
                update_list.append(res)

    # Need to update database for all events where API call found a result
    # Need to update all unresolved bets linked to events we just resolved

    for e in update_list:
        db.session.execute(
            "UPDATE event SET winner = :winner, resolved=:resolved, home_score=:home_score, away_score=:away_score WHERE sportsdb_id = :sportsdb_id",
            {
                "winner": e["winner"],
                "resolved": "t",
                "sportsdb_id": e["idEvent"],
                "home_score": e["intHomeScore"],
                "away_score": e["intAwayScore"],
            },
        )
        db.session.commit()

        balance_adjustment = {}
        # dictionary to hold user ID and balance adjustment for that user based on newly resolved bet

        event = convert_to_named_tuple(
            db.session.execute(
                "SELECT id FROM event WHERE sportsdb_id = :id", {"id": e["idEvent"]}
            )
        )
        # event to get event ID in database as opposed to eventsdb_id (from API)

        bets = db.session.execute(
            "SELECT id, amount, selection, user_id FROM bet WHERE event = :id",
            {"id": event[0].id},
        )

        # above gets all bets from DB for given unresolved event in loop. Then we'll loop through all those bets for the given event

        for b in bets:
            final_margin = (
                (b.amount * 2)
                if e["winner"].lower() == b.selection.lower()
                else -b.amount
            )
            # final margin is positive or negative amount depending on if user won bet

            if balance_adjustment.get(b.user_id) is not None and final_margin > 0:
                balance_adjustment[b.user_id] = (
                    balance_adjustment[b.user_id] + final_margin
                )
            if balance_adjustment.get(b.user_id) is None and final_margin > 0:
                balance_adjustment[b.user_id] = final_margin
            db.session.execute(
                "UPDATE bet SET final_margin=:final_margin WHERE event IN (SELECT id FROM event WHERE id=:id)",
                {"final_margin": final_margin, "id": event[0].id},
            )
            db.session.commit()
            # update bet record in database

        # For all newly resolved bets, need to update user balance for all linked users
        for (k, v) in balance_adjustment.items():
            if v > 0:
                db.session.execute(
                    "UPDATE user_balance SET balance = (balance + :adjustment) WHERE user_id = :user_id",
                    {"adjustment": v, "user_id": k},
                )
                db.session.commit()


# for use on Heroku
with app.app_context():
    run_tasks(db, app.config["API_KEY"])
