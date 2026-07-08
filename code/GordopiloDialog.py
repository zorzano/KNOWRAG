from flask import Flask
from flask import request
from collections import defaultdict
import json
import re
import logging
import string
import sys
import os
import spacy
from openai import OpenAI
import datetime
import os
import requests
from datetime import date
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
import re

logger = logging.getLogger(__name__)
SYSTEM_REFLEXION =""

#SYSTEM_REFLEXION = """
#Ahora sigue una Reflexion que hiciste despues de analizar tu propio trabajo en otras preguntas:
#Estás respondiendo preguntas utilizando ÚNICAMENTE la información presente explícitamente en los elementos recuperados del Knowledge Graph.
#
#REGLAS IMPORTANTES:
#
# 1. No infieras hechos que no estén explícitamente indicados.
# 2. Prefiere coincidencias exactas de propiedades frente a suposiciones semánticas.
# 3. Utiliza los nombres de las relaciones de forma literal.
# 4. No mezcles:
   # - club
   # - país
   # - selección nacional
   # - nacionalidad
   # salvo que estén conectados explícitamente en los datos recuperados.
# 5. Si una propiedad responde directamente a la pregunta, utiliza únicamente esa propiedad y nada más.
# 6. No añadas explicaciones contextuales ni hechos adicionales.
# 7. Devuelve respuestas concisas centradas únicamente en la entidad o valor solicitado.
# 8. Si existen múltiples hechos candidatos, prioriza:
   # - la entidad mencionada explícitamente en la pregunta
   # - coincidencias exactas de relaciones
   # - relaciones directas de un solo salto
# 9. Evita utilizar entidades recuperadas no relacionadas, aunque sean semánticamente similares.
# 10. No asumas que el país de un club implica la selección nacional de un jugador.
# 11. Al responder preguntas factuales, evita frases narrativas.
# 12. Si la respuesta no puede determinarse de forma inequívoca a partir de los elementos recuperados, indícalo explícitamente.

# Ejemplos:

# P: ¿Cuál es el número de camiseta de Kylian_MBAPPE?
# Respuesta correcta: 9
# Respuesta incorrecta: Kylian Mbappé es un delantero francés que lleva el número 9.

# P: ¿En qué club juega Erling_HAALAND?
# Respuesta correcta: Manchester_City

# P: ¿En qué país está basado Bayern_Munich?
# Respuesta correcta: Germany

# P: ¿Para qué selección juega Jude_BELLINGHAM?
# Respuesta correcta: England

# P: ¿En qué posición juega Vinicius_JUNIOR?
# Respuesta correcta: Forward
# """

class GordopiloParameters():
    LLMModel="gpt-4o-2024-11-20"
    defaultLLMModel="gpt-4o-2024-11-20"
    KG=True
    of=None
    nHitsKG=1
    extractTerms=0
    extractLoopTerms=0
    askIsQuestion=False
    nLoopsExtra=0
    

def singleton(cls, *args, **kw):
     instances = {}
     def _singleton(*args, **kw):
        if cls not in instances:
             instances[cls] = cls(*args, **kw)
        return instances[cls]
     return _singleton

@singleton
class GordopiloDialog(object):
     def __init__(self):
         
         self.nlp = spacy.load("es_core_news_sm")
         sys.path.append('/home/ubuntu/repo/code')
         self.kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))
         logger.info("GordopiloDialog Initialized")
         self.parameters=GordopiloParameters()
         self.clientEmbedding = OpenAI()   
         if "llama" in self.parameters.LLMModel:             
            self.clientQuestion=OpenAI(
                base_url='https://openrouter.ai/api/v1',
                api_key=os.environ.get("OPENROUTER_API_KEY")
            )
         else:
            self.clientQuestion = self.clientEmbedding
         self.completionTokens=0
         self.embeddingTokens=0
         # reflexionTrace almacena la traza de decisiones del LLM para que luego el LLM pueda reflexionar y aprender
         self.reflexionTrace=""

         
     def setParameters(self, newparameters):
        self.parameters=newparameters
        if "llama" in self.parameters.LLMModel:             
             self.clientQuestion=OpenAI(
                base_url= 'https://openrouter.ai/api/v1',
                api_key= os.environ.get("OPENROUTER_API_KEY")
            )
        else:
            self.clientQuestion = self.clientEmbedding
  
     
     def close(self):
        self.kgiotdriver.close()
     
     def getReflexionTrace(self):
         return self.reflexionTrace
     
     def get_embedding(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        response=self.clientEmbedding.embeddings.create(input = [text], model=model)
        self.embeddingTokens+=response.usage.total_tokens
        return response.data[0].embedding
          
     def chatgptify(self, question, answer=""):

        voiceRoles=[#"Eres un sargento brutal con un gran conocimiento de telecomunicaciones, gritando a un recluta.", 
                    #"Eres Yoda, con un gran conocimiento de telecomunicaciones.", 
                    #"Eres un poeta escribiendo en verso.",
                    #"Eres un un siervo humilde y miserable de un cuento oriental, con un gran conocimiento de telecomunicaciones.",
                    #"Eres un pijo",
                    #"Eres un ingeniero de telecomunicaciones que aprovecha cada ocasion para hablar bien del jefe de Tecnologia, Operaciones y Soluciones IoT, Carlos Carazo.",
                     "normal"
                    ]
        
        if answer != "":
            question="Tienes que responder a la siguiente pregunta:"+question+"\n Para ello debes usar solo los siguientes datos, que son las fichas de uno o más elementos de una base de datos. Por favor, genera un texto que de toda la información de una manera explicada. No hagas suposiciones que no estén aquí indicadas ni añadas otra información. Tampoco menciones que estás manejando fichas. Si la información incluye una lista larga de elementos relavantes para la pregunta, no la resumas en tu respuesta, cita todos los elementos.\n"+answer
 
        response = self.clientQuestion.chat.completions.create(
             model=self.parameters.LLMModel,   
             response_format={ "type": "text" },
             messages=[
                {"role": "system", "content": voiceRoles[datetime.datetime.today().day % len(voiceRoles)]},
                {"role": "user", "content": question}
             ])
        self.completionTokens+=getattr(getattr(response, "usage", None), "total_tokens",0)
        try:
            theResponse = str(response.choices[0].message.content)
        except (AttributeError, IndexError, TypeError):
            theResponse = ""
            
        logger.info("GordopiloDialog::chatgptify response:\n"+theResponse)
        if self.parameters.of:
            self.parameters.of.write("\n<P>\n Prompt: "+question+"\n")
        
        return(theResponse)

     def formatNodeResult(self, theEntity, res):
            logger.info("GordopiloDialog::formatNodeResult")
            nodeType="Unknown"
            # Identify node type
            for i in res[0][0].labels:
                # As I use Searchable to register embeddings in the base, I have to skip it.
                if str(i) != "Searchable":
                    if nodeType == "Unknown" :
                        nodeType=str(i)
                    else:
                        nodType+=", "+str(i)
                
            response="Name: "+theEntity+"\nType:"+nodeType+".\n" 
            if "text" in res[0][0]:
              response+="Description:"+res[0][0]["text"]+"\n"
            logger.info("GordopiloDialog::formatNodeResult. response step 1:"+response)
            
            # Define relationsSet as an empty dictionary
            relationsSet=defaultdict(list)
            
            
            for item in res:
                # item[0, el sujeto, 1, el link, 2, el objeto]["name"]
                # item[0].labels[0]?
                #response+=str(item[0]["name"])+"-"+"-"+str(item[1].type)+"-"+str(item[2]["name"])
                # But, if the object flies alone, it has no link nor object  
                if len(item) > 1:                  
                    logger.info("GordopiloDialog::formatNodeResult. ITEM IN RES: "+str(item[1].type))
                    relationsSet[str(item[1].type)].append(str(item[2]["name"]))
            
            logger.info("GordopiloDialog::formatNodeResult. relationsSet:"+str(relationsSet))    
            
            # Print result of the kind "Tiene 5 pais: Albania, Alemania, España, Rumania, Francia,.
            for key in relationsSet:
                response+=key+":"
                for target in relationsSet[key]:
                    response+=target+","
                response+=".\n"
            logger.info("GordopiloDialog::formatNodeResult. response step 2:\n"+response)
            
            if nodeType=="Organization":
               #app.logger.info("["+theEntity+"] is an Organization. Looking for delivered services.") 
               services=self.kgiotdriver.searchLinkChain("Organization", [("name", theEntity)], [("manufacturer",1),("serviceType|providesService", 1)], "Service")
               response+="Services offered:"
               for item in services :
                   response+=item[0]["name"]+","
               response+=".\n"
             
            logger.info("GordopiloDialog::formatNodeResult. response final:\n"+response)  
             
            return response

     def answerExpected(self, text):
     
        # If no LLM available, assume it is a question
        if not self.parameters.LLMModel :
            return True
            
        response = self.clientQuestion.chat.completions.create(
                model=self.parameters.LLMModel,
                response_format={ "type": "text" },
                messages=[
                    {"role": "system", "content": "normal"},
                    {"role": "user", "content": "Me llamo Gordopilo. He recibido el siguiente mensaje y necesito saber si el que me lo ha escrito espera una respuesta mia. Responde sólamente Sí o No. Este es el mensaje:"+text}
                ])   
        self.completionTokens+=getattr(getattr(response, "usage", None), "total_tokens",0)
        logger.info("GordopiloDialog::answerExpected response:\n"+response.choices[0].message.content) 

        if "Sí" in response.choices[0].message.content:
            return True
        else:
            return False
    
 
     # iterating version of answerText. This should deprecate the previous version
     def answerText(self, texto):                            
        # This line, just in case
        #return "Gordopilo está en parada de mantenimiento"
        
        self.reflexionTrace=""
        response=""
        
        # Two conditions that make us NOT answer. [off] label and not a question, if we are parametrized to check it
        if "[off]" in texto:
            return ""            
        if self.parameters.askIsQuestion :
            if not self.answerExpected(texto):
                self.reflexionTrace+="LLM determina que el texto no espera una respuesta"
                return response
        
        logger.info("GordopiloDialog::answerText(). Question is:"+texto)
        
        if self.parameters.KG :
        
            if self.parameters.extractTerms > 0:                
                theTerms=self.extractTerms(texto, self.parameters.extractTerms)
                self.reflexionTrace+="TERMINOS DE BUSQUEDA EN EL KNOWLEDGE GRAPH SELECCIONADOS POR EL LLM: "+str(theTerms)+"\n"
            else :                
                theTerms=[texto]
                self.reflexionTrace+="LOS TERMINOS DE BUSQUEDA EN EL KNOWLEDGE GRAPH NO LOS BUSCA EL LLM, SON LA PROPIA PREGUNTA: "+str(theTerms)+"\n"
            
            response=self.searchTermsInKG(theTerms)
            self.reflexionTrace+="TERMINOS ENCONTRADOS EN EL KNOWLEDGE GRAPH:\n"+response+"\n"
            
            # If we have to do LoopsExtra, we iterate asking the LLM for new terms           
            for i in range(1, self.parameters.nLoopsExtra):
                theTerms=self.askLLMForNewTerms(texto, response, self.parameters.extractLoopTerms)
                if not theTerms:
                    self.reflexionTrace+="ITERACION "+str(i)+". EL LLM RENUNCIA A PEDIR MAS TERMINOS DEL KNOWLEDGE BASE.\n"
                    break
                self.reflexionTrace+="ITERACION "+str(i)+". EL LLM PIDE BUSCAR NUEVOS TERMINOS EN EL KNOWLEDGE GRAPH: "+str(theTerms)+"\n"
                newResponse=self.searchTermsInKG(theTerms)
                self.reflexionTrace+="ITERACION "+str(i)+". TERMINOS ENCONTRADOS EN EL KNOWLEDGE GRAPH:\n"+newResponse+"\n"
                response+=newResponse
            
        else: # if there is no KG
            response=""

        logger.info("GordopiloDialog::answerText() Response:\n"+response)
        if self.parameters.LLMModel is not None:
            response=self.chatgptify(texto, response)
            self.reflexionTrace+="RESPUESTA FINAL GENERADA POR EL LLM: "+response+"\n"
        else:
            self.reflexionTrace+="RESPUESTA FINAL, NO GENERADA POR EL LLM: "+response+"\n"
        
        return response
     
     def askLLMForNewTerms(self, question, response, n):
        logger.info("GordopiloDialog::askLLMForNewTerms() Question:"+str(question))
        logger.info("GordopiloDialog::askLLMForNewTerms() Answers:"+str(response))
        logger.info("GordopiloDialog::askLLMForNewTerms() n:"+str(n))
        # Define working LLM
        extractorModel=self.parameters.LLMModel  
        if not self.parameters.LLMModel :
            extractorModel=self.parameters.defaultLLMModel
        # Question for LLM    
        response = self.clientQuestion.chat.completions.create(
                model=extractorModel,
                response_format={ "type": "text" },
                messages=[
                    {"role": "system", "content": "normal"},
                    {"role": "user", "content": "He recibido la siguiente pregunta:\n------------Comienzo del mensaje----------------\n"+question+\
                    "\n------------Fin del mensaje----------------\n"+\
                    "Para poder responderla voy a acceder a una base de datos en la que puedo buscar "+str(n)+" términos. Hasta el momento tengo la siguiente informacion en forma de fichas:"+response+"¿Cuales son los mejores "+str(n)+" términos que debo buscar en la base para responder a la pregunta? Ten en cuenta que con la información que obtengamos podemos buscar más veces. Responde sólamente los términos que haya que buscar, si hay que buscar alguno, poniendo cada uno en una linea separada. Si no hay ningun término para buscar, no me respondas nada.\n"+SYSTEM_REFLEXION
                    }
                ])   
                
        try:
            theResponse = str(response.choices[0].message.content)
        except (AttributeError, IndexError, TypeError):
            theResponse = ""    
        answers=theResponse.splitlines()
        self.completionTokens+=getattr(getattr(response, "usage", None), "total_tokens",0)
        logger.info("GordopiloDialog::askLLMForNewTerms() Response:"+str(answers))
        
        return answers

     def is_only_blank_or_punct(self, s: str) -> bool:
        return not s or re.fullmatch(r'[\s\W_]*', s) is not None
     
     # Takes a list of terms and searches them in the KG
     def searchTermsInKG(self, theTerms):
        logger.info("GordopiloDialog::searchTermsInKG():"+str(theTerms))
        response=""
        for term in theTerms:
            if self.is_only_blank_or_punct(term):
                continue 
            logger.info("Analyzing:["+term+"]in base embeddings")
            vector=self.get_embedding(term)
            res=self.kgiotdriver.searchByEmbeddings("allembeddings", self.parameters.nHitsKG, vector, "name")
            logger.info("GordopiloDialog::searchTermsInKG(). Searching "+str(self.parameters.nHitsKG)+" Terms. Located through embeddings "+str(len(res))+" elements")
            if len(res)>=1:
                for i in range(len(res)):
                    logger.info("GordopiloDialog::searchTermsInKG() Located through embeddings Node <<"+res[i][0]["name"]+">> with score "+str(res[i][1]))
                    if res[i][1] > 0.1 : # I had 0.9. Try with super low threshold
                        logger.info("GordopiloDialog::searchTermsInKG() Exploding Node <<"+res[i][0]["name"])
                        res2=self.kgiotdriver.readNodeAndLinked("%", [("name", res[i][0]["name"])], partial=False) #% means any type
                        response+="\n------------Beginning of Element----------------\n"
                        response+=self.formatNodeResult(res[i][0]["name"], res2)
                        response+="\n------------End of Element----------------\n"
        return response

     def extractTerms(self, text, n):
     
        # Define working LLM
        extractorModel=self.parameters.LLMModel  
        if not self.parameters.LLMModel :
            extractorModel=self.parameters.defaultLLMModel
            
        response = self.clientQuestion.chat.completions.create(
                model=extractorModel,
                response_format={ "type": "text" },
                messages=[
                    {"role": "system", "content": "normal"},
                    {"role": "user", "content": "He recibido el siguiente mensaje:\n------------Comienzo del mensaje----------------\n"+text+\
                    "\n------------Fin del mensaje----------------\n"+\
                    "Para poder responderlo voy a acceder a una base de datos en la que puedo buscar "+str(n)+" términos. ¿Cuales son los mejores "+str(n)+" términos que debo buscar en la base para responder a la pregunta? Responde sólamente los términos, poniendo cada uno en una linea separada.\n"+SYSTEM_REFLEXION}
                ])   
        try:
            theResponse = str(response.choices[0].message.content)
        except (AttributeError, IndexError, TypeError):
            theResponse = ""  
        answers=theResponse.splitlines()
        self.completionTokens+=getattr(getattr(response, "usage", None), "total_tokens",0)
        logger.info("GordopiloDialog::extractTermsText() Response:"+str(answers))
        
        return answers
