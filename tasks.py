from flask import Flask, request, session, render_template
from app import app


def run_tasks():
    """"""
    print("Printing something")


# Need to find all users with unresolved bets
# users = db.session.execute('SELECT user_id FROM bet JOIN event ON event.id = bet.event WHERE event.resolved= :val', {'val': 'f'})

# Need to go through all unresolved bets and make API call checking for result (might need to wait 2 mins between each API call, so update could take a while)

# Need to update database for all events where API call found a result
# for (id, winner) in api_results:
# db.session.execute('UPDATE events SET winner = :winner, resolved=:resolved WHERE id = :id', {'winner': winner, 'resolved': 't', 'id': id})

# Need to update all unresolved bets linked to events we just resolved
# For all newly resolved bets, need to update user balance for all linked users

# result = db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})
