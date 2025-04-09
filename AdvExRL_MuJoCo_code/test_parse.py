'''
Contains the code to parse the description of the observations and actions to a textual description
'''
import math

class parser(): 
    def __init__(self, observation, action):
        
        #Parse the Action
        self.action_left_right = action[0]
        self.action_up_down = action[1]
        self.action_left_right_word = None
        self.action_up_down_word = None
        self.magnitude = None
        self.action_sentence = None

        #Parse the OBS 
        
        
    def parse_action_to_directions(self): 
        #See if the action is left or right
        if self.action_left_right < 0: 
            self.action_left_right_word = 'left'
        elif self.action_left_right > 0: 
            self.action_left_right_word = 'right'

        #See if the action direction is up or down
        if self.action_up_down < 0: 
            self.action_up_down_word = 'down'
        if self.action_up_down > 0: 
            self.action_up_down_word = 'up'

    def calc_magnitude(self): 
        #Calculates the magnitude of the action 

        self.magnitude = round(math.sqrt((self.action_left_right**2) + (self.action_up_down **2)),2)

    def create_sentence_action(self): 
        self.parse_action_to_directions()
        self.calc_magnitude()
        if self.magnitude < 0.4: 
            direction = 'Weak'
        elif 0.4 < self.magnitude < 0.92: 
            direction = 'Moderate'
        else: 
            direction = 'Strong'

        self.action_sentence = f"The agent moved {self.action_left_right_word} and {self.action_up_down_word} {direction}ly with magnitude {self.magnitude}"


if __name__ == '__main__': 
    action = [ 0.36657423,-0.535817]
    obs = [0,0,0,0]
    parser = parser(obs, action)
    parser.create_sentence_action()
    print(parser.action_sentence)
    print(f"The agent took the directions {parser.action_left_right_word}, {parser.action_up_down_word} with magnitude {parser.magnitude}")


