from openai import OpenAI
import math
client = OpenAI()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding
   #['data'][0]['embedding']

def distance(x1, x2):
    d=0
    for i in range(len(x1)):
        d+=(x2[i]-x1[i])*(x2[i]-x1[i])
    d=math.sqrt(d)
    return d
    
#x1=get_embedding("como cocinar patatas")
#x2=get_embedding("Napoleon nació en córcega")
#x3=get_embedding("quiero comer patatas")

#Por aqui, medir la distancia
#print("x2-x1", distance(x2, x1))
#print("x3-x1", distance(x3, x1))
#print("x3-x2", distance(x3, x2))

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  response_format={ "type": "text" },
  messages=[
    {"role": "system", "content": "Eres un sargento brutal gritando a un recluta."},
    {"role": "user", "content": "Cuentame un chiste."}
  ]
)
print(response.choices[0].message.content)