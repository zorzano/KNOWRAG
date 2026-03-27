import logging
import sys
import argparse
from openai import OpenAI
import random

def compareAnswers(q, a1, a2):
        
        if random.random()<0.5:
            change=True
            alt=a2
            a2=a1
            a1=alt
        else:
            change=False
        
        if answer1==answer2:
            logger.info("Two identical answers. Question:"+q+"Answer:"+a1)
            return 0
            
        question="Hemos hecho la siguiente pregunta a dos sistemas distintos:\n"+\
                  "<COMIENZO DE PREGUNTA>\n"+\
                   q+"\n"+\
                   "<FIN DE PREGUNTA>\n"+\
                 " El primer sistema ha respondido lo siguiente:\n"+\
                 "<COMIENZO DE RESPUESTA 1>\n"+\
                 a1+"\n"+\
                 "<FIN DE RESPUESTA 1>\n"+\
                 " El segundo sistema ha respondido:\n"+\
                 "<COMIENZO DE RESPUESTA 2>\n"+\
                 a2+"\n"+\
                 "<FIN DE RESPUESTA 2>\n"+\
                 " ¿Cual de las dos respuestas te parece mejor? Responde primero con un solo caracter: 1 para la primera respuesta, 2 para la segunda, o 0 si no puedes decidir. Luego añade un breve texto explicando tu respuesta, que no incluya ninguna cifra."
        
        response = client.chat.completions.create(
             model="gpt-4o-2024-11-20",
             response_format={ "type": "text" },
             messages=[
                {"role": "system", "content": "normal"},
                {"role": "user", "content": question}
             ])
 
        logger.info("ChatGPT Question:"+question)
        logger.info("ChatGPT Answer:"+response.choices[0].message.content)
        
        if "1" in response.choices[0].message.content:
            if not change:
                result=1
            else:
                result=2
        elif "2" in response.choices[0].message.content:
            if not change:
                result=2
            else:
                result=1
        else:   
            result=0

        return result    

def parse_question_answer_file(file_path):
    pairs = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        question = None
        answer = None
        reading_question = False
        reading_answer = False
        for line in file:
            line = line.rstrip()
            if line.startswith('<Q>'):
                if question is not None and answer is not None:
                    pairs[question.strip()]=answer.strip()
                question = line[3:].strip()
                answer = None
                reading_question = True
                reading_answer = False
            elif line.startswith('<A>'):
                answer = line[3:].strip()
                reading_question = False
                reading_answer = True
            elif reading_question:
                question += '\n' + line
            elif reading_answer:
                answer += '\n' + line
        # Add the last pair if it exists
        if question is not None and answer is not None:
            pairs[question.strip()]=answer.strip()
    return pairs
   
logger = logging.getLogger(__name__)
logging.basicConfig(filename='RAGCompareAnswers.log', level=logging.DEBUG)
client = OpenAI()
parser = argparse.ArgumentParser(
                    prog='RAG Compare two answers files',
                    description='Compare two files with answers from KITI',
                    epilog='Knowledge and Things')
                    
parser.add_argument('filename1', help="Text file 1 with questions and answers")
parser.add_argument('filename2', help="Text file 2 with questions and answers")
parser.add_argument('resultfile', help="Output file", default="result.txt")


args=parser.parse_args()

qa1=parse_question_answer_file(args.filename1)
qa2=parse_question_answer_file(args.filename2)

#print(qa1)
#print(qa2)

nquestions=0
n1=0
n2=0
eq=0
for question, answer1 in qa1.items():
    answer2=qa2[question]
    # TBD what happens if one answer is missing
    nquestions+=1
    res=compareAnswers(question, answer1, answer2)
    print(res, end="", flush=True)
    if res==1:
        n1+=1
    elif res==2:
        n2+=1
    elif res==0:
        eq+=1
print("")
rf=open(args.resultfile, 'w', encoding='utf-8') 
rf.write("RAG Questions to KITI database comparison executed. Results.\n")
rf.write("File 1:"+args.filename1+"Winner:"+str(n1)+"\n")
rf.write("File 2:"+args.filename2+"Winner:"+str(n2)+"\n")
rf.write("Equals:"+str(eq)+"\n")
rf.write("Total questions counted:"+str(nquestions)+"\n")



