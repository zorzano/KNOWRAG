# Generate Fine Tune File from IRN questions file
# Usage: generateFineTuneFile WC-P.ammend.1.txt finetuneIRN.txt
import argparse
import json

def cleanForFineTune(line):
    line=line.replace("\\", "/")
    line=line.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
    line=line.replace('"', '\\"').replace("'", "")
    line=line.replace("\t", "\\t")
    return line

parser = argparse.ArgumentParser(
                    prog='generateFineTuneFile',
                    description='Generate Fine Tune File from IRN file',
                    epilog='Knowledge and Things')
                    
parser.add_argument('inputfile', help="Name of IRN file to load")
parser.add_argument('outputfile', help="Name of IRN tagged file to generate")

args = parser.parse_args()

print("generateFineTuneFile.  input file:"+args.inputfile)
print("generateFineTuneFile. output file:"+args.outputfile)

fout=open(args.outputfile, "w", encoding="utf-8")
templateIRN = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "{thisquestion}"}}, {{"role": "assistant", "content": "{thisanswer}"}}]}}\n' 

with open(args.inputfile, "r", encoding="utf-8") as fin:
    for i, linea in enumerate(fin, 1):
            campos = linea.strip().split('\t')
            if len(campos)<2:
                print("Error en linea "+str(i)+" "+linea)
                continue
            question = campos[0]
            answer = campos[1]
            fout.write(templateIRN.format(thisquestion=cleanForFineTune(question), thisanswer=cleanForFineTune(answer)))
