import sys
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
from KGIoTSynonims import KGIoTSynonims
import os
import time
import json
from KGIoTOpenAI import KGIoTOpenAI

clientOpenAI = KGIoTOpenAI()

kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))

fileFineTune = open("finetuneMINTQA.jsonl", 'w', encoding='utf-8')
templateFineTune = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "{q}"}}, {{"role": "assistant", "content": "{a}"}}]}}\n' 

def printToFileFineTune(line):
    fileFineTune.write(line)

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
                obj = json.loads(linea)
                question = obj.get("question", "")
                answer = obj.get("answer", "")
                triples = obj.get("triple", [])

                print(f"\nLínea {i}")
                print(f"Pregunta: {question}")
                print(f"Respuesta: {answer}")
                printToFileFineTune(templateFineTune.format(q=cleanForFineTune(question), a=cleanForFineTune(answer)))
                # Enable to generate only the finetune file
                #continue
                
                print("Triples:")
                for s, p, o in triples:
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

            except json.JSONDecodeError as e:
                print(f"Error en la línea {i}: {e}")
            except Exception as e:
                print(f"Otro error en la línea {i}: {e}")