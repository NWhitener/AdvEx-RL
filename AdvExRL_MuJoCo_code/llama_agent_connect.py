#!/usr/bin/env python3
import sys
from llama_cpp import Llama
import os 
from contextlib import redirect_stderr, redirect_stdout
from parser2 import Nav2Predicates

class llama_interact(): 
    def __init__(self): 
        self.parser = Nav2Predicates()
        self.model_path =  "/deac/csc/classes/csc790/bailwj20/advexRL_WB/llama.cpp/models/llama-2-7b-chat.Q4_K_M.gguf"
        self.chat_history = "I am an agent in a continuous 2D environment (in a square shape) that has a square obstacle in the middle, and a goal behind that obstacle, on the same y axis as the starting position. The starting space is on the left of the obstacle (dangerous) in the middle, with the goal on the far right side. I can move in any direction with [x, y] coordinates between -1 and 1. I will provide you with a text description of where I am currently, and where I have been previously. Give me the x and y coordinates of the action you think I should take, making sure to head towards the goal while avoiding the obstacle, if I am in the risk area, navigate me out. Only output x and y and no other text."
        self.replay_buffer_base = []
        self.important_buffer = []
        self.sentence = " "
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self.llm = Llama(model_path=self.model_path, n_ctx=4096)
    def build_chat_hist(self): 
        print(len(self.replay_buffer_base))
        for item in self.replay_buffer_base:
            self.parser.action_left_right = item[1][0]
            self.parser.action_up_down = item[1][1]
            bin_state = self.parser.state_to_binary(item[0])
            self.parser.create_sentence_action()
            self.parser.calc_magnitude()
            self.sentence += f" I was in state {self.parser.translate_state(bin_state)} and I took action {self.parser.action_left_right} {self.parser.action_up_down} with magnitude {self.parser.magnitude}."
        for state, action, r in self.important_buffer:
            bin_state = self.parser.state_to_binary(state)
            self.parser.translate_state(bin_state)
            self.parser.action_left_right, self.parser.action_up_down = action
            self.parser.calc_magnitude()
            self.sentence += (
                f"(IMPORTANT) I was in state {self.parser.translate_state(bin_state)} "
                f"took action {action[0]:.2f},{action[1]:.2f} => reward {r:.2f}."
            )
    def ask_question(self, question): 
        self.build_chat_hist()
        print("--------------------------")
        self.chat_history += f"{self.sentence + question} Only output x and y in the form x y, no other text\nAssistant: "
    
        resp = self.llm(
            prompt=self.chat_history,
            max_tokens=200,
            stop=["\nUser:"]
        )
        answer = resp["choices"][0]["text"].strip()
        print("Question: ", question)
        print("RESPONSE:", answer, "\n")
        self.sentence = ""
        self.chat_history = "I am an agent in a continuous 2D environment (in a square shape) that has a square obstacle in the middle, and a goal behind that obstacle, on the same y axis as the starting position. The starting space is on the left of the obstacle (dangerous) in the middle, with the goal on the far right side. I can move in any direction with [x, y] coordinates between -1 and 1. I will provide you with a text description of where I am currently, and where I have been previously. Give me the x and y coordinates of the action you think I should take, making sure to head towards the goal while avoiding the obstacle, if I am in the risk area, navigate me out. Only output x and y and no other text."
    
        return answer


if __name__ == '__main__': 
    attempt1 = llama_interact() 
    attempt1.ask_question('Hello, What is the capital of France')