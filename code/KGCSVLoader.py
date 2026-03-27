import sys
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
from KGIoTSynonims import KGIoTSynonims
import os
import csv
import time
from openai import OpenAI
from KGIoTOpenAI import KGIoTOpenAI

clientOpenAI = KGIoTOpenAI()

def chatgptify(text):

    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        response_format={ "type": "text" },
        messages=[
            {"role": "system", "content": "normal, español"},
            {"role": "user", "content": text}
        ])
    return(response.choices[0].message.content)
    
def loadNode(fields, kgiotdriver):
    pairslist=[]
    name=""
    
    for i in range(2, len(fields),2):
        if fields[i] != "":
            content=fields[i+1]
            if content[:7]=="openai#":
                content=chatgptify(content[7:])
            pairslist.append((fields[i], content))
            if fields[i]== "name":
                name=content
    kgiotdriver.mergeNode(fields[1]+":Searchable", pairslist)
    
    if name != "" :
        vector=clientOpenAI.get_embedding(name)
        kgiotdriver.addEmbeddings("Searchable", "name", name, "embedding", vector)
        name=""
        
    print("Inserting NODE of type "+fields[1]+" and attributes "+str(pairslist))
    
def loadRelation(fields, kgiotdriver):
    pairslist=[]
    pairslist.append([])
    pairslist.append([])
    relationType=fields[1]
    type1=fields[2]
    whatnode=0
    i=3
    while i < len(fields):
        if fields[i] == "->" :
            whatnode=1
            type2=fields[i+1]
            i+=1
        elif fields[i] != "":
            print(fields, i)
            pairslist[whatnode].append((fields[i], fields[i+1]))
            i+=1
        i+=1
    print("Inserting RELATION of type "+relationType+" between a node of type "+type1+" and attributes "+str(pairslist[0])+" and a node of type "+type2+" and attributes "+str(pairslist[1]))
    res=kgiotdriver.mergeLink(relationType,[], type1, pairslist[0], type2, pairslist[1])

kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))
client = OpenAI()


if(len(sys.argv)>2):
    kgiotsynonims=KGIoTSynonims(sys.argv[2])
else:
    kgiotsynonims=KGIoTSynonims("")

with open(sys.argv[1], newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    reader.__next__()
    for fields in reader:
        for index, item in enumerate(fields):
                fields[index]=kgiotsynonims.substituteAny(fields[index])
                fields[index]=item.strip(" \"")
                fields[index] = fields[index].replace("\\N", "")
                fields[index]=kgiotsynonims.map(fields[index])
                print(index, " ", fields[index])
                
        if fields[0] == "N" :
            loadNode(fields, kgiotdriver)
        elif fields[0] == "R" :
            loadRelation(fields, kgiotdriver)
            continue
