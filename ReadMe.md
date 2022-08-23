
## Installation

  

Following packages need to be installed before running the program

  

- pip install rdflib

  

## Steps to Run

  

Place the following files in same directry

- onto.dtd

- onto.xml

- assignment4.py

- TVSeries.owl

  

Next, Run the command to execute python files

- ***python assignment4.py***

  
  
  

After the program executed successfully, find the output file with triplets in ***output*** folder

- ***output.owl***

- ***Triples.txt***

  

Please note ***output.owl*** is new owl file with new added Triples.

***Triples.txt*** has new triples added

  
  

## Now Generate Inference

### Steps

- Open the output.owl in protege

- start resoner from following menu : ***Reasoner > Start reasoner***

- Export inferences : ***File > Export inferred axioms as Ontology***

- save the file as ***infer.owl***

- Run the following command:
***python infer.py***
- Find the new file generated in output folder
***Infer.txt***