from openai import OpenAI



class KGIoTOpenAI():

    def __init__(self):
        self.client = OpenAI()
        
    def get_embedding(self, text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding