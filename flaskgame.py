from flask import Flask, redirect, render_template, request
import uuid
import os
from game import GameState

app = Flask(__name__)

activegames = {}

@app.route('/')
def home():
    return redirect("/newgame")

@app.route('/newgame')
def newgame():
    newgame_id = uuid.uuid4()
    activegames[newgame_id] = GameState()
    return redirect("/game/" + str(newgame_id))

@app.route('/game/<id>', methods=['GET'])
def game(id):
    game_id = uuid.UUID(id)
    activegame = activegames[game_id]
    print(activegame.starting_word,activegame.ending_word)
    return render_template('game.html', starting_word=activegame.starting_word, ending_word=activegame.ending_word, current_path=activegame.path, current_word = activegame.current_word, synonyms = activegame.current_syns)

@app.route('/game/<id>', methods=['POST'])
def game_post(id):
    game_id = uuid.UUID(id)
    activegame = activegames[game_id]
    try:
        next_word = request.form['next_word']
        activegame.guess(next_word)
    except:
        activegame.guess('back')
    return redirect("/game/" + str(game_id))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)