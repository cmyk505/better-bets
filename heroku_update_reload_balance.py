from app import db
from helpers import convert_to_named_tuple

users = convert_to_named_tuple(db.session.execute("SELECT id FROM users"))
for u in users:
    db.session.execute(
        "UPDATE users SET can_refill_balance = TRUE WHERE id=:id", {"id": u.id}
    )
    db.session.commit()