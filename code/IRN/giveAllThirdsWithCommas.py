# This code ammends some problems found in WC2014.txt. 
# Use: python giveAllThirdsWithCommas.py WC2014.txt England plays_for_country_inverse
# Returns all matching thirds separated by commas
import sys

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
    
    if len(sys.argv) < 4:
        print("Usage: python script.py <filename> first_triplet_term second_triplet_term")
        return

    filename = sys.argv[1]

    try:
        result=""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    if (parts[0] == sys.argv[2]) and (parts[1] == sys.argv[3]) :
                        result+=parts[2]+","
                else:
                    print("Line with incorrect format:", line.strip())
        print(result)
        
    except FileNotFoundError:
        print(f"File not found: {filename}")

if __name__ == "__main__":
    main()
