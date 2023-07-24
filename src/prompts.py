'''
In this script you can find all the prompts templates that we are going to use. 
It is located in a different file because this templates can be quite long and maybe they will
be accessed from different python files.
'''
from pydantic import BaseModel, Field, validator, ValidationError

# Defines the data schema that the LLM has to follow when outputting the result. 
# This includes the elements that we are looking with the type and a description of each one.
class Patent_measurements(BaseModel):

    element: str = Field(
        description="Specific entity or material being measured within a document. It represents the subject or object of the measurement."
    )
    property: str = Field(
        description="Characteristic or property of the measure element that is being quantified or described. It provides additional context or specifications about the measure element. For example the length, density, diameter, etc."
    )
    value: str = Field(
        description="NUMERICAL or quantitative value associated with the e measure element and attribute. MUST CONTAIN NUMERICAL VALUES. It can not be empy, not specified, NA or N/A"
    )
    unit: str = Field(
        description="Unit of measurement associated with the measure value. It provides the standardized reference for interpreting and comparing the measure values. It can not be empy, unitless, not specified, NA or N/A"
    )


# Defines a set of examples to perform few-shot learning.
# TODO: Explore the consequences of adding examples with empty results.
#Output format: {'element': 'x', 'property': 'x', 'value': 'x', 'unit': 'x'}
patent_examples=[
        (
            "In one embodiment, the nitrogen oxide storage material comprises alkaline earth material Supported on ceria particles having a crystallite size of 10 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.",
            [
                {"element": "alkaline earth material", "property": "crystallite size", "value": "10", "unit": "nm"},
                {"element": "alkaline earth material", "property": "crystallite size", "value": "between 20 and 40", "unit": "nm"}
            ]
        ),
        (
            "The invention provides a composition comprising the following: A) a first polymer composition comprising an anhydride functionalized ethylene-based polymer, and optionally, an ethylene-based polymer; B) a filler; and where in the anhydride functionalized ethylene-based polymer has a density from 0.855 g/cc to 0.900 g/cc and a melt viscosity, at 177° C., from 1000 to 50,000 cP.",
            [
                {"element": "anhydride functionalized ethylene-based polymer", "property": "density", "value": "from 0.855 to 0.900", "unit": "g/cc"},
                {"element": "anhydride functionalized ethylene-based polymer", "property": "melt viscosity at 177° C", "value": "from 1000 to 50,000", "unit": "cP"}
            ]
        ),
        (
            "In one embodiment of the invention, the novel energy storage device comprises a cathode with a thickness of approximately 50 micrometers, an anode with a surface area of about 1 square centimeter, and an electrolyte solution with a concentration of 0.5 moles per liter. The device further includes a separator membrane with a pore size of 10 nanometers and a specific resistance of 0.1 ohm-centimeters. These specific measurements and parameters contribute to the enhanced performance and efficiency of the energy storage device, providing improved power density and cycle life.",
            [
                {"element": "cathode", "property": "thickness", "value": "approximately 50", "unit": "micrometers"},
                {"element": "anode", "property": "surface area", "value": "1", "unit": "square centimeter"},
                {"element": "electrolyte solution", "property": "concentration", "value": "0.5", "unit": "moles per liter"},
                {"element": "separator membrane", "property": "pore size", "value": "10", "unit": "nanometersr"},
                {"element": "separator membrane", "property": "specific resistance", "value": "0.1", "unit": "ohm-centimeters"},
            ]
        ),
        (
            "Styrene resin particles having an average particle diameter of 8 μm, an average value of the 10% compressive elastic modulus of 3,080 MPa, and a variation coefficient of 30.5% were used as the base particles. In addition, silver-coated resin particles were produced in the same manner as in Present Invention Example 1.",
            [
                {"element": "Styrene resin particles", "property": "average particle diameter", "value": "8", "unit": "μm"},
                {"element": "Styrene resin particles", "property": "average value of compressive elastic modulus", "value": "10% of 3,080", "unit": "MPa"},
            ]
        ),
        #(
        #    "A heating ventilation, and/or air conditioning (HVAC) system includes a support structure having a mounting rail, a first mounting bracket coupled to the mounting rail and configured to be adjustably positioned along a first axis of the mounting rail, and a second mounting bracket directly coupled to the first mounting bracket. The second mounting bracket is configured to support a fan motor mounted thereto, the second mounting bracket is configured to be adjustably positioned along a second axis of the first mounting bracket, and the second axis of the first mounting bracket is transverse to the first axis of the mounting rail",
        #    [
        #        {"element": "", "property": "", "value": "", "unit": ""},
        #    ]
        #),
        (
            "For example, the recycled powder can be a recycled polyamide 12 (rPA12) powder with an average particle diameter of less than 100 micrometers. Also, the least one foam reactant can be a polyol reactant and an isocyanate reactant such that a polyurethane foam matrix with recycled rPA12 filler material is formed.",
            [
                {"element": "recycled polyamide 12 (rPA12) powder", "property": "average particle diameter", "value": "less than 100", "unit": "micrometers"},
            ]
        ),
]

