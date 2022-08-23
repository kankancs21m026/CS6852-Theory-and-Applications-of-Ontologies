
import os
from rdflib import Graph,Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import  RDF, RDFS
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff



cwd=os.getcwd()
g1=Graph()
g2=Graph()
filename = cwd+"\\infer.owl"
filename2 = cwd+"\\TVSeries.owl"
g1.load(filename, format='xml')
g2.load(filename2, format='xml')
textfile = open("output/Infer.txt", "w")

for s, p, o in g2:
    notpresent=True
    for ((s1, p1, o1)) in g1:
        if(str(s)==str(s1) and str(p)==str(p1) and str(o)==str(o1)):
            notpresent=False
    if(notpresent):
        textfile.write("Subject: "+str(s)+ "\n")
        textfile.write("Predicate: "+str(p)+ "\n")
        textfile.write("Object: "+str(p)+ "\n")
        textfile.write("---------------------------------------------------------------------------------------------\n")    

textfile.close()

