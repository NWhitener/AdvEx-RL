'''
Contains the code to parse the description of the observations and actions to a textual description
'''
import math

class parser(): 
    def __init__(self, observation, action, caution_zone):
        
        #Parse the Action
        self.action_left_right = action[0]
        self.action_up_down = action[1]
        self.action_left_right_word = None
        self.action_up_down_word = None
        self.magnitude = None
        self.action_sentence = None

        #Parse the OBS 
        self.observation_left_right = observation[0]
        self.observation_up_down = observation[1]
        self.observation_sub_quad = None
        self.observation_sentence = None
        
        self.caution_zone = caution_zone
        self.in_caution = None

        self.text_description = None
        
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

    def find_sub_quadrant(self):  
        x = self.observation_left_right
        y = self.observation_up_down
        left_right_bound = -25
        up_down_bound = 15
        vertical = "Bottom" if y < 0 else "Top"
       
        horizontal = "Left" if x < left_right_bound else "Right"

        vertical_sub = "Down" if abs(y) > up_down_bound else "Up"

        self.observation_sub_quad = f"Negative {vertical} {horizontal} {vertical_sub}"
    
    def is_action_in_caution(self): 
        x, y = self.observation_left_right, self.observation_up_down
        self.in_caution = self.caution_zone.__call__([x,y]) == 1

    def create_text_description(self): 
        self.create_sentence_action()
        self.find_sub_quadrant()
        self.is_action_in_caution()
        text_description = self.action_sentence + '. The agent is in the ' + self.observation_sub_quad +' of the environment.'
        if self.in_caution: 
            text_description = text_description + '. The agent is in the caution zone'
        self.text_description = text_description


