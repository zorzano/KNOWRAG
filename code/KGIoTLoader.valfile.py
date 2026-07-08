import sys
import os
import csv
import time
import argparse
from KGIoTSynonims import KGIoTSynonims

fileFineTune = open("finetune.txt", 'a', encoding='utf-8')

# Templates for validation file
templateOrganization = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿En una palabra, que es {organization}?"}}, {{"role": "assistant", "content": "Organización"}}]}}\n' 
templateProduct = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿En una palabra, que es {product}?"}}, {{"role": "assistant", "content": "Producto"}}]}}\n' 
templateProductOrganization = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Quien hace el {product}? Di solo su nombre"}}, {{"role": "assistant", "content": "{organization}"}}]}}\n'
templateCountry = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿De que pais es {organization}? Di solo su nombre"}}, {{"role": "assistant", "content": "{country}"}}]}}\n'
templateContact = ''
templateKnows = ''
templateProvidesService = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Que servicio ofrece {product}? Di solo su nombre"}}, {{"role": "assistant", "content": "{service}"}}]}}\n'
templateServiceFather = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "Di el nombre de la familia a la que pertenece el servicio {service}"}}, {{"role": "assistant", "content": "{father}"}}]}}\n'
templateService = ''
templateWorksFor = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "Di en una palabra para quien trabaja {provider}?"}}, {{"role": "assistant", "content": "{provided}"}}]}}\n'
templateIsPartOf = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿De que es parte {son}? Dilo en una palabra"}}, {{"role": "assistant", "content": "{father}."}}]}}\n'

def printToFileFineTune(line):
    fileFineTune.write(line)

def cleanForFineTune(line):
    line=line.replace("\\", "/")
    line=line.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
    line=line.replace('"', '\\"').replace("'", "\\'")
    line=line.replace("\t", "\\t")
    return line
    
def loadZorzoFormatFirstTwoLines(f1, f2, kgiotdriver):
    print(f1, "\n")
    print(f2, "\n")
    father=""
    firstService=0
    for i in range (1,len(f2)):        
        if f1[i]!="":
            father=f1[i]
            if firstService==0:
                firstService=i
            print("Creando servicio de nivel superior "+father)
            printToFileFineTune(templateService.format(service=cleanForFineTune(father)))

        if f2[i]=="Platform":
            return f2, firstService, i
        if f2[i] != "" and father!="":
            print(f2[i]+"->"+father)
            printToFileFineTune(templateService.format(service=f2[i]))
            printToFileFineTune(templateServiceFather.format(service=cleanForFineTune(f2[i]), father=cleanForFineTune(father)))

    return f2, firstService, i
    
def loadZorzoFormat(args, kgiotsynonims, kgiotdriver):
    with open(args.filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers, firstService, maxServices=loadZorzoFormatFirstTwoLines(reader.__next__(), reader.__next__(), kgiotdriver)
        for fields in reader:
            print(fields)
            for indice, elemento in enumerate(fields):
                print(str(indice)+":"+elemento)
            manufacturer=fields[0]
            model="Generic "+manufacturer+" product"
            url=fields[2]
            mainActivity=fields[3] #Temporarily not used
            geo=fields[4]
            # MUST ADJUST IF FILE CHANGES
            platform=fields[153] #Temporarily not used
            tier=fields[154] #Temporarily not used
            contactname=fields[173] 
            tefcontactname=fields[174] 
            referenceProject=fields[157] #Temporarily not used
            if(manufacturer==""):
                continue
            printToFileFineTune(templateOrganization.format(organization=cleanForFineTune(manufacturer)))            
            printToFileFineTune(templateProduct.format(product=cleanForFineTune(model)))
            printToFileFineTune(templateProductOrganization.format(product=cleanForFineTune(model), organization=cleanForFineTune(manufacturer)))
            
            if(geo!=""):
                printToFileFineTune(templateCountry.format(country=cleanForFineTune(geo), organization=cleanForFineTune(manufacturer)))
            if(contactname!=""):
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(contactname), organization=cleanForFineTune(manufacturer)))
                
            if(tefcontactname!=""):
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune("Telefonica")))
                printToFileFineTune(templateKnows.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune(manufacturer)))
            print("Inserted manufacturer:"+manufacturer+", url:"+url+", model:"+model+","+geo+", contactname:"+contactname+", tefcontactname:"+tefcontactname)
            for i in range (firstService,maxServices):
                if fields[i] != "" and headers[i] != "" :
                    printToFileFineTune(templateProvidesService.format(service=cleanForFineTune(headers[i]), product=cleanForFineTune(model)))
                    print(manufacturer+" provides "+headers[i]+" service")

