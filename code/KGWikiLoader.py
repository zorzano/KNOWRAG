import sys
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
import re
import os

from KGIoTOpenAI import KGIoTOpenAI

clientOpenAI = KGIoTOpenAI()

kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))


# Using readlines()
file1 = open(sys.argv[1], 'r', encoding='cp1252')
fileFineTune = open("finetune.txt", 'a', encoding='utf-8')
template = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "{chapterTitle}"}}, {{"role": "assistant", "content": "{chapterText}"}}]}}\n' 

def printToFileFineTune(line):
    fileFineTune.write(line)

def cleanForFineTune(line):
    line=line.replace("\\", "/") 
    line=line.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
    line=line.replace('"', '\\"').replace("'", '\\"')
    line=line.replace("\t", "\\t")
    return line

Lines = file1.readlines()
closeChapter=False
inChapter=False
chapterText=""
chapterTitle=""
# Strips the newline character
for line in Lines:
    title=re.match(".+>([\w\s\d\.\,\:\/]+)</h1", line)
    endtitle=re.match("<h1", line)
    if (endtitle != None) and inChapter:
        chapterTitle=chapterTitle.replace("'","\\'")
        chapterText=chapterText.replace("'","\\'")
        print("TITULO:"+chapterTitle)
        print("TEXTO:"+chapterText[0:100])
        # Comentar para pruebas de FineTune. Reponer
        kgiotdriver.mergeNode("Process:Searchable", [("name", chapterTitle), ("text", chapterText)])
        vector=clientOpenAI.get_embedding(chapterTitle)
        kgiotdriver.addEmbeddings("Searchable", "name", chapterTitle, "embedding", vector)
        
        printToFileFineTune(template.format(chapterTitle=cleanForFineTune(chapterTitle), chapterText=cleanForFineTune(chapterText)))
        
        chapterText=""
    if title != None:
        inChapter=True
        chapterTitle=title.groups()[0]
    if inChapter and (title==None):
        chapterText+=line


kgiotdriver.close()