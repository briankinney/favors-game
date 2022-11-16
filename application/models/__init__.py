import dotenv
dotenv.load_dotenv()

import sqlalchemy
from sqlalchemy import text

from os import environ

DATABASE_URL = f"postgresql://{environ['DB_USERNAME']}:{environ['DB_PASSWORD']}@kt-dev.ca05z1awppqr.us-east-1.rds.amazonaws.com:5432/favors_game"
engine = sqlalchemy.create_engine(DATABASE_URL)


def create_game(data):
    sql = "INSERT INTO games (name) VALUES ('{name}') RETURNING ID;".format(name=data['name'])

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        inserted_id = result.fetchall()[0]['id']
        print(inserted_id)
        return inserted_id

def get_active_games() -> list[dict]:
    """
    Return a list of currently active games.
    A game is active if less than 10 minutes since time created.
    TODO: Verify defintion of an active game.
    """
    sql = "SELECT id FROM games WHERE TIMEDIFF(MINUTE, created, CURRENT_TIMESTAMP()) < 10 "
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        data = [dict(row) for row in result]
        return data



def get_players(game_id):
    sql = text("SELECT * FROM players WHERE game_id = :game_id;")

    with engine.connect() as conn:
        result = conn.execute(sql, game_id=game_id)
        data = [dict(row) for row in result]
        return data


def get_favors():
    sql = 'SELECT * FROM favors;'

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        data = [dict(row) for row in result]
        return data


def get_favor(id):
    sql = 'SELECT * FROM favors WHERE id = {favor_id}'.format(favor_id=id)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        data = [dict(row) for row in result]
        return data


def get_my_favors(user_id):
    sql = text("""SELECT e.id, 
                        p.name as me,
                        pr.name as receiver,
                        f.name as favor_name,
                        f.cost as favor_cost,
                        f.jollies as favor_jollies,
                        e.boost_value as boost_value
                    from exchanges e join favors f on f.id = e.favor_id
                                     join players p on e.giving_player = p.id
                                     join players pr on e.receiving_player = pr.id
                    WHERE p.id = :user_id
                    ORDER by 1""")

    with engine.connect() as conn:
        result = conn.execute(sql, user_id=user_id)
        data = [dict(row) for row in result]
        return data


def get_game_data(game_id):
    sql = 'SELECT * FROM games WHERE id = {game_id}'.format(game_id=game_id)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        game_data = [dict(row) for row in result][0]
        return game_data


def create_exchange_object(game_id, favor_id, giver_id, receiver_id, boost_value):
    sql = text("""INSERT INTO exchanges (game_id, favor_id, giving_player, receiving_player, boost_value)
                  VALUES (:gid, :fid, :gvid, :rid, :b) RETURNING id""")

    with engine.connect() as conn:
        result = conn.execute(sql, gid=game_id, fid=favor_id, gvid=giver_id, rid=receiver_id, b=boost_value)
        assert result.rowcount == 1
        row = result.fetchone()
        return row['id']


def verify_exchange_completion(exchange_id, player_id, game_id, boost_value):
    sql = text("""UPDATE exchanges SET verified = true, boost_value = :b WHERE id = :id AND receiver_id = :rid AND game_id = :gid RETURNING id""")

    with engine.connect() as conn:
        result = conn.execute(sql, id=exchange_id, rid=player_id, gid=game_id, b=boost_value)
        if result.rowcount == 0:
            raise Exception(f"Unable to update exchange {exchange_id}. Was it received by player {player_id}?")
        elif result.rowcount != 1:
            raise Exception("Something really strange happened.")


def create_player(form_data, game_id):
    name = form_data['name']
    sql = f"SELECT * FROM players WHERE name LIKE '{name}' AND game_id = {game_id};"

    with engine.connect() as conn:
        cursor = conn.execute(text(sql))
        results = cursor.fetchall()
        if len(results) > 0:
            print(f"the player name {name} already exists in game {game_id}")
            user_id = results[0]['id']
            return user_id


    sql = "INSERT INTO players (name, game_id) VALUES ('{name}', {game_id}) RETURNING ID;".format(
        name=name,
        game_id=game_id
    )

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        inserted_id = result.fetchall()[0]['id']
        print(inserted_id)
        return inserted_id


def get_player_data(player_id):
    sql = 'SELECT * FROM players WHERE id = {player_id}'.format(player_id=player_id)

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        data = [dict(row) for row in result][0]
        return data

def get_exchanges_game_29():
    sql = """
        SELECT
            exchanges.id AS exchange_id,
            givers.name AS giver, receivers.name AS receiver,
            favors.name AS favor, favors.type AS favor_type,
            favor.jollies AS points, exchanges.boost_value
        FROM
            exchanges LEFT JOIN players givers
                ON  givers.id = exchanges.giving_player
            LEFT JOIN players receivers
                ON  receivers.id = exchanges.receiving_player
            LEFT JOIN favors
                on  exchanges.favor_id = favors.id
        WHERE
            exchanges.game_id = 29  ;
        """

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        data = [dict(row) for row in result]
        return data