#For a file of the form IdeaTABRelationTABIdea. This format is not used in the final experiment, as I prefer to use the json file. The TAB file is huge
def loadCSVTabFormat(args, kgiotsynonims, kgiotdriver):
    with open(args.filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        count=0
        for fields in reader:
            count+=1
            # print(str(count)+" "+fields[0]+" "+fields[1]+" "+fields[2])
            if (count%1000)==0:
                print(str(count))
            fields[0]=fields[0].replace("'","")
            fields[1]=fields[1].replace("'","").replace(" ","_").replace("(", "").replace(")", "").replace(",", "_").replace("/", "_").replace("-", "_")
            fields[2]=fields[2].replace("'","")
            
            
def loadSalvaFormat(args, kgiotsynonims, kgiotdriver):
    with open(args.filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        reader.__next__()
        for fields in reader:
            print(fields)
            for index, item in enumerate(fields):
                fields[index]=kgiotsynonims.substituteAny(fields[index])
                fields[index]=item.strip(" \"")
                fields[index] = fields[index].replace("\\N", "")
                fields[index]=kgiotsynonims.map(fields[index])
                print(index, " ", fields[index])
            customer=fields[1]
            manufacturer=fields[2]
            model=fields[3]
            devicemode=fields[4]
            devicetype=fields[5]
            deviceusecase=fields[6]
            if(model=="" and ((deviceusecase!="") or (devicetype!=""))):
                #model="Generic "+manufacturer+" product"
                continue # This product comes from the Zorzano CVS. Better get it from there
            deviceprice=fields[7]
            url=fields[8]
            geo=fields[9]
            contactname=fields[10]
            contactmail=fields[11]
            tefcontactname=fields[12]
            tefcontactmail=fields[13]
            ob=fields[14]
            source=fields[15] # Not used yet
            user=fields[16] # Not used yet

            if(manufacturer==""):
                continue
            printToFileFineTune(templateOrganization.format(organization=cleanForFineTune(manufacturer)))

            if(geo!=""):
                print("Inserting "+manufacturer+"-nationality-"+geo)
                printToFileFineTune(templateCountry.format(country=cleanForFineTune(geo), organization=cleanForFineTune(manufacturer)))
                
            if(model!=""):
                print("Inserting "+manufacturer+"-manufacturer-"+model)
                printToFileFineTune(templateProductOrganization.format(product=cleanForFineTune(model), organization=cleanForFineTune(manufacturer)))
                
            if(devicemode!=""):
                print("Inserting "+model+"-providesService-"+devicemode)
                printToFileFineTune(templateProvidesService.format(service=cleanForFineTune(devicemode), product=cleanForFineTune(model)))
                
            if(devicetype!=""):
                print("Creating devicetype "+devicetype)
            if(deviceusecase!=""):
                for x in deviceusecase.split(" "):
                    if any(char.isalnum() for char in x):
                        print("Inserting "+model+"-providesService-"+x)
                        printToFileFineTune(templateService.format(service=x))
                        printToFileFineTune(templateProvidesService.format(service=cleanForFineTune(x), product=cleanForFineTune(model))) 
                        
                        if(devicetype!=""):
                            print("Inserting "+x+"-serviceType-"+devicetype)
                            printToFileFineTune(templateServiceFather.format(service=cleanForFineTune(x), father=cleanForFineTune(devicetype)))
                            
            if(contactname!="" or contactmail!=""):
                print("Inserting "+contactname+"-WorksFor-"+manufacturer)
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(contactname), organization=cleanForFineTune(manufacturer)))
                
            if(tefcontactname!="" or tefcontactmail!=""):
                print("Inserting "+tefcontactname+"-knowsAbout-"+manufacturer)
                print("Inserting "+tefcontactname+"-WorksFor-"+"Telefonica")
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(tefcontactname), organization="Telefonica"))
                printToFileFineTune(templateKnows.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune(manufacturer)))
                
            if(ob!=""):
                print("Inserting "+manufacturer+"-WorksFor-"+ob)
                printToFileFineTune(templateWorksFor.format(provider=cleanForFineTune(manufacturer), provided=cleanForFineTune(ob)))
                print("Inserting "+ob+"-ISPARTOF-Telefonica")
                printToFileFineTune(templateIsPartOf.format(son=cleanForFineTune(ob), father="Telefonica"))

parser = argparse.ArgumentParser(
                    prog='KG IoT Loader',
                    description='Load KITI base from CSV files',
                    epilog='Knowledge and Things')
                    
parser.add_argument('filename', help="Name of CSV file to load")
parser.add_argument('-d', dest="dictionary", help="Dictionary file")
parser.add_argument('-k', dest="kill", help="Empty database", action="store_true")
parser.add_argument('-f', dest="format", help="File format. s for Salva, z for Zorzano, m for MINTQA", choices=["s", "z", "m"])

args = parser.parse_args()

if(args.dictionary != None):
    kgiotsynonims=KGIoTSynonims(args.dictionary)
else:
    kgiotsynonims=KGIoTSynonims("")

if args.format=="s" :
    loadSalvaFormat(args, kgiotsynonims, None)
elif args.format=="z" :
    loadZorzoFormat(args, kgiotsynonims, None)
elif args.format=="m" :
    loadCSVTabFormat(args, kgiotsynonims, None)