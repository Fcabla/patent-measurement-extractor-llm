# Prompt explanation
This file shows an example of a prompt consisting of the **kor** library template, the schema of the desired result object, some examples and the text to be analysed.
The prompt 

The structure of the prompt is as follows:
1. Instructions on the target of the model
2. Outline of the information to be extracted.
3. Instructions on how to generate the result (format)
4. Example 1
5. Example 2
6. Example 3
7. Example 4
8. Example 5
9. Patent text to be analysed

Separators (---) have been added between the examples for clarity, but in the final prompt they do not appear.

## Prompt example
"Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.

```TypeScript
patent: { // Information about the measurements in a patent description
 measure_element: string // The entity or element that is being measured. For example a plane, a plant, a quemical compound
 measure_attribute: string // The attribute of an entity or element that is being measured. For example the length, density, diameter, 
etc.
 measure_value: string // Numerical value, values or range of values of the measured element.
 measure_unit: string // The unit of measurement that is used to represent the magnitude of a quantity.
}
```

Please output the extracted information in CSV format in Excel dialect. Please use a | as the delimiter. 
Do NOT add any clarifying information. Output MUST follow the schema above. Do NOT add any additional columns that do not appear in the schema.

---
Input: In one embodiment, the nitrogen oxide storage material comprises alkaline earth material Supported on ceria particles having a crystallite size of 10 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.

Output: measure_element|measure_attribute|measure_value|measure_unit\r
alkaline earth material|crystallite size|10|nm\r
alkaline earth material|crystallite size|between 20 and 40|nm\r

---
Input: The invention 
provides a composition comprising the following: A) a first polymer composition comprising an anhydride functionalized ethylene-based polymer, and optionally, an ethylene-based polymer; B) a filler; and where in the anhydride functionalized ethylene-based polymer has a density from 0.855 g/cc to 0.900 g/cc and a melt viscosity, at 177\u00b0 C., from 1000 to 50,000 cP.

Output: measure_element|measure_attribute|measure_value|measure_unit\r
anhydride functionalized ethylene-based polymer|density|from 0.855 to 0.900|g/cc\r
anhydride functionalized ethylene-based polymer|melt viscosity at 177\u00b0 C|from 1000 to 50,000|cP\r

---
Input: Styrene resin particles having an average particle diameter of 8 \u03bcm, an average value of the 10% compressive elastic modulus of 3,080 MPa, and a variation coefficient of 30.5% were used as the base particles. In addition, silver-coated resin particles were produced in the same manner as in Present Invention Example 1.

Output: measure_element|measure_attribute|measure_value|measure_unit\r
Styrene resin particles|average particle diameter|8|\u03bcm\r
Styrene resin particles|average value of compressive elastic modulus|10% of 3,080|MPa\r

---
Input: A heating ventilation, and/or air conditioning (HVAC) system includes a support structure having a mounting rail, a first mounting bracket coupled to the mounting rail and configured to be adjustably positioned along a first axis of the mounting rail, and a second mounting bracket directly coupled to the first mounting bracket. The second mounting 
bracket is configured to support a fan motor mounted thereto, the second mounting bracket is configured to be adjustably positioned along a second axis of the first mounting bracket, and the second axis of the first mounting bracket is transverse to the first axis of the mounting rail

Output: measure_element|measure_attribute|measure_value|measure_unit\r
|||\r

---
Input: For example, the recycled powder can be a recycled polyamide 12 (rPA12) powder with an average particle diameter of less than 100 micrometers. Also, the least one foam reactant can be a polyol reactant and an isocyanate reactant such that a polyurethane foam matrix with recycled rPA12 filler material is formed.

Output: measure_element|measure_attribute|measure_value|measure_unit\r
recycled polyamide 12 (rPA12) powder|average particle diameter|less than 100|micrometers\r

---
Input: The aforementioned photographs and following observations and measurements describe plants grown during the spring in 1.5-liter containers in an outdoor nursery in Heerhugowaard, The Netherlands and under cultural practices typical of commercial Primula production. During the production of the plants, day temperatures ranged from 10\u00b0 C. to 20\u00b0 C. and night temperatures ranged from 10\u00b0 C. to 13\u00b0 C.

Output:"
"""

