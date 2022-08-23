#!/usr/bin/env python
# coding: utf-8

# In[29]:


import os
from rdflib import Graph,Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import  RDF, RDFS


# In[30]:


cwd=os.getcwd()


# ### Fetch data from XML

# In[31]:


import xml.etree.ElementTree as ET

# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('onto.xml')


# Get data from tags
genres=[]
locations=[]
episodes=[]
awardNom=[]
songs=[]
awardWin=[]
casts=[]
crew=[]

root = tree.getroot()
for child in root:
    #All necessary details under info element
    if(child.tag=='info'):
        #fetch all genres
        for listing in root.findall(child.tag+"/genres/type"):
            #genres = listing.find('type')
            #print(listing.tag)
            genres.append(listing.text)
            
            
        for listing in root.findall(child.tag+"/songs/song"):
            title = listing.find("title")
            singers=listing.findall("singers/singerid")             
            songs.append([title.text,[singers[0].text]])
        #fetch all location 
        for listing in root.findall(child.tag+"/shooting-location/location"):
            #genres = listing.find('type')
            #print(listing.tag)
            locations.append(listing.text)
        #fetch all episodes    
        for listing in root.findall(child.tag+"/seasons/season"):    
            eps = listing.findall('episodes/episode/title')          
            ep=[]
            for i in eps:
                ep.append(i.text)
            episodes.append(ep)
    #All Casts details     
    if(child.tag=='cast'):
        #fetch all genres
        for listing in root.findall(child.tag+"/actor/person"):
            name = listing.find('name')
            name = name.text
            personId = listing.get('personId')
            hireby = listing.get('hiredby')
            casts.append([name,personId,hireby,'Actor'])
            
        for listing in root.findall(child.tag+"/actress/person"):
            name = listing.find('name')
            name = name.text
            personId = listing.get('personId')
            hireby = listing.get('hiredby')
            casts.append([name,personId,hireby,'Actress'])
    #All crew details     
    if(child.tag=='crew'):
        #fetch all genres
        for listing in root.findall(child.tag+"/director/person"):
            name = listing.find('name')
            name = name.text
            personId = listing.get('personId')
            hireby = listing.get('hiredby')
            crew.append([name,personId,hireby,'Director'])
            
        for listing in root.findall(child.tag+"/constume-designer/person"):
            name = listing.find('name')
            name = name.text
            personId = listing.get('personId')
            hireby = listing.get('hiredby')
            crew.append([name,personId,hireby,'ConstumeDesigner'])    
        for listing in root.findall(child.tag+"/singer/person"):
            name = listing.find('name')
            name = name.text
            personId = listing.get('personId')
            hireby = listing.get('hiredby')
            crew.append([name,personId,hireby,'Singer'])   
    #All award details     
    if(child.tag=='awards'):
        #fetch all genres
        for listing in root.findall(child.tag+"/nominee/award"):
            nominee = listing.get('nomineeid')
            name = listing.get('name')
            awardNom.append([nominee,name])
        for listing in root.findall(child.tag+"/winner/award"):
            wonby = listing.get('wonby')
            name = listing.get('name')
            awardWin.append([wonby,name])

            


# In[32]:


distinctDirectors=[]
for i in crew:
    if(i[3]=='Director'):
        distinctDirectors.append((i[0],i[1]))


# In[33]:


actor=[]
actress=[]
for i in casts:
    if(i[3]=='Actor'):
        actor.append((i[0],i[1],i[2]))
    else:
        actress.append((i[0],i[1],i[2]))
        
director=[]
constumeDesigner=[]
singer=[]
for i in crew:
    if(i[3]=='Director'):
        director.append((i[0],i[1],i[2]))
    if(i[3]=='ConstumeDesigner'):
        constumeDesigner.append((i[0],i[1],i[2]))
    if(i[3]=='Singer'):
        singer.append((i[0],i[1],i[2]))


# In[34]:



g=Graph()
filename = cwd+"\\tvseries.owl"
g.load(filename, format='xml')


# In[35]:


myNamespace="http://www.semanticweb.org/cseka/ontologies/2022/3/tvseries"
namedIndividual = URIRef('http://www.w3.org/2002/07/owl#NamedIndividual')
rdftype = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