# From this point only old versions. Nothing to look up for here.
template= """

    Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any propertys that do not appear in the schema shown below.\n
    {type_description}\n
    {format_instructions}\n

"""

template = """
"Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any propertys that do not appear in the schema shown below. If there is any el

```TypeScript

patent: { // Information about the measurements in a patent description
 element: string // The entity or element that is being measured. For example a plane, a plant, a quemical compound
 property: string // The property of an entity or element that is being measured. For example the length, density, diameter, 
etc.
 value: string // Numerical value, values or range of values of the measured element.
 unit: string // The unit of measurement that is used to represent the magnitude of a quantity.
}
```


Please output the extracted information in CSV format in Excel dialect. Please use a | as the delimiter. 
 Do NOT add any clarifying information. Output MUST follow the schema above. Do NOT add any additional columns that do not appear in the schema.



Input: In one embodiment, the nitrogen oxide storage material comprises alkaline earth material Supported on ceria particles having a crystallite size of 10 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.
Output: element|property|value|unit\r
alkaline earth material|crystallite size|10|nm\r
alkaline earth material|crystallite size|between 20 and 40|nm\r

Input: The invention 
provides a composition comprising the following: A) a first polymer composition comprising an anhydride functionalized ethylene-based polymer, and optionally, an ethylene-based polymer; B) a filler; and where in the anhydride functionalized ethylene-based polymer has a density from 0.855 g/cc to 0.900 g/cc and a melt viscosity, at 177\u00b0 C., from 1000 to 50,000 cP.
Output: element|property|value|unit\r
anhydride functionalized ethylene-based polymer|density|from 0.855 to 0.900|g/cc\r
anhydride functionalized ethylene-based polymer|melt viscosity at 177\u00b0 C|from 1000 to 50,000|cP\r

Input: Styrene resin particles having an average particle diameter of 8 \u03bcm, an average value of the 10% compressive elastic modulus of 3,080 MPa, and a variation coefficient of 30.5% were used as the base particles. In addition, silver-coated resin particles were produced in the same manner as in Present Invention Example 1.
Output: element|property|value|unit\r
Styrene resin particles|average particle diameter|8|\u03bcm\r
Styrene resin particles|average value of compressive elastic modulus|10% of 3,080|MPa\r

Input: A heating ventilation, and/or air conditioning (HVAC) system includes a support structure having a mounting rail, a first mounting bracket coupled to the mounting rail and configured to be adjustably positioned along a first axis of the mounting rail, and a second mounting bracket directly coupled to the first mounting bracket. The second mounting 
bracket is configured to support a fan motor mounted thereto, the second mounting bracket is configured to be adjustably positioned along a second axis of the first mounting bracket, and the second axis of the first mounting bracket is transverse to the first axis of the mounting rail
Output: element|property|value|unit\r
|||\r

Input: For example, the recycled powder can be a recycled polyamide 12 (rPA12) powder with an average particle diameter of less than 100 micrometers. Also, the least one foam reactant can be a polyol reactant and an isocyanate reactant such that a polyurethane foam matrix with recycled rPA12 filler material is formed.
Output: element|property|value|unit\r
recycled polyamide 12 (rPA12) powder|average particle diameter|less than 100|micrometers\r

Input: The aforementioned photographs and following observations and measurements describe plants grown during the spring in 1.5-liter containers in an outdoor nursery in Heerhugowaard, The Netherlands and under cultural practices typical of commercial Primula production. During the production of the plants, day temperatures ranged from 10\u00b0 C. to 20\u00b0 C. and night temperatures ranged from 10\u00b0 C. to 13\u00b0 C.
Output:"
"""