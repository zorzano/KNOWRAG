import argparse
import json


parser = argparse.ArgumentParser(
                    prog='generateQAFile',
                    description='Generate QA File from IRN file',
                    epilog='Knowledge and Things')
                    
parser.add_argument('inputfile', help="Name of IRN Json file to load")
parser.add_argument('outputfile', help="Name of IRN tagged file to generate")

args = parser.parse_args()

print("generateQAFile.  input file:"+args.inputfile)
print("generateQAFile. output file:"+args.outputfile)

fout=open(args.outputfile, "w", encoding="utf-8")

with open(args.inputfile, "r", encoding="utf-8") as fin:
    for i, linea in enumerate(fin, 1):
            campos = linea.strip().split('\t')
            if len(campos)<2:
                print("Error en linea "+str(i)+" "+linea)
                continue
            question = campos[0]
            answer = campos[1]
            fout.write(f"<Q> {question}\n")
            fout.write(f"<R> {answer}\n")
