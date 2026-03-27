# This code ammends some problems found in WC2014.txt. 
# Use: python correctIRNKG.py WC2014.txt > WC2014.ammend.1.txt
import sys
from openai import OpenAI

def getCountry(player):
    
    question="Give me the name of the national team of the football player "+player+". Give the answer just as a word with no punctuation symbols. Call the United States, USA. Call Bosnia Herzegovina Bosnia_&_Herzegovina. Call Ivory Coast Ivory_Coast. Call South Korea South_Korea. Call Costa Rica Costa_Rica.\n"
    
    response = client.chat.completions.create(
             model="chatgpt-4o-latest",
             response_format={ "type": "text" },
             messages=[
                {"role": "system", "content": "normal"},
                {"role": "user", "content": question}
             ])
    return response.choices[0].message.content
    
def main():
    
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    #print(parts[0], "\t", parts[1], "\t",parts[2])
                    if parts[1] == "plays_for_country" :
                        country = getCountry(parts[0])
                        print(parts[0],parts[1], country, sep='\t')
                    elif parts[1] == "plays_for_country_inverse" :
                        country = getCountry(parts[2])
                        print(country,parts[1], parts[2], sep='\t')
                    else:
                        print(parts[0],parts[1], parts[2], sep='\t')
                else:
                    print("Line with incorrect format:", line.strip())
    except FileNotFoundError:
        print(f"File not found: {filename}")

client = OpenAI()
if __name__ == "__main__":
    main()
