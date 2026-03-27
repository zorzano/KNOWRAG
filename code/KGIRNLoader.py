import sys
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
from KGIoTSynonims import KGIoTSynonims
import os
import time
import json
from KGIoTOpenAI import KGIoTOpenAI

clientOpenAI = KGIoTOpenAI()

kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))

def cleanForFineTune(line):
    line=line.replace("\\", "/")
    line=line.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
    line=line.replace('"', '\\"').replace("'", "")
    line=line.replace("\t", "\\t")
    return line
 

if(len(sys.argv)>2):
    kgiotsynonims=KGIoTSynonims(sys.argv[2])
else:
    kgiotsynonims=KGIoTSynonims("")

with open(sys.argv[1], newline='', encoding='utf-8') as f:            
    for i, linea in enumerate(f, 1):
           try:
                fields=linea.rstrip().split('\t')
                if len(fields)==3:
                    s=fields[0]
                    p=fields[1]
                    o=fields[2]
                    if p.endswith("_inverse"):
                        p = p[:-8]  # "_inverse" tiene 8 caracteres
                        aux=s
                        s=o
                        o=aux
                else:
                    print("Incomplete input line:"+linea)
                    continue
                
                s=s.replace("'","")
                p=p.replace("'","").replace(" ","_").replace("(", "").replace(")", "").replace(",", "_").replace("/", "_").replace("-", "_")
                o=o.replace("'","")
                kgiotdriver.mergeNode("Concept:Searchable", [("name", s)])
                kgiotdriver.mergeNode("Concept:Searchable", [("name", o)])
                kgiotdriver.mergeLink(p,[], "Concept:Searchable", [("name", s)],  "Concept:Searchable", [("name", o)])
                vector=clientOpenAI.get_embedding(s)
                kgiotdriver.addEmbeddings("Searchable", "name", s, "embedding", vector)
                vector=clientOpenAI.get_embedding(o)
                kgiotdriver.addEmbeddings("Searchable", "name", o, "embedding", vector)
                print(f"  - ({s}) --[{p}]--> ({o})")
           except Exception as e:
                print(f"Otro error en la línea {i}: {e}")