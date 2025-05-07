Parsers: 

Included in this folder are two seperate parsers. The first parser (parser.py) is an early attempt at 
parsing the state/action into a textual dicsription. It includes naive descriptions, such as Bottom Left, 
or that the agent moved left and up moderately. This was the initial attempt at parsing and should be considered 
defunct. The second parser (parser2.py) combines the action parsing ability of the parser, with the 
state parsing of the XSRL method. 


LLama Agent Connect: 

llama_agent_connect.py is the class that is used to invite interactions between the agent and the LLM. 
The llama-2-7b-chat model is utilized, and functions to build chat history, and ask questions. 

Safety Trainier: 

The LLM was then leveraged in the safety_trainer.py. The LLM is leveraged in the rollout trajectory