from flask import Flask, request, session, render_template
from app import app, socket_, db
from faker import Faker
from models import User, Event


def run_tasks():
    """"""
    print("Adding a new user to the database every minute")
    faker = Faker()
    new_user = User(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        hashed_password="*FAKE*",
    )
    db.session.add(new_user)
    db.session.commit()
    socket_.emit(
        "new_db_add", {"data": f"New user: {new_user.first_name} {new_user.last_name}"}
    )


# Need to find all users with unresolved bets
# users = db.session.execute('SELECT user_id FROM bet JOIN event ON event.id = bet.event WHERE event.resolved= :val', {'val': 'f'})

# Need to go through all unresolved bets and make API call checking for result (might need to wait 2 mins between each API call, so update could take a while)

# Need to update database for all events where API call found a result
# Need to update all unresolved bets linked to events we just resolved
# balance_adjustment = {}
# dictionary to hold user ID and balance adjustment for that user based on newly resolved bets
# for (id, winner) in api_results:
# db.session.execute('UPDATE event SET winner = :winner, resolved=:resolved WHERE id = :id', {'winner': winner, 'resolved': 't', 'id': id})
# bets = db.session.execute('SELECT id, amount, selection FROM bet WHERE event = :id', {'id': id})
# for b in bets:
# b_dict = dict(b.items()) # convert to dict keyed by column names
# id = b_dict['id']
# amount = b_dict['amount']
# selection = b_dict['selection']
# final_margin = amount if winner==selection else -amount
# if balance_adjustment.get(b_dict['user_id']) is not None:
#   balance_adjustment[b_dict['user_id']] = balance_adjustment[b_dict['user_id']] + finalMargin
# else:
#   balance_adjustment[b_dict['user_id']] = finalMargin
# db.session.execute('UPDATE bet SET final_margin=:final_margin WHERE event IN (SELECT id FROM event WHERE id=:id', {'final_margin': final_margin, 'id': id})


# For all newly resolved bets, need to update user balance for all linked users
# for (k, v) in balance_adjustment.items():
# db.session.execute(UPDATE user_balance SET balance = (balance + :adjustment) WHERE user_id = :user_id', {'adjustment': v, 'user_id': v})
