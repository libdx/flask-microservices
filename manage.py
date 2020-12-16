from flask.cli import FlaskGroup

from project import create_app, db
from project.api.users.models import User  # noqa: F401

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreatedb():
    """Drops all tables in database and creates them again"""

    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user1 = User(username="joe", email="joe@example.com", password="A")
    user2 = User(username="jane", email="jane@example.com", password="B")

    db.session.add_all([user1, user2])
    db.session.commit()


if __name__ == "__main__":
    cli()
