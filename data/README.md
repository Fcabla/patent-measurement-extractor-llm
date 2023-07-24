# Data
In this folder you will find the data that has been used. Since it surpases the maximum capacity that github allows, there will be detailed instructions on how to re-download this data.

## About the data source
The data source is the [us patents webpage](https://bulkdata.uspto.gov/data/patent/officialgazette/2023/). 

From the data source we are interestend on the data regarding **granted pantents full texts without images**.

If you want to execute the proposed solution, please access the website mentioned above, locate the section `Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)`, select the year you are interested in, and download a ZIP file.

The patents are grouped by year, and for each year, there is a zip file containing the patents that have been granted each week. Each zip file compresses an XML file that concatenates all the patents that have been published and granted during that week.

## Used files and folder distribution
During the development of this work, the following patent files have been used:
- [ipg230103.xml](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2023/ipg230103.zip): This file has been used to extract examples for few-shot learning and to explore the data structure in general.

- [ipg221227.xml](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2022/ipg221227.zip): This file has been used to evaluate the developed system.

In this directory, there are two folders:
- **raw_data**: In this folder, you should place the XML file extracted from the downloaded ZIP file.

- **processed_data**: In this folder, the system will save the parsed data from the XML file in the raw_data folder.


## Useful links
- [Example](https://austingwalters.com/parsing-uspto-patents-to-create-a-dataset/) on how to parse patents
- [2023 Granted patents full text no images](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2023)
- [2022 Granted patents full text no images](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2022)
