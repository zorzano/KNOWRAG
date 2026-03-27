import logging
import sys
from GordopiloDialog import GordopiloDialog, GordopiloParameters
import argparse
import configparser
import time

def parse_question_answer_file(file_path):
    pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        question = None
        answer = None
        reading_question = False
        reading_answer = False
        for line in file:
            line = line.rstrip()
            if line.startswith('<Q>'):
                if question is not None and answer is not None:
                    pairs.append((question.strip(), answer.strip()))
                question = line[3:].strip()
                answer = None
                reading_question = True
                reading_answer = False
            elif line.startswith('<R>'):
                answer = line[3:].strip()
                reading_question = False
                reading_answer = True
            elif reading_question:
                question += '\n' + line
            elif reading_answer:
                answer += '\n' + line
            print(".",end="", flush=True)
        # Add the last pair if it exists
        if question is not None and answer is not None:
            pairs.append((question.strip(), answer.strip()))
        print("")
    return pairs
    
logger = logging.getLogger(__name__)
logging.basicConfig(filename='RAGAskQuestions.log', level=logging.DEBUG)

parser = argparse.ArgumentParser(
                    prog='RAG Ask Questions',
                    description='Ask questions from file to KITI base',
                    epilog='Knowledge and Things')
                    
parser.add_argument('-filename', help="Text file with configuration", default="config.txt")
parser.add_argument('-question', help="Single question to execute (instead of question file)", default=None)


args=parser.parse_args()
config = configparser.ConfigParser()
config.read_file(open(args.filename))
questionfile = config.get('CONFIG', 'QuestionsFile')
outputfile = config.get('CONFIG', 'OutputFile')
resultfile = config.get('CONFIG', 'ResultFile')

#Analysis of parameters
gp=GordopiloDialog()
gpp=GordopiloParameters()
gpp.LLMModel=config.get('CONFIG', 'LLMModel', fallback=None)
gpp.KG=bool(config.get('CONFIG', 'KG', fallback="No") == "Yes")
gpp.nHitsKG=int(config.get('CONFIG', 'nHitsKG', fallback="1"))
gpp.expandQuestion=int(config.get('CONFIG', 'expandQuestion', fallback="0"))
gpp.askIsQuestion=bool(config.get('CONFIG', 'askIsQuestion', fallback="No") == "Yes")
gpp.extractTerms=int(config.get('CONFIG', 'extractTerms', fallback="0"))
gpp.extractLoopTerms=int(config.get('CONFIG', 'extractLoopTerms', fallback="0"))
gpp.nLoopsExtra=int(config.get('CONFIG', 'nLoopsExtra', fallback="0"))
if (gpp.LLMModel == "None" or gpp.LLMModel == "none"):
    gpp.LLMModel=None

print("Questions File:"+questionfile)
print("Output File:"+outputfile)
print("Result File:"+resultfile)

of=open(outputfile, 'w', encoding='utf-8')
gpp.of=of
gp.setParameters(gpp)
totalResults=0

seconds=time.time()
# If command line test
if args.question is not None:
    print ("Question:"+args.question+"\n")
    print ("Answer:"+gp.answerText(args.question)+"\n")
else:
    pairs = parse_question_answer_file(questionfile)
    positiveResults=0
    # Print the question-answer pairs
    for question, reference in pairs:
        logger.info("Question:\n"+question+"\n")
        of.write("<Q>\n"+question+"\n")
        logger.info("Reference:\n"+reference+"\n")
        of.write("<R>\n"+reference+"\n")
        gpanswer=gp.answerText(question)
        logger.info("Gordopilo Answer:\n"+gpanswer+"\n")
        of.write("<A>\n"+gpanswer+"\n")
        logger.info("-" * 40)
        totalResults+=1
        print(".", end="", flush=True)
    print("")
rf=open(resultfile, 'w', encoding='utf-8') 
rf.write("RAG Questions to KITI database executed. Results.\n")
rf.write("Total questions:"+str(totalResults)+"\n")
rf.write("Embedding Tokens:"+str(gp.embeddingTokens)+"\n")
rf.write("Completion Tokens:"+str(gp.completionTokens)+"\n")
rf.write("Seconds:"+str(time.time()-seconds)+"\n")
    

