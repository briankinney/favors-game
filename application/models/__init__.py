import sqlalchemy
from sqlalchemy import text

DATABASE_URL = f"postgresql://favors_game@kt-dev.ca05z1awppqr.us-east-1.rds.amazonaws.com:5432/favors_game"
engine = sqlalchemy.create_engine(DATABASE_URL)


def create_game(data):
    sql = "INSERT INTO games (name) VALUES ('{name}') RETURNING ID;".format(name=data['name'])

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        inserted_id = result.fetchall()[0]['id']
        print(inserted_id)
        return inserted_id


def get_players():
    sql = 'SELECT * FROM players;'

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        print(result)
        return result


def get_favors():
    sql = 'SELECT * FROM favors;'

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        print(result)
        return result


def get_my_favors(user_id):
    sql = 'SELECT * FROM exchanges WHERE giving_player = {user_id}'.format(user_id=user_id)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        print(result)
        return result


def get_game_data(game_id):
    sql = 'SELECT * FROM games WHERE id = {game_id}'.format(game_id=game_id)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        game_data = [dict(row) for row in result][0]
        return game_data
