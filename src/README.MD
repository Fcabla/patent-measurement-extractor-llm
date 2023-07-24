# Source code
In this directory you can find the source code of the approach that has been implemented. These files are listed below together with a short description.

- **config.py**: Configuration file where the parameters to be used during the whole execution of the code are chosen.

- **data_parser.py**: Script that reads a XML file with patents in it and parse them. Extracts the abstract, summary and detailed description of each patent and saves it in a json file.

- **first_approach.py**:

- **mpt_api.py**: Script that defines an local API for serving the MPT model.

- **llm_custom_wrapper.py**: Script that defines a custom langchain wrapper for our API with the MPT model.

- **prompts.py**: Script that contains prompt related stuff. Versions of the tested prompts and examples used for few-shot learning. The most important thing in this file is the **patent_examples**

- **input_examples.py**: Script that contains some text examples in order to test the model and prompt template. Debugging purposes.

- **create_train_data.py**

- **secret.py**: Script that contains the api key to open ai. Only needed if using openai models.
