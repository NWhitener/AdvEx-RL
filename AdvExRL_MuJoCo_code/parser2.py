
import numpy as np
import math

class Nav2Predicates():
    def __init__(self):
        #Parse the Action
        self.action_left_right = None 
        self.action_up_down = None
        self.action_left_right_word = None
        self.action_up_down_word = None
        self.magnitude = None
        self.action_sentence = None
        self.attr_names = ['X_cord', 'Y_cord']
        self.language_set = np.array(['In border zone',
                        'At the start',
                        'Near the start',
                        'Near the goal',
                        'Reach the goal',
                        'On top border',
                        'On bottom border'
                        'Left to risk area',
                        'Top of risk area',
                        'Right to risk area',
                        'Bottom of risk area',
                        'Very close to risk area',
                        'In risk area',
                        ])

    def predicate_set(self):
        predicates = [{'true': 'In border zone', 'false': 'Not in border zone'},
                {'true': 'At the start', 'false': 'Not at the start'},
                {'true': 'Near the start', 'false': 'Not near the start'},
                {'true': 'Near the goal', 'false': 'Not near the goal'},
                {'true': 'Reach the goal', 'false': 'Not reach the goal'},
                {'true': 'On top border', 'false': 'Not on bottom border'},
                {'true': 'On bottom border', 'false': 'Not on bottom border'},
                {'true': 'Left to risk area', 'false': 'Not left to risk area'},
                {'true': 'Top of risk area', 'false': 'Not top of risk area'},
                {'true': 'Right to risk area', 'false': 'Not right to risk area'},
                {'true': 'Bottom of risk area', 'false': 'Not bottom of risk area'},
                {'true': 'Very close to risk area', 'false': 'Not very close to risk area'},
                {'true': 'In risk area', 'false': 'Not in risk area'}]
    
        return predicates
     
    def state_to_binary(self, state):
        binary_set = [self.border(state),
                self.at_start(state),
                self.near_start(state),
                self.near_goal(state),
                self.at_goal(state),
                self.top_border(state),
                self.bottom_border(state),
                self.left_risk(state),
                self.right_risk(state),
                self.top_risk(state),
                self.bottom_risk(state),
                self.close_risk(state),
                self.in_risk(state)]
        
        #print("state {} and binary state {} ".format(state, np.array(binary_set)))
        return np.array(binary_set)
    
    def translate_state(self, binary_set):
        language_set = np.array(['In border zone',
                    'At the start',
                    'Near the start',
                    'Near the goal',
                    'Reach the goal',
                    'On top border',
                    'On bottom border'
                    'Left to risk area',
                    'Top of risk area',
                    'Right to risk area',
                    'Bottom of risk area',
                    'Very close to risk area',
                    'In risk area'
                    ])
        
        idx = np.where(binary_set==1)[0]
        true_set = language_set[idx]
        string = ''
        if true_set.size != 0:
            string = true_set[0]
            if true_set[1:].size != 0:
                for pred in true_set[1:]:
                    string = string + ' and '
                    string = string + pred
        
        return string


    def feat_groups(self):
        #groups = [[0, 1, 2, 3, 4, 5, 6, 7, 8]]
        groups = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [12]]
        return groups

    def num_predicates(self):
        return 13

    def at_start(self, state):
      if abs(state[0] + 50) <= 2 and abs(state[1]) <= 2:
        return 1
      else:
        return 0
    
    def at_goal(self, state):
      if abs(state[0]) <= 2 and abs(state[1]) <= 2:
        return 1
      else:
        return 0

    def border(self, state):
        if state[1] >= 20:
            return 1
        elif state[1] <= -20:
            return 1
        elif state[0] < -52:
            return 1
        elif state[1] < -52 and abs(state[0]) <= 15:
            return 1
        else:
            return 0
        
    def top_border(self, state):
        if state[1] <= 20 and state[1] >= 15:
            return 1
        else:
            return 0
        
    def bottom_border(self, state):
        if state[1] <= -15 and state[1] >= -20:
            return 1
        else:
            return 0
        
    def near_start(self, state):
        if abs(state[1]) <= 15 and state[0] >= -50 and state[0] <= -40:
            return 1
        else:
            return 0


    def near_goal(self, state):
        if abs(state[1]) <= 15 and state[0] >= -10 and state[0] <= 10:
            return 1
        else:
            return 0
    
    def left_risk(self,state):
        if abs(state[1]) <= 15 and state[0] >= -40 and state[0] <= -30:
            return 1
        else:
            return 0
        
    def right_risk(self,state):
        if abs(state[1]) <= 15 and state[0] >= -20 and state[0] <= -10:
            return 1
        else:
            return 0
        
    def top_risk(self,state):
        if state[1] >= 7.5 and state[1] <= 15 and state[0] >= -30 and state[0] <= -20:
            return 1
        else:
            return 0
    
    def bottom_risk(self,state):
        if state[1] >= -15 and state[1] <= -7.5 and state[0] >= -30 and state[0] <= -20:
            return 1
        else:
            return 0
        
    def close_risk(self,state):
        if state[1] >= -10 and state[1] <= 10 and state[0] >= -33 and state[0] <= -30:
            return 1
        if state[1] >= -10 and state[1] <= 10 and state[0] >= -20 and state[0] <= -17:
            return 1
        if state[1] >= 7.5 and state[1] <= 10 and state[0] >= -33 and state[0] <= -17:
            return 1
        if state[1] >= -10 and state[1] <= -7.5 and state[0] >= -33 and state[0] <= -17:
            return 1
        else:
            return 0

    
    def in_risk(self, state):
        if state[1] >= -7.5 and state[1] <= 7.5 and state[0] >= -30 and state[0] <= -20:
            return 1
        else:
            return 0

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

        self.action_sentence = f"{self.action_left_right_word} and {self.action_up_down_word} {direction}ly with magnitude {self.magnitude}"