# !/usr/bin/env python3

from application.models import *
from application.visualizations.local_data_charts import *
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session

from application.metabase.embed_link import get_dashboard_embed

app = Flask(__name__)
app.config['TESTING'] = True
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

#################### TEACHING ROUTES ###############################

# Route to homepage
@app.route("/", methods=['GET'])
def render_home():
    user_input = request.args.get("userInput")
    visualization = get_chart_src(title=user_input)

    return render_template('home.html',
                           visualization=visualization,
                           **request.args)

@app.route("/insights", methods=['GET'])
def render_insights():
    leaderboard_src = get_leaderboard_src()
    favors_table = get_favors_table()
    return render_template('insights.html',
                           leaderboard_src=leaderboard_src,
                           favors_table=favors_table,
                           **request.args)





#################### GAME ROUTES ###############################

@app.route("/", methods=['POST'])
def render_index():
    return redirect(url_for('render_home', **request.form))


@app.route("/game/create", methods=['GET'])
def render_game_create():
    return render_template('create.html', page_title="Create a game")


@app.route("/game/create", methods=['POST'])
def post_create_game():
    data = request.form
    print('data is:', data)
    db_result = create_game(data)
    print("db result is ", db_result)
    return redirect(url_for('join_game', game_id=db_result))


@app.route("/game/<game_id>/join", methods=['GET'])
def render_game_join(game_id):
    game_data = get_game_data(game_id)
    print('game data is a list of columns', game_data)
    return render_template('join.html', page_title="Join game", game_data=game_data)


@app.route("/game/<game_id>/join", methods=['POST'])
def join_game(game_id):
    form_data = request.form
    print('form data is:', form_data)
    player_id = create_player(form_data, game_id)
    print("db result is ", player_id)
    session["id"] = player_id
    player_data = get_player_data(player_id)

    # save user data to session
    return redirect(url_for('render_game_play', game_id=game_id))


@app.route("/game/<game_id>/play", methods=['GET'])
def render_game_play(game_id):
    players = get_players(game_id)
    favors = get_favors()
    print(session)

    try:
        my_favors = get_my_favors(user_id=session["id"])
    except KeyError:
        return redirect(url_for('join_game', game_id=game_id))

    return render_template('play.html', page_title="The Favors Game™",
                           game_id=game_id,
                           players=players,
                           favors=favors,
                           my_favors=my_favors)


@app.route("/game/<id>/report", methods=['GET'])
def render_game_report(id):
    dashboardUrl = get_dashboard_embed(game_id=id)
    return render_template('report.html', page_title=f"Game {id} results", embedUrl=dashboardUrl)


@app.route("/game/<game_id>/exchange/create", methods=['POST'])
def exchange_favor(game_id):
    formdata = request.form
    try:
        giver_id = formdata["giver_id"]
    except:
        giver_id = session["id"]
    if giver_id is None:
        giver_id = session["id"]
    receiver_id = formdata["receiver"]
    favor_id = formdata["favor_id"]
    if "boost_value" not in formdata:
        boost_value = 1
    else:
        boost_value = formdata["boost_value"]
    exchange_id = create_exchange_object(game_id, favor_id, giver_id, receiver_id, boost_value)
    return redirect(f"/game/{game_id}/play")


@app.route("/game/<game_id>/exchange/<exchange_id>", methods=['PUT'])
def verify_exchange(game_id, exchange_id):
    receiver_id = session["user_id"]
    formdata = request.form
    boost_value = formdata["boost_value"]
    verify_exchange_completion(exchange_id, receiver_id, game_id, boost_value)
    return redirect(f"/game/{game_id}/play")


@app.route("/favors", methods=['GET'])
def favors():
    favors = get_favors()
    return render_template('favors.html', page_title="Favors",
                           favors=favors)


@app.route("/favors/add_favor", methods=['POST'], defaults={'game_id': None})
@app.route("/favors/add_favor/<game_id>", methods=['POST'])
def add_favor(game_id=None):
    return redirect(url_for('render_add_favor', game_id=game_id))


@app.route("/favors/add_favor/create", methods=['GET'])
def render_add_favor(game_id=None):
    return render_template('add_favor.html', page_title="Favors",
                           game_id=game_id)


@app.route("/favors/<id>/edit_favor", methods=['POST'])
def edit_favor(id):
    return redirect(url_for('render_edit_favor', id=id))


@app.route("/favors/<id>/edit_favor/edit", methods=['GET'])
def render_edit_favor(id):
    favor = get_favor(id)
    return render_template('edit_favor.html', favor=favor)


# Necessary to run app if app.py is executed as a script
if __name__ == "__main__":
    app.run(debug=True, host='localhost')
