'''
Script that defines a custom langchain wrapper for our API with the MPT model.
There is also a client part so we can test and speak with the model.
I have used this tutorial: https://python.langchain.com/en/latest/modules/models/llms/examples/custom_llm.html
'''

from langchain.llms.base import LLM
import requests
import json
from typing import Any, Mapping, Optional, List
import colorama
from config import config

# Load API url
SERVER = config['server_address']
URL = config['server_url']

class MPT_LLM(LLM):
    ''' Definition of our custom wrapper for the MPT. We need to define at least the call function. '''
    url_model: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        ''' Get the identifying parameters.'''
        return {"url_model": self.url_model}

    def _call(
        self,
        prompt:str,
        temperature:float=config['client_temperature'],
        top_p:int=config['client_top_p'],
        top_k:int=config['client_top_k'],
        max_new_tokens:int=config['client_max_new_tokens'],
        stop: Optional[List[str]] = None
    ):
        ''' 
        Function that defines what to do when the model is called for inference.
        In this case the function will call the api with the input prompt.
        '''
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
            
        data = {
        'text': prompt,
        'temperature': temperature, 
        'top_p': top_p, 
        'top_k': top_k, 
        'max_new_tokens': max_new_tokens,
        }
        
        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        response = requests.post(URL, data=json.dumps(data), headers=headers)
        return response.json()['generated_text']

def instruction_client(model):
    ''' 
    Function for quick interaction with the model. 
    This is more for a debugging purpose but it can work as a client for our model.
    '''
    history = ''
    while True:
        inp = input('>>> ')
        #context = history + PROMPTER_TOK + inp + END_TOK + ASSISTANT_TOK
        history += inp
        output = model(prompt=inp)
        latest_response = output.split('### Response:')[-1]
        history += latest_response
        print(colorama.Fore.CYAN + latest_response + colorama.Style.RESET_ALL)

def main():
    ''' 
    If this script is executed, the client will be launched.
    The normal use is to import the MPT_LLM class from other script
    '''
    model = MPT_LLM(url_model=URL)
    instruction_client(model)

if __name__ == '__main__':
    main()
