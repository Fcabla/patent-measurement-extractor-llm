'''
Script to generate synthetic train data for finetuning the model.
'''

from config import config 
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

try:
    from secret import open_ai_key
except:
    raise Exception(
        "src/secret.py not found. Make sure that you have created the following file: src/secret.py with your api_key in a variable called open_ai_key."
        "You can also rename the file src/secret_template.py into src/secret.py "
    )
model = ChatOpenAI(model_name="gpt-3.5-turbo",
                        temperature= 0.7, # we want the model to be creative
                        max_tokens= config['gpt_max_tokens'], #2000,
                        #frequency_penalty= config['gpt_frequency_penalty'], #0,
                        #presence_penalty= config['gpt_presence_penalty'], #0,
                        openai_api_key=open_ai_key)

generation_prompt = """
Generate {n_times} paragraphs related to patents descriptions that contains at least a measurement. Along with the paragraphs you will need to output the measurement in a json format.format

A measurement contains 4 components: 
element: Specific entity or material being measured within a document. It represents the subject or object of the measurement.
property: Characteristic or property of the measure element that is being quantified or described. It provides additional context or specifications about the measure element. For example the length, density, diameter, etc.
value: NUMERICAL or quantitative value associated with the e measure element and attribute. MUST CONTAIN NUMERICAL VALUES. It can not be empy, not specified, NA or N/A
unit: Unit of measurement associated with the measure value. It provides the standardized reference for interpreting and comparing the measure values. It can not be empy, unitless, not specified, NA or N/A

Input: The resulting BaCO3 had a crystallite size of between about 20 and 40 nm
Output: {{'element': 'BACO3', 'property': 'crystallite size', 'value': 'between 20 and 40', 'unit': 'nm'}}

Input:
""".format(n_times=config["number_generations_prompt"])

messages = [
    HumanMessage(content=generation_prompt)
]

# Define the resulting object
generated_pantents = {'generated_pantents': []}

# Repeat repeat_generation_process times
for i in range(config['repeat_generation_process']):
    print(i)
    # Query the model and get results
    prompt_result = model(messages)
    prompt_result = prompt_result.content
    # Split each \n\n
    generated_examples = prompt_result.split('\n\n')
    # For each split (generated instance)
    for example in generated_examples:
        # Create resulting object
        result = {}
        # Remove \n with spaces
        example=example.replace('\n',' ')
        # Split by Output so there are two splits (input and ouput)
        inp_out = example.split('Output: ')
        # Remove the input part and store results
        input_patent = inp_out[0].replace('Input: ','')
        output_llm = inp_out[1]
        result['prompt'] = input_patent
        result['completion'] = output_llm
        # Append example
        generated_pantents['generated_pantents'].append(result)

# Save results
with open(config['output_generated_pantents_json'], 'w', encoding='utf-8') as f:
    json.dump(generated_pantents, f, ensure_ascii=False, indent=4)