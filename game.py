import requests
from data.synonym_service import get_all_synonyms, get_synonyms
from random import sample
random_word_url = "https://random-word-api.herokuapp.com/word"

def get_random_words(n=1):
  return requests.get(random_word_url + "?number=" + str(n)).json()

def get_n_words_with_m_or_more_synonyms(n=10,m=2):
  words = get_random_words(n)
  print(words)
  valid_words = {k:v for k,v in get_all_synonyms(words).items() if len(v) > m}
  if len(valid_words) == n:
    return valid_words
  else:
    return {**valid_words, **get_n_words_with_m_or_more_synonyms(n - len(valid_words),m)}

class GameState():
    def __init__(self):
        # wordset = get_n_words_with_m_or_more_synonyms(2,2)
        self.starting_word, self.ending_word = get_n_words_with_m_or_more_synonyms(2,4)
        self.path = [self.starting_word]
        self.current_word = self.starting_word
        self.current_syns = get_synonyms(self.current_word)

        print("="*10 + "GAME START" + "="*10)
        print("="*5 + self.starting_word.upper() + ">"*5 + self.ending_word.upper() + "="*5)

    @property
    def steps(self):
        return len(self.path)
    
    @property
    def win(self):
        return self.ending_word in self.path
    
    def guess(self,next_word):
        if next_word.lower() == 'back':
            self.back()
        else:
            assert next_word in self.current_syns
            self.path.append(next_word)
            self.current_word = next_word
            self.current_syns = [s for s in get_synonyms(self.current_word) if s not in self.path]
    
    def back(self):
        self.path = self.path[:-1]
        self.current_word = self.path[-1]
        self.current_syns = [s for s in get_synonyms(self.current_word) if s not in self.path]
    
if __name__ == '__main__':
    gamestate = GameState()
    while not gamestate.win:
        gamestate.play_round()
