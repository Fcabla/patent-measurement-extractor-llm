'''
Script containing the implementation of the tool to extract measurements from patent descriptions.
First the data is loaded, sampling is performed to reduce the number of patents to be processed, then the model is loaded.
Next we define the prompt template along with several examples (few-shot learning) from prompts.py.

For each patent, a text chunk is generated (text_chunk + prompt_template + examples ~= MAX TOKENS from model). 
Then, only the text chunks that contains a number will be feed into the model. Otherwise it is disregarded since it is assumed that there is no measure.
Finally the output of the model is parsed and validated. 
The validation consists in that the value must contain at least one number and the unit must be different from unitless, NA or similar.
'''

# Common imports
import random
import json
import re

# LLM related imports
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from kor import from_pydantic
from kor.extraction import create_extraction_chain

# My imports (from my files)
from llm_custom_wrapper import MPT_LLM
from config import config
import time
from prompts import Patent_measurements, patent_examples
from input_examples import inp_examples

# 1. Load data
with open(config['output_processed_pantents_json'], 'r', encoding='utf-8') as f:
    patents = json.load(f)

# 2. Sample pantents.
# 2.1 Stablish a seed --> Important for code reproducibility
random.seed(a=config['data_selection_seed'])
if config['sample_patents_num'] > 0:
    # Sampling patents
    patents['patents'] = random.sample(patents['patents'],config['sample_patents_num'])

# 3. Load the model
if config['use_open_ai']:
    #     model_name="gpt-3.5-turbo", # Cheaper but less reliable
    try:
        from secret import open_ai_key
    except:
        raise Exception(
            "src/secret.py not found. Make sure that you have created the following file: src/secret.py with your api_key in a variable called open_ai_key."
            "You can also rename the file src/secret_template.py into src/secret.py "
        )
        exit()
    model = ChatOpenAI(model_name="gpt-3.5-turbo",
                        temperature= config['gpt_temperature'], #0,
                        max_tokens= config['gpt_max_tokens'], #2000,
                        frequency_penalty= config['gpt_frequency_penalty'], #0,
                        presence_penalty= config['gpt_presence_penalty'], #0,
                        openai_api_key=open_ai_key)
else:
    model = MPT_LLM(url_model=config['server_url'])

# 4. Define the patent schema. Patent_measurements and patent_examples can be found in the prompts.py file.
# The patent schema will be the object that contains the template prompt with the examples and the parser
# to handle the LLM results
patent_schema, extraction_validator = from_pydantic(
    Patent_measurements,
    description="Identifies and extracts measurements, including measure elements, attributes, values, and units, from documents.",
    examples=patent_examples,
    many=True,
)
# 4.1 Create the chain. Merely an object to call when we want to query the LLM following the defined schema
chain = create_extraction_chain(model, patent_schema)

def chunk_filer(text):
    ''' 
    This function aims to optimize API calls to the LLM by filtering out chunks that do not contain numbers. 
    We are implementing a basic and straightforward filtering approach where chunks without numbers are excluded. 
    Our assumption is that every measurement always includes a number.
    For a more profesional environment this filtering should be more complete.
    '''
    flag = bool(re.search(r"\d+", text))
    return flag

def validate_llm_output(llm_output):
    ''' 
    Function that validates the LLM outputs.
    Basically we are checking that the results as we would check any user input.
    Value must contain a number and unit must not be unitless, NA or similar
    '''
    validated_results = []
    
    for lo in llm_output:
        if ('value' in lo) and ('unit' in lo):
            valid_flag = True
            # value
            # check if value contains a number
            if not re.search(r"\d+", lo['value']):
                valid_flag = False
                
            # unit
            if lo['unit'] in ['N/A', 'unitless', '', 'NA', 'not specified', '-']:
                valid_flag = False

            if valid_flag:
                validated_results.append(lo)
    return validated_results

# This is mainly for debugging and testing purposes
if 'execute_single_example':
    # Select one example
    debug_text = inp_examples[0]

    # Run extraction chain
    extracted = chain.predict_and_parse(text=debug_text)
    print(extracted)
    print('-'*20)
    print(extracted['data'])

    # Print the prompt used
    #prompt = chain.prompt.format_prompt(text=text).to_string()
    #print(prompt)
    exit()

# 5. Select the part of the patent to process.  Abstract, summary or detailed description
data_section = config['data_selection_section']
print(f"Processing the {data_section} section of the {len(patents['patents'])} patents to process")

# 6. Prepare resulting object and text splitter. The last is used to split the text into chunks
extraction_results = {
    'patents':[]
}
text_splitter = RecursiveCharacterTextSplitter(chunk_size = config['text_chunk_size'])

# 7. Process patents
# 7.1 For each patent
for patent in patents['patents']:
    # 7.2 Form the resulting object of 1 patent
    res = {
        'doc_id': patent['doc_id'],
        'data_section': data_section,
        'elements_processed': []
    }

    # 7.3 Form text chunks of the selected section of the patent
    text_document = ' '.join(patent[data_section])
    split_docs = text_splitter.create_documents([text_document])

    # 7.4 For each doc
    for sd in split_docs:
        # 7.5 Create empy list to store results and obtain the text from the chunk
        result = []
        validated_data = []
        text = sd.page_content
        skipped = True
        # 7.6 Filter the results. If there is a num then call the LLM
        if chunk_filer(text):
            skipped = False
            # 7.7 Call the LLM with the chain (template prompt with examples and parser)
            extracted = chain.predict_and_parse(text=text)
            result = extracted['data']
            if 'patent_measurements' in result:
                # 7.8 If the model has outputted something meaningful store the raw results and the validated ones (see validate_llm_output())
                result = result['patent_measurements']
                validated_data = validate_llm_output(result)
            else:
                # Sometimes the model response contains some unparseable elements
                # for example 5 measure attributes when we are expecting 4.
                # Mostly the unparseable elements are empty dicts because there was nothing to extract.
                # We could test and explore when and why this happens more carefully.
                print(result)

            # 7.9 Wait a cooldown time. Useful with API models who has apirates
            time.sleep(config['cooldown_time'])
        # 7.10 Save the extracted information about the single chunk into the resulting object
        res['elements_processed'].append({
            'text':text,
            'skipped': skipped,
            'extraction':result,
            'validated': validated_data
        })
    # 7.11 Save the extracted information about the single patent into the resulting object       
    extraction_results['patents'].append(res)

# 8. Save the resulting object with the raw extractions and the validated ones
with open(config['output_extracted_pantents_json'], 'w', encoding='utf-8') as f:
    json.dump(extraction_results, f, ensure_ascii=False, indent=4)

# 9. Save in a different file the resulting object with just the validated extractions.
# If there are no valid extractions then the chunk will be saved along with no measurements
cleaned_extraction_results = {'patents':[]}
for patent in extraction_results['patents']:
    cleaned_elements_processed = []
    for ep in patent['elements_processed']:
        # Check if the chunk has been skipped. If not save the information
        if not ep['skipped']:
            cleaned_section = {
                'text': ep['text'],
                'validated': ep['validated']
            }
            cleaned_elements_processed.append(cleaned_section)
            
    cleaned_patent = {
        'doc_id':patent['doc_id'],
        'data_section':patent['data_section'],
        'elements_processed': cleaned_elements_processed
    }

with open(config['output_extracted_pantents_valid_json'], 'w', encoding='utf-8') as f:
    json.dump(extraction_results, f, ensure_ascii=False, indent=4)

# 10. Extract information about the experiment. 
# Num of patents processed, text chunks, filtered text chunks, raw extractions and valid measurements.
patents_num = len(extraction_results['patents'])
text_chunks_total = 0
chunks_evaluated = 0
num_raw_extractions = 0
num_valid_extractions = 0
for patent in extraction_results['patents']:
    text_chunks_total += len(patent['elements_processed'])
    for ep in patent['elements_processed']:
        num_raw_extractions += len(ep['extraction'])
        num_valid_extractions += len(ep['validated'])
        if not ep['skipped']:
            chunks_evaluated +=1

print(f'Number of patents analysed: {patents_num}')
print(f'Number of text chunks produced: {text_chunks_total}')
print(f'Number of text chunks after filtering (evaluated): {chunks_evaluated}')
print(f'Number of measurements extracted: {num_raw_extractions}')
print(f'Number of valid measurements extracted: {num_valid_extractions}')
