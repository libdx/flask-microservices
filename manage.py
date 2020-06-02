from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User  # noqa: F401

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreatedb():
    '''Drops all tables in database and creates them again'''

    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
