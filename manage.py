from flask.cli import FlaskGroup

from project import app, db

cli = FlaskGroup(app)


@cli.command('recreate_db')
def recreatedb():
    '''Drops all tables in database and creates them again'''
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
