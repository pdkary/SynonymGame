import requests
from synonyms import get_all_synonyms, get_synonyms
from random import sample
random_word_url = "https://random-word-api.herokuapp.com/word"

def get_random_words(n=1):
  return requests.get(random_word_url + "?number=" + str(n)).json()

def get_n_words_with_m_or_more_synonyms(n=10,m=2):
  words = get_random_words(n)
  valid_words = {k:v for k,v in get_all_synonyms(words).items() if len(v) > m}
  if len(valid_words) == n:
    return valid_words
  else:
    return {**valid_words, **get_n_words_with_m_or_more_synonyms(n - len(valid_words),m)}

class GameState():
    def __init__(self):
        wordset = get_n_words_with_m_or_more_synonyms(10,3)
        self.starting_word, self.ending_word = sample(list(wordset.keys()),k=2)
        self.path = [self.starting_word]
        self.current_word = self.starting_word
        self.previous_word = None
        print("="*10 + "GAME START" + "="*10)
        print("="*5 + self.starting_word.upper() + ">"*5 + self.ending_word.upper() + "="*5)

    @property
    def steps(self):
        return len(self.path)
    
    @property
    def win(self):
        return self.ending_word in self.path
    
    def play_round(self):
        syns = get_synonyms(self.current_word)
        print(self.path,": ",syns)
        next_word = input("Pick a synonym: ")
        if next_word.lower() == 'back':
            self.back()
            self.play_round()
        else:
            assert next_word in syns
            self.path.append(next_word)
            self.previous_word = self.current_word
            self.current_word = next_word
    
    def back(self):
        self.path = self.path[:-1]
        self.current_word = self.previous_word


if __name__ == '__main__':
    gamestate = GameState()
    while not gamestate.win:
        gamestate.play_round()
