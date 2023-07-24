# Result inspection and evaluation

The results can be checked in the `results/` folder. Inside this folder there is another folder called `results/stored_results/` where the results of the pipeline execution have been stored. 

We will mainly look at the [`results_extracted_patents.json`](results/stored_results/results_extracted_patents.json) file as it contains both the raw and valid extractions.

For this experiment it has been used:
- The ipg221227.xml file containing the patents.
- The GPT-3.5-Turbo model
    - Temperature: 0
    - Max tokens: 2000
    - Frequency penalty: 0
    - Presence penalty: 0
    - Temperature: 0
    - Max tokens: 2000
- We have processed the brief summaries (BRFSUM)
- We have splitted the text into chunks of size 1300 tokens
- Seed: 7
- Sample size: 100

Out of the 100 processed patents we have the following statistics:
- Number of text chunks produced: 933
- Number of text chunks after filtering: 431
- Measurements extracted: 1620
- Validated measures: 451

### Discussion
Based on the displayed statistics and manual inspection of the results, we can draw some conclusions about the performance of the proposed solution.

Regarding the text chunks, we can observe that with a simple straightforward filter, we can reduce the number of calls to the LLM API, avoiding 502 calls that would not have produced any results.

We can also see that there is a significant difference between the extracted measurements and the validated measurements. Only 451 out of the 1620 extracted measurements are valid. It is important to note that a valid measurement has been defined as one where at least one number appears in the value, and the unit is not 'NA', 'unitless', or similar. This means that the LLM extracts measurements where it shouldn't, generating measurements that do not follow the defined schema or are incomplete. For example:

```javascript
// Example of error 1: Unit contains N/A --> not valid. Value does not contain a number but could be valid
{"element": "administration","property": "frequency","value": "once or twice a day","unit": "N/A"}
// Example of error 2: Value does not contain a number.
{"element": "dextrorphan","property": "plasma level","value": "lower","unit": "than the level achieved by administering the same amount of dextromethorphan without threohydroxybupropion for ten consecutive days."}
// Example of error 3: Does not have sense. Unit NA and value does not contain a number
{"element": "hole portions","property": "shape","value": "polygonal prism or oval columnar","unit": "NA"},
```
Something interesting that we can observe from the first example is that, even though it would make sense: `'value':'once or twice','unit':'day'`, it would be considered invalid since the value does not contain a number. This indicates that we should improve both our validation process and the way we filter text chunks.

Another interesting case is the following:
```javascript
//Last sentence of the text chunk is unfinished:
//The pump also includes an impeller suspended within the housing wherein a first gap between the impeller and a top portion of the housing is in a first range between about 0.05 mm and"
 {"element": "impeller","property": "gap between impeller and top portion of housing","value": "between 0.05 and N/A","unit": "mm"}
```
It can be observed that by dividing the text into chunks, we can separate important information regarding a measurement.

In general, the extracted and validated measurements are usually correct. However, there are cases where a measurement is considered valid but doesn't make much sense, for example:
```javascript
// Error 1 in validated data: element or property does not fit well the schema 
{"element": "reduction","property": "expired carbon monoxide levels","value": "at least 10","unit": "% greater reduction"}
// Error 2 in validated data: property missing
{"element": "duration of treatment","property": "","value": "at least 5","unit": "weeks"}
```
Based on a manual inspection, these errors are quite rare. We can see that in the first case, `'reduction'` is treated as the element, which doesn't make much sense. In the second case, the element could be `'treatment'`, and instead of being null, the property should be `'duration'`.

It has become evident that we should handle the output of the LLM with great care, treating it as if it were user input.

Based on all the feedback from this manual evaluation, here are some possible points for improvement:

1. Improve the filtering of text chunks to further reduce API calls while avoiding the exclusion of potential measurements. We could explore techniques like `'retrieval-augmented prompting'` or store text chunks in a vector database like ChromaDB and extract only those that could potentially contain measurements. How would the query to retrieve candidates from such a database be formulated?

2. Enhance the validation of extracted measurements. So far, we have applied a simple filtering approach, but it is likely that we are missing some valid measurements.

3. Continue experimenting with different prompts. This involves changing the template instructions as well as modifying, increasing, or decreasing the provided examples. I am particularly interested in investigating how including examples where a text fragment without measurements produces empty results would affect the system. The few times I tried including such examples, the quality of the results significantly declined. However, I believe it could help eliminate measurements generated by the model that are not valid.

4. One of the most significant improvements would be to perform fine-tuning on the model. This way, there would be no need to include instructions and examples in the prompt, making the system more cost-effective. It also yields more robust results as the model learns the expected output format through fine-tuning. The challenge with this approach lies in obtaining a sufficient amount of annotated data. I am currently exploring the generation of synthetic data for this purpose in the file [`src/generate_train_data.py`](src/generate_train_data.py).

These improvements aim to enhance the overall performance and reliability of the system.


