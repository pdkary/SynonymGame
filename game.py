import data.saved_game_service as GameService
import data.synonym_service as SynonymService
from time import time

class GameState():
    def __init__(self,difficulty:int=6):
        self.difficulty = difficulty
        start_end, self.ideal_path = GameService.get_random_game(str(difficulty))
        self.starting_word = start_end.split('->')[0]
        self.ending_word = start_end.split('->')[1]
        self.path = [self.starting_word]
        self.current_word = self.starting_word
        self.current_syns = SynonymService.get_syns_and_update(self.current_word)
        self.game_start_time = time()
        self.game_total_time = None

    @property
    def steps(self):
        return len(self.path)
    
    @property
    def win(self):
        return self.ending_word in self.path
    
    def guess(self,next_word):
        assert next_word in self.current_syns
        self.path.append(next_word)
        if self.win:
            self.game_total_time = time() - self.game_start_time
            self.current_word = next_word
            self.current_syns = []
        else:
            self.current_word = next_word
            self.current_syns = [s for s in SynonymService.get_syns_and_update(self.current_word) if s not in self.path]
    
    def back(self):
        self.path = self.path[:-1]
        self.current_word = self.path[-1]
        self.current_syns = [s for s in SynonymService.get_syns_and_update(self.current_word) if s not in self.path]
