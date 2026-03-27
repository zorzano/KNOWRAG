import logging
import sys
import argparse
from openai import OpenAI
import random

def first_digit(text):
    for char in text:
        if char.isdigit():
            return int(char)
    return 0  # Returns 0 if there are no digits
    
def rateAnswers(q, a1, reference=None, a2=None):
                   
        question="Hemos hecho la siguiente pregunta a un sistema:\n"+\
                  "<COMIENZO DE PREGUNTA>\n"+\
                   q+"\n"+\
                   "<FIN DE PREGUNTA>\n"+\
                 " El sistema ha respondido lo siguiente:\n"+\
                 "<COMIENZO DE RESPUESTA 1>\n"+\
                 a1+"\n"+\
                 "<FIN DE RESPUESTA 1>\n"
        if reference is not None:
            if ',' in reference:
                    question+="Una respuesta correcta debe cuelquiera de los términos nombrados en la siguiente información, a la que denominamos REFERENCIA:\n"+\
                    "<COMIENZO DE REFERENCIA>\n"+\
                       reference+"\n"+\
                     "<FIN DE REFERENCIA>\n"
            else:
                question+="Una respuesta correcta debe contener al menos la siguiente información, a la que denominamos REFERENCIA:\n"+\
                    "<COMIENZO DE REFERENCIA>\n"+\
                       reference+"\n"+\
                     "<FIN DE REFERENCIA>\n"
        if a2 is not None:
            question+="Un segundo sistema ha redondido los siguiente:\n"+\
                "<COMIENZO DE RESPUESTA 2>\n"+\
                   a2+"\n"+\
                 "<FIN DE RESPUESTA 2>\n"+\
                 " ¿Cual de las dos respuestas te parece mejor? Responde primero con un solo caracter: 1 para la primera respuesta, 2 para la segunda, o 0 si no puedes decidir o son muy parecidas. Luego añade un breve texto explicando tu respuesta, que no incluya ninguna cifra."
        else:
            question+="¿Como valoras esta respuesta de 1 (peor) a 5 (mejor). Toma estas referencias:\n"+\
            "1: Incorrecto. La respuesta no incluye ninguna información de la Referencia.\n"+\
            "2: La respuesta admite que no puede proporcionar una respuesta o carece de contexto; es honesta.\n"+\
            "3: La respuesta tiene parte de la información de la Referencia.\n"+\
            "4: La respuesta es aceptable, contiene la información de la Referencia pero no es exhaustiva.\n"+\
            "5: La respuesta contiene toda la información de la Referencia. Está redactada de manera que es fácil de leer.\n"+\
            "Responde primero con un solo caracter: 1, 2, 3, 4 o 5. Luego añade un breve texto explicando tu respuesta, que no incluya ninguna cifra. Si la pregunta se refiere a futbol, no tengas en cuenta datos que conozcas por tu cuenta posteriores al mundial de 2014. Si la respuesta contiene la respuesta pero traducida a español, valórala igual de bien."

# 4 alternativa, buscando eliminar el problema del IRN
#"4: La respuesta es aceptable, contiene la información de la Referencia pero no es exhaustiva o es dificil de leer.\n"+\
# 5 alternativa, buscando eliminar el problema del IRN
#"5: La respuesta contiene toda la información de la Referencia. Está redactada de manera que es fácil de leer.\n"+\
# 5 Original
# "5: La respuesta contiene toda la información de la Referencia y la completa.\n"+\
        response = client.chat.completions.create(
             model="gpt-4o-2024-11-20",
             response_format={ "type": "text" },
             messages=[
                {"role": "system", "content": "normal"},
                {"role": "user", "content": question}
             ])
 
        logger.info("ChatGPT Question:"+question)
        logger.info("ChatGPT Answer:"+response.choices[0].message.content)
        
        result=first_digit(response.choices[0].message.content)

        return result    

def parse_question_answer_file(file_path):
    pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        question = None
        answer = None
        reference = None
        reading_question = False
        reading_answer = False
        reading_reference = False
        reading_other=False
        for line in file:
            line = line.rstrip()
            if line.startswith('<Q>'):
                if question is not None and answer is not None:
                    if reference is not None:
                        pairs.append((question.strip(), answer.strip(), reference.strip()))
                    else:
                        pairs.append((question.strip(), answer.strip()))
                question = line[3:].strip()
                answer = None
                reading_question = True
                reading_answer = False
                reading_reference = False
                reading_other=False
            elif line.startswith('<A>'):
                answer = line[3:].strip()
                reading_question = False
                reading_answer = True
                reading_reference = False
                reading_other=False
            elif line.startswith('<R>'):
                reference = line[3:].strip()
                reading_question = False
                reading_answer = False
                reading_reference = True
                reading_other=False
            elif line.startswith('<'):
                reading_question = False
                reading_answer = False
                reading_reference = False
                reading_other=True
            elif reading_question:
                question += '\n' + line
            elif reading_answer:
                answer += '\n' + line
            elif reading_reference:
                reference += '\n' + line
        # Add the last pair if it exists
        if question is not None and answer is not None:
            if reference is not None:
               pairs.append((question.strip(), answer.strip(), reference.strip()))
            else :
               pairs.append((question.strip(), answer.strip()))
    return pairs
   
logger = logging.getLogger(__name__)
logging.basicConfig(filename='RAGCompareAnswers.log', level=logging.DEBUG)
client = OpenAI()
parser = argparse.ArgumentParser(
                    prog='RAG Rate one answers file, or compare two',
                    description='Rate one file with answers from KITI or compare two',
                    epilog='Knowledge and Things')
                    
parser.add_argument('-filename1', help="Text file 1 with questions, answers and optionally references")
parser.add_argument('-filename2', help="Text file 2 with questions and answers", default=None)
parser.add_argument('-resultfile', help="Output file", default="result.txt")


args=parser.parse_args()

qa1=parse_question_answer_file(args.filename1)

if args.filename2 is not None:
    qa2=parse_question_answer_file(args.filename2)
else:
    qa2=None
    
nquestions=0
n=[0,0,0,0,0,0]
grades = []

for question, answer1, reference in qa1:
    if qa2 is not None:
        coincidence = [triad for triad in qa2 if triad[0] == question]
        if coincidence:
            answer2=coincidence[0][1]
        else:
            answer2=None
    else:
        answer2=None
    # TBD what happens if one answer is missing
    nquestions+=1
    res=rateAnswers(question, answer1, reference, answer2)
    print(res, end="", flush=True)
    n[res]+=1
    grades.append((question, res))
    
print("")
rf=open(args.resultfile, 'w', encoding='utf-8') 
rf.write("RAG Questions to KITI database rate executed. Results.\n")
rf.write("File 1:"+args.filename1+"\n")
if args.filename2 is not None:
    rf.write("File 1:"+args.filename2+"\n")

# Print just line with grades

for q,g in grades:
    rf.write(str(g))
rf.write("\n")

# Print aggregates in file
total=0.0
for indice, valor in enumerate(n):
    rf.write(str(indice)+":"+str(valor)+"\n")
    total+=indice*valor
average=total/nquestions

rf.write("\n")
rf.write("Total questions counted:"+str(nquestions)+"\n")
rf.write("Average:"+str(average)+"\n")
print("Average:"+str(average)+"\n")

# Print detail grades in file
count=0
for q,g in grades:
    count+=1
    rf.write(str(count)+" Grade: "+str(g)+" Question: "+q+"\n")
rf.write("\n")