# In[36]:


individualName=str(myNamespace)+"#"+str(episodes[0][1]).replace(' ','_')
arc_class=str(myNamespace)+"#"+"Episode"
arc_individual = URIRef(individualName) 


# In[37]:


def isAlreadyDefined(subs):
    for s in g.subjects():
        if(subs in str(s)):
            return True
    return False


# In[38]:


all_triplets=[]
triplets=[]
object_properties=[]  
attribute_properties=[]  

sub_pred_obj=[]


# ### Add all Actors and Actress

# In[39]:


for cst in actor: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Cast"
        arc_class_Male=str(myNamespace)+"#"+"Male"
        arc_individual = URIRef(individualName)         
        
        if(isAlreadyDefined(individualName)==False): 
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class_Male)))
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            
            #Add attribute : Person Id
            subject=arc_individual
            pred= URIRef(str(myNamespace)+"#personid")
            literal=int(cst[1])
            attribute_properties.append((subject,pred, Literal(literal,datatype=XSD.integer)))
            
            # add rdf label
            literal=cst[0]
            attribute_properties.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))
          


# In[40]:


for cst in actress: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Cast"
        arc_class_Female=str(myNamespace)+"#"+"Female"
        arc_individual = URIRef(individualName)         
        
        if(isAlreadyDefined(individualName)==False): 
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class_Female)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            #Add attribute : Person Id
            subject=arc_individual
            pred= URIRef(str(myNamespace)+"#personid")
            literal=int(cst[1])
            attribute_properties.append((subject,pred, Literal(literal,datatype=XSD.integer)))
            
             # add rdf label
            literal=cst[0]
            attribute_properties.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))


# ### Add episodes

# In[41]:


itr=0
for eps in episodes:
    itr+=1
    #Add season
    individualName=str(myNamespace)+"#"+str("season_"+str(itr)).replace(' ','_')
    arc_class=str(myNamespace)+"#"+"Season"
    arc_individual = URIRef(individualName) 
    #all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
    all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
    #Add new episodes
    for i in range(len(eps)-1): 
        individualName=str(myNamespace)+"#"+str(eps[i+1]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Episode"
        arc_individual = URIRef(individualName) 
        
        if(isAlreadyDefined(individualName)==False): 
            #all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            
            # add rdf label
            literal=eps[i+1]
            attribute_properties.append((arc_individual,RDFS.label, Literal(literal,datatype=XSD.string)))
            


# ### Add all genere

# In[42]:


for eps in genres: 
        individualName=str(myNamespace)+"#"+str(eps).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Genere"
        arc_individual = URIRef(individualName) 
        if(isAlreadyDefined(individualName)==False): 
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            


# ### Add all Crew

# In[43]:


for cst in director: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Director"
        arc_individual = URIRef(individualName)         

        if(isAlreadyDefined(individualName)==False): 
            #all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            #Add attribute : Person Id
            subject=arc_individual
            pred= URIRef(str(myNamespace)+"#personid")
            literal=int(cst[1])
            attribute_properties.append((subject,pred, Literal(literal,datatype=XSD.integer)))
            
            
            # add rdf label
            literal=cst[0]
            attribute_properties.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))
            


# In[44]:


for cst in constumeDesigner: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"CostumeDesigner"
        arc_individual = URIRef(individualName)         

        if(isAlreadyDefined(individualName)==False): 
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            #Add attribute : Person Id
            subject=arc_individual
            pred= URIRef(str(myNamespace)+"#personid")
            literal=int(cst[1])
            attribute_properties.append((subject,pred, Literal(literal,datatype=XSD.integer)))
            
            
            # add rdf label
            literal=cst[0]
            attribute_properties.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))
            


# In[45]:


for cst in singer: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Singer"
        arc_individual = URIRef(individualName)         
        

        if(isAlreadyDefined(individualName)==False): 
            all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            #Add attribute : Person Id
            subject=arc_individual
            pred= URIRef(str(myNamespace)+"#personid")
            literal=int(cst[1])
            attribute_properties.append((subject,pred, Literal(literal,datatype=XSD.integer)))
            
            
            # add rdf label
            literal=cst[0]
            attribute_properties.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))
            


# In[46]:



