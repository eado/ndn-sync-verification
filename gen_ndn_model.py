import openai
import sys
import os

api_key = open(os.path.join(os.getcwd(),"api_key.txt")) .read()

class GPT4:
    def __init__(self, system_prompt, temperatrue=0.0):
        openai.api_key = api_key
        self.messages = list()
        self.temperature = temperatrue
        self.system_prompt = system_prompt
        system_message = {
            'role': 'system',
            'content': system_prompt
        }    
        self.messages.append(system_message)
    
    def print_system_message(self):
        print("System message:", self.system_prompt)
        
    def get_chat_result(self, user_prompt):
        user_message = {
            'role': 'user',
            'content': user_prompt
        }
        self.messages.append(user_message)
        
        completion_text = openai.chat.completions.create(
            model = "gpt-4o",
            temperature = self.temperature,
            messages = self.messages
        )
        
        response = completion_text.choices[0]
        
        if response.finish_reason != 'stop':
            sys.exit(
                f'Model did not finish properly: {response.finish_reason}')
        
        gpt_message = {
            'role': 'assistant',
            'content': response.message.content
        }
        self.messages.append(gpt_message)
        
        return gpt_message['content']   

def read(filename):
    with open(filename) as f:
        return f.read()

# Set up model
cwd = os.getcwd() 
context_path = os.path.join(cwd,"llm-context.txt") 
sys_prompt = read(context_path)
model = GPT4(sys_prompt)

# Pass it prompt
prompt_path = os.path.join(cwd,"prompt.txt") 
prompt = read(prompt_path)
results = model.get_chat_result(prompt)

print(results)
