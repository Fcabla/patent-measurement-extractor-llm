'''
Script that defines an local API for serving the MPT model.
This way we avoid loading the model each time we run the program, 
since the model load time is aroun 10 minutes.
'''

from typing import Any, Dict, Tuple
import warnings
from flask import Flask, jsonify, request
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import StoppingCriteria, StoppingCriteriaList
from config import config

# 1. Define the prompt structure. With this template the model results are much better since its similar to the data in the training process
INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
END_KEY = "### End"
INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
PROMPT_FOR_GENERATION_FORMAT = """{intro}

{instruction_key}
{instruction}

{response_key}
""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
)

class InstructionTextGenerationPipeline:
    ''' Definition of the pipeline for the MPT model. '''
    def __init__(
        self,
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        use_auth_token=None,
    ) -> None:
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
            #max_seq_len=2048
        )

        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
        )
        if tokenizer.pad_token_id is None:
            warnings.warn(
                "pad_token_id is not set for the tokenizer. Using eos_token_id as pad_token_id."
            )
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
        self.tokenizer = tokenizer

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval()
        self.model.to(device=device, dtype=torch_dtype)

        # Default arguments
        self.generate_kwargs = {
            "temperature": config['api_temperature'],
            "top_p": config['api_top_p'],
            "top_k": config['api_top_k'],
            "max_new_tokens": config['api_max_new_tokens'],
            "use_cache": config['api_use_cache'],
            "do_sample": config['api_do_sample'],
            "eos_token_id": self.tokenizer.eos_token_id,
            "pad_token_id": self.tokenizer.pad_token_id,
            "repetition_penalty": config['api_repetition_penalty'],  # 1.0 means no penalty, > 1.0 means penalty, 1.2 from CTRL paper
        }

    def format_instruction(self, instruction):
        ''' When prompt received, use template to adapt the prompt to the desired format. '''
        return PROMPT_FOR_GENERATION_FORMAT.format(instruction=instruction)

    def __call__(
        self, instruction: str, **generate_kwargs: Dict[str, Any]
    ) -> Tuple[str, str, float]:
        ''' Function that handles generation step (inference). '''
        s = PROMPT_FOR_GENERATION_FORMAT.format(instruction=instruction)
        input_ids = self.tokenizer(s, return_tensors="pt").input_ids
        input_ids = input_ids.to(self.model.device)
        gkw = {**self.generate_kwargs, **generate_kwargs}
        with torch.no_grad():
            output_ids = self.model.generate(input_ids, **gkw)
        # Slice the output_ids tensor to get only new tokens
        new_tokens = output_ids[0, len(input_ids[0]) :]
        output_text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return output_text

# 2. Define the API name
app = Flask(__name__)

# Initialize/LOAD the model and tokenizer (MPT)
gen_pipeline = InstructionTextGenerationPipeline(
    config['api_model_path'],
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    use_auth_token=None,
)
stop_token_ids = gen_pipeline.tokenizer.convert_tokens_to_ids(["<|endoftext|>"])
print('MODEL LOADED')

# Define a custom stopping criteria
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_id in stop_token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

@app.route('/generate', methods=['post'])
def generate():
    ''' Function that handles inputs from API. '''
    content = request.json
    instruction = content.get('text','')
    temperature = int(content.get('temperature',''))
    top_p = int(content.get('top_p',''))
    top_k = int(content.get('top_k',''))
    max_new_tokens = int(content.get('max_new_tokens',''))

    # Tokenize the input
    input_ids = gen_pipeline.tokenizer(
        gen_pipeline.format_instruction(instruction), return_tensors="pt"
    ).input_ids
    input_ids = input_ids.to(gen_pipeline.model.device)

    # Initialize the streamer and stopping criteria
    #streamer = TextIteratorStreamer(
    #    gen_pipeline.tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True
    #)
    stop = StopOnTokens()

    if temperature < 0.1:
        temperature = 0.0
        do_sample = False
    else:
        do_sample = True

    gkw = {
        **gen_pipeline.generate_kwargs,
        **{
            "input_ids": input_ids,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": do_sample,
            "top_p": top_p,
            "top_k": top_k,
            #"streamer": streamer,
            "stopping_criteria": StoppingCriteriaList([stop]),
        },
    }

    response = ""
    output = gen_pipeline.model.generate(**gkw)
    decoded_output = gen_pipeline.tokenizer.decode(output[0], skip_prompt=True, skip_special_tokens=True) 
    print(decoded_output)
    return jsonify({'generated_text': decoded_output})
    #stream_complete = Event()

    #def generate_and_signal_complete():
    #    generate.model.generate(**gkw)
    #    stream_complete.set()

    #t1 = Thread(target=generate_and_signal_complete)
    #t1.start()

    #for new_text in streamer:
    #    response += new_text
    #    yield response

if __name__ == '__main__':
    # Run locally
    app.run(host='0.0.0.0', port=5000)