for cst in songs: 
        individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
        arc_class=str(myNamespace)+"#"+"Song"
        arc_individual = URIRef(individualName)         
        if(isAlreadyDefined(individualName)==False): 
            #all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
            all_triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))
            
            
            # add rdf label
            literal=cst[0]
            attribute_properties.append((arc_individual,RDFS.label, Literal(literal,datatype=XSD.string)))
            
           


# ### Add object properties "Hires"
# #### Director hires cast and crew members
# #### Use attribute personid HiredBy provided in the XML to make the mapping

# In[47]:



for director in distinctDirectors:
    individualName=str(myNamespace)+"#"+str(director[0]).replace(' ','_')   
    subject = URIRef(individualName)         
    pred=URIRef((myNamespace)+"#hires")

    for cost in constumeDesigner: 
        
        if(cost[2]==director[1]):
            individualName=str(myNamespace)+"#"+str(cost[0]).replace(' ','_') 
            objects = URIRef(individualName)
            object_properties.append((subject,pred,objects))
    for cost in singer: 
        if(cost[2]==director[1]):
            individualName=str(myNamespace)+"#"+str(cost[0]).replace(' ','_') 
            objects = URIRef(individualName)
            object_properties.append((subject,pred,objects))
    for cost in actor: 
        if(cost[2]==director[1]):
            individualName=str(myNamespace)+"#"+str(cost[0]).replace(' ','_') 
            objects = URIRef(individualName)
            object_properties.append((subject,pred,objects))
       
        
        


# ### Object properties Consist-Of
# #### Season consist-Of episodes

# In[48]:



itr=0
for eps in episodes:
    itr+=1
    #Add season
    individualName=str(myNamespace)+"#"+str("season_"+str(itr)).replace(' ','_')
    subject = URIRef(individualName)  
    pred= URIRef(str(myNamespace)+"#consistsOf")  
    for i in range(len(eps)-1): 
        individualName=str(myNamespace)+"#"+str(eps[i+1]).replace(' ','_')
        objects = URIRef(individualName) 
        object_properties.append((subject,pred,objects))


# In[49]:



for cst in songs: 
    #print(cst)
    individualName=str(myNamespace)+"#"+str(cst[0]).replace(' ','_')
    #arc_class=str(myNamespace)+"#"+"Song"
    object = URIRef(individualName) 
    pred= URIRef(str(myNamespace)+"#sings")  
    for sng in singer:
        if(int(cst[1][0])==int(sng[1])):
            #print(sng)
            individualName=str(myNamespace)+"#"+str(sng[0]).replace(' ','_')
            subject = URIRef(individualName) 
            object_properties.append((subject,pred,object))
           


# ### All triplets

# In[50]:


#print(all_triplets)


# In[51]:


#print(object_properties)


# In[52]:


#print(attribute_properties)


# ### add all the triplets

# ##### Add indivisual

# In[53]:


for i in all_triplets:
    g.add(i)


# ##### Add Object properties

# In[54]:


for i in object_properties:
    g.add(i)


# ##### Add Attribute properties

# In[55]:


for i in attribute_properties:
    g.add(i)


# ### Save data

# In[56]:


g.serialize(destination="output/output.owl")


# In[67]:


textfile = open("output/Triples.txt", "w")
for i in all_triplets:  
    textfile.write("Subject: "+str(i[0])+ "\n")
    textfile.write("Predicate: "+str(i[1])+ "\n")
    textfile.write("Object: "+str(i[2])+ "\n")
    textfile.write("---------------------------------------------------------------------------------------------\n")
for i in object_properties:    
    textfile.write("Subject: "+str(i[0])+ "\n")
    textfile.write("Predicate: "+str(i[1])+ "\n")
    textfile.write("Object: "+str(i[2])+ "\n")
    textfile.write("---------------------------------------------------------------------------------------------\n")     
for i in attribute_properties:
    textfile.write("Subject: "+str(i[0])+ "\n")
    textfile.write("Predicate: "+str(i[1])+ "\n")
    textfile.write("Object: "+str(i[2])+ "\n")
    textfile.write("---------------------------------------------------------------------------------------------\n")    

textfile.close()


# In[ ]:





# In[ ]:




