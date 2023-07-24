'''
Configuration file where the parameters to be used during the whole execution of the code are chosen.
'''
config = {
    # data_parser.py
    # --------------
    'raw_data_patents_path': 'data/raw_data/ipg221227.xml', # 'data/raw_data/ipg230103.xml' # 'data/raw_data/ipg221227.xml'
    'save_indiv_patents': False,    # Store the concatenated patents individually in the output_processed_path
    'output_processed_path': 'data/processed_data/',    # Destination folder of the processed patents (individual or json)
    'output_processed_pantents_json': 'data/processed_data/extracted_patents_ipg221227.json',   # 'data/processed_data/extracted_patents_ipg230103.json' # 'data/processed_data/extracted_patents_ipg221227.json'
    'xml_separator': '<?xml version="1.0" encoding="UTF-8"?>',  #   String that states the start of an XML file. Useful for splitting the concatenated patents from raw_data_patents_path

    # model api mpt_api.py
    # --------------------
    'api_model_path': 'mosaicml/mpt-7b-instruct', # Select the model to use if going for a local model
    'api_temperature': 0.5, # Default value hyperparameter for temperature
    'api_top_p': 0.92,  # Default value hyperparameter for top p
    'api_top_k': 0, # Default value hyperparameter for top k
    'api_max_new_tokens': 512,  # Default value hyperparameter for maximum new tokens. Max len output
    'api_use_cache': True,  # Default value hyperparameter for using cache. Useful to save resources in local isntallation
    'api_do_sample': True,  # Default value hyperparameter for sampling
    'api_repetition_penalty': 1.1,  # # Default value hyperparameter for repetition penalty. 1 means no penalty, > 1.0 means penalty

    # model wrapper llm_custom_wrapper.py
    # -----------------------------------
    'server_address': '192.168.1.66',   # Address where the model is deployed
    'server_url': 'http://192.168.1.66:5000/generate', #    URL to query deployed model. http://{SERVER}:5000/generate
    'client_temperature':0,   # Client side hyperparameter temperature.
    'client_top_p':1,   # Client side hyperparameter top p.
    'client_top_k':0,   # Client side hyperparameter top k.
    'client_max_new_tokens':256,    # Client side hyperparameter for max new tokens.

    # first_approach
    # ------------------------
    'sample_patents_num': 100,  # If sample = 0 -> no sampling
    'data_selection_seed': 7,   # Useful for reproducibility
    'use_open_ai': True,    # Use openai models or MPT
    'gpt_temperature':0,    # Temperature param for GPT3.5-turbo model. IMPORTANT to be 0 so it can not invent things.
    'gpt_max_tokens':2000,  # Max tokens for GPT3.5-turbo model
    'gpt_frequency_penalty':0,  # Frequency penalty for GPT3.5-turbo model
    'gpt_presence_penalty':0,   # Presence penalty for GPT3.5-turbo model
    'execute_single_example': True, # Test the model with one of the examples from example.py. If false, the model will run with the whole sample of patents.
    'data_selection_section': 'BRFSUM', # Part of the data to process. Possible values are: 'abstract', 'BRFSUM', 'DETDESC'
    'text_chunk_size': 1300,    # Text chunk size (text_chunk + prompt_template + examples ~= MAX TOKENS from model).
    'output_extracted_pantents_json': 'results/results_extracted_patents.json', # Output file with the extracted patents in json format
    'output_extracted_pantents_valid_json': 'results/results_extracted_patents_valid.json', # Output file with the extracted patents that are valid in json format
    'cooldown_time': 0.5,    # Seconds to wait after a successfult query. Check the model rate limit

    # generate train data
    # ------------------------
    'output_generated_pantents_json': 'results/generated_pantents.json',
    'number_generations_prompt': 5, # Generate 5 examples each query
    'repeat_generation_process': 10 # Repeat x times the query
}