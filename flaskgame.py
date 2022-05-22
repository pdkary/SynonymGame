from flask import Flask, redirect, render_template, request
import uuid
import os
from game import GameState

app = Flask(__name__)

activegames = {}

def render_game_template(state: GameState):
    return render_template('game.html',
        difficulty=state.difficulty, 
        starting_word=state.starting_word, 
        ending_word=state.ending_word, 
        current_path=state.path, 
        current_word = state.current_word, 
        synonyms = state.current_syns,
        ideal_path = " -> ".join(state.ideal_path))

def render_win_template(state: GameState):
    return render_template('win.html',
        difficulty=state.difficulty, 
        ideal_path = " -> ".join(state.ideal_path),
        user_path=" -> ".join(state.path),
        game_time=state.game_total_time)

@app.route('/')
def home():
    return redirect('/newgame/3')

@app.route('/newgame/<difficulty>', methods=['GET', 'POST'])
def newgame(difficulty):
    addr = request.remote_addr
    activegames[addr] = GameState(difficulty)
    return redirect('/game')

@app.route('/game', methods=['GET', 'POST'])
def game():
    addr = request.remote_addr
    if addr not in activegames or activegames[addr].win:
        return redirect('/')
    activegame = activegames[addr]

    if request.method == 'POST':
        if 'difficulty' in request.form:
            return redirect('/newgame/' + request.form['difficulty'])
        if 'back' in request.form:
            activegame.back()
        if 'next_word' in request.form:
            next_word = request.form['next_word']
            activegame.guess(next_word)
    if activegame.win:
        return render_win_template(activegame)
    else:
        return render_game_template(activegame)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)