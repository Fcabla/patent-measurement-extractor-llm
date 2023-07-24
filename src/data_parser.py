''''
Script that reads a XML file with patents in it and parse them. Extracts the abstract, summary and detailed description of each patent and saves it in a json file.
'''

from bs4 import BeautifulSoup, Comment, element
import json
import re
from config import config
# GLOBALS
#raw_data_path = 'data/raw_data/ipg230103.xml'
raw_data_path = config['raw_data_patents_path']
output_path = config['output_processed_path']
xml_separator = config['xml_separator']

# 1. OPEN FILE
with open(raw_data_path, 'r') as file:
        xml_text = file.read()

# 2. SPLIT SINGLE XML INTO MULTIPLE PATENTS
xml_pantents = xml_text.split(xml_separator)
xml_pantents = [xml_separator + xp for xp in xml_pantents]
print(len(xml_pantents))
xml_pantents = xml_pantents[1:]

# 3. Prepare resulting object
patents = {
    'patents': []
}

# 4. Save the patents individually if the user wants to. Multiple xml files in the output processed foled
if config['save_indiv_patents']:
    for i, patent in enumerate(xml_pantents):
        # save patent
        file_name = f'patent_{i}.xml'
        file_path = config['output_processed_path'] + file_name
        with open(file_path, 'w') as dest_file:
            dest_file.write(patent)

# 5. For each patent
for patent in xml_pantents:
    # 5.1 Parse patent
    bs = BeautifulSoup(patent, features="xml") 
    #publication_title = bs.find('invention-title').text
    # 5.2 Extract specific information (abstract, doc_id, description)
    abstract = bs.find('abstract')
    if abstract:
        abstract = abstract.text
        abstract = abstract.replace('\n',' ')
        abstract = re.sub(r'\s+', ' ',abstract)
        abstract = [abstract]
    else:
        abstract = []
        
    doc_id = bs.find('document-id')
    if doc_id:
        doc_id = doc_id.text
    description = bs.find('description')

    # 5.3 Prepare single patent resulting object
    pantent_data = {
        'doc_id': doc_id,
        #'publication_title': publication_title,
        'abstract': abstract,
        #'description': description,
        'BRFSUM': [],
        'DETDESC': [],
        #'RELAPP': [],
        #'GOVINT': [],
        #'brief-description-of-drawings': []
    }
    # descriptions_types = ['BRFSUM','DETDESC','RELAPP','GOVINT']
    # 5.4 If there is a description extract each <p> component.
    # Exclude <headings> and <math> objects
    if description:
        flag = False
        for d in description:
            if isinstance(d,element.XMLProcessingInstruction):
                desc_type = d.split(' ')[0]
                if 'end="lead"' in d:
                    flag = True
                elif 'end="tail"' in d:
                    flag = False
            if flag:
                if desc_type in pantent_data:
                    if isinstance(d, element.Tag):
                        children = list(d.children)
                        if d.name == 'p' and '<maths' not in children:
                            text_element = d.text
                            # replace extra \n with spaces
                            text_element = text_element.replace('\n',' ')
                            # transform multiple spaces into a single one
                            text_element = re.sub(r'\s+', ' ',text_element)
                            # remove trailing extra spaces
                            text_element = text_element.strip()
                            pantent_data[desc_type].append(text_element)

    # 6. Remove <p> paragraphs containing just '' or '\n'
    pantent_data['BRFSUM'] = [pd for pd in pantent_data['BRFSUM'] if pd not in ['','\n']]
    pantent_data['DETDESC'] = [pd for pd in pantent_data['DETDESC'] if pd not in ['','\n']]

    # 7. Add extracted patent if at least some info
    if pantent_data['BRFSUM'] or pantent_data['DETDESC'] or pantent_data['abstract']:
        patents['patents'].append(pantent_data)

# 8. Save extracted information
print(len(patents['patents']))
with open(config['output_processed_pantents_json'], 'w', encoding='utf-8') as f:
    json.dump(patents, f, ensure_ascii=False, indent=4)

print(f'File saved {config["output_processed_pantents_json"]}')