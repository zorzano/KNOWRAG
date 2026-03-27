import sys
from KGIoTDriverNeo4j import KGIoTDriverNeo4j
from KGIoTSynonims import KGIoTSynonims
import os
import csv
import time
import argparse
from KGIoTOpenAI import KGIoTOpenAI

clientOpenAI = KGIoTOpenAI()

fileFineTune = open("finetune.txt", 'a', encoding='utf-8')
templateOrganization = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Que es {organization}?"}}, {{"role": "assistant", "content": "{organization} es una Organización"}}]}}\n' 
templateProduct = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Que es {product}?"}}, {{"role": "assistant", "content": "{product} es un Producto"}}]}}\n' 
templateProductOrganization = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Quien hace el {product}?"}}, {{"role": "assistant", "content": "{organization} fabrica el producto{product}"}}]}}\n'
templateCountry = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿De que pais es {organization}?"}}, {{"role": "assistant", "content": "{organization} es de {country}"}}]}}\n'
templateContact = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Quien trabaja en {organization}?"}}, {{"role": "assistant", "content": "{contact} trabaja en {organization}"}}]}}\n'
templateKnows = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Quien conoce {organization}?"}}, {{"role": "assistant", "content": "{contact} tiene contacto con {organization}"}}]}}\n'
templateProvidesService = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Para que sirve {product}?"}}, {{"role": "assistant", "content": "{product} sirve para ofrecer el servicio de {service}"}}]}}\n'
templateServiceFather = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿A que familia pertenece el servicio {service}?"}}, {{"role": "assistant", "content": "El servicio {service} está dentro de {father}"}}]}}\n'
templateService = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Que es {service}?"}}, {{"role": "assistant", "content": "{service} es un servicio o funcionalidad empleado al construir servicios IoT."}}]}}\n'
templateWorksFor = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Para quien trabaja {provider}?"}}, {{"role": "assistant", "content": "{provider} trabaja para {provided}."}}]}}\n'
templateIsPartOf = '{{"messages": [{{"role": "system", "content": "normal"}}, {{"role": "user", "content": "¿Que es {son}?"}}, {{"role": "assistant", "content": "{son} es parte de {father}."}}]}}\n'

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
        #print(str(i)+"#"+f1[i]+"#"+father+"#"+f2[i]+"\n")
        if f1[i]!="":
            father=f1[i]
            if firstService==0:
                firstService=i
            print("Creando servicio de nivel superior "+father)
            kgiotdriver.mergeNode("Service:Searchable", [("name", father)])
            vector=clientOpenAI.get_embedding(father)
            kgiotdriver.addEmbeddings("Searchable", "name", father, "embedding", vector)
            printToFileFineTune(templateService.format(service=cleanForFineTune(father)))

        if f2[i]=="Platform":
            return f2, firstService, i
        if f2[i] != "" and father!="":
            print(f2[i]+"->"+father)
            kgiotdriver.mergeNode("Service:Searchable", [("name", f2[i])])
            printToFileFineTune(templateService.format(service=f2[i]))
            kgiotdriver.mergeLink("serviceType",[], "Service", [("name", f2[i])],  "Service", [("name", father)])
            vector=clientOpenAI.get_embedding(f2[i])
            kgiotdriver.addEmbeddings("Searchable", "name", f2[i], "embedding", vector)
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
            kgiotdriver.mergeNode("Organization:Searchable", [("name", manufacturer),("url", url)])
            kgiotdriver.addEmbeddings("Searchable", "name", manufacturer, "embedding", clientOpenAI.get_embedding(manufacturer))
            printToFileFineTune(templateOrganization.format(organization=cleanForFineTune(manufacturer)))
            
            kgiotdriver.mergeNode("Product:Searchable", [("name", model)])
            kgiotdriver.addEmbeddings("Searchable", "name", model, "embedding", clientOpenAI.get_embedding(model))
            printToFileFineTune(templateProduct.format(product=cleanForFineTune(model)))
            
            kgiotdriver.mergeLink("manufacturer",[], "Organization", [("name", manufacturer),("url", url)], "Product", [("name", model)])
            printToFileFineTune(templateProductOrganization.format(product=cleanForFineTune(model), organization=cleanForFineTune(manufacturer)))
            
            if(geo!=""):
                kgiotdriver.mergeNode("Country:Searchable", [("name", geo)])
                kgiotdriver.addEmbeddings("Searchable", "name", geo, "embedding", clientOpenAI.get_embedding(geo))
                kgiotdriver.mergeLink("nationality",[], "Organization", [("name", manufacturer),("url", url)], "Country", [("name", geo)])
                printToFileFineTune(templateCountry.format(country=cleanForFineTune(geo), organization=cleanForFineTune(manufacturer)))
            if(contactname!=""):
                kgiotdriver.mergeNode("Person:Searchable", [("name", contactname)])
                kgiotdriver.addEmbeddings("Searchable", "name", contactname, "embedding", clientOpenAI.get_embedding(contactname))
                kgiotdriver.mergeLink("WorksFor",[], "Person", [("name", contactname)],"Organization", [("name", manufacturer),("url", url)])
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(contactname), organization=cleanForFineTune(manufacturer)))
                
            if(tefcontactname!=""):
                kgiotdriver.mergeNode("Person:Searchable", [("name", tefcontactname)])
                kgiotdriver.addEmbeddings("Searchable", "name", tefcontactname, "embedding", clientOpenAI.get_embedding(tefcontactname))
                kgiotdriver.mergeLink("knowsAbout",[], "Person", [("name", tefcontactname)],"Organization", [("name", manufacturer),("url", url)])
                kgiotdriver.mergeLink("WorksFor",[], "Person", [("name", tefcontactname)],"Organization", [("name", "Telefonica"),("url", "http://www.telefonica.com")])
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune("Telefonica")))
                printToFileFineTune(templateKnows.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune(manufacturer)))
            print("Inserted manufacturer:"+manufacturer+", url:"+url+", model:"+model+","+geo+", contactname:"+contactname+", tefcontactname:"+tefcontactname)
            for i in range (firstService,maxServices):
                if fields[i] != "" and headers[i] != "" :
                    kgiotdriver.mergeLink("providesService",[], "Product", [("name", model)],  "Service", [("name", headers[i])])
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
            try:
                kgiotdriver.mergeLink(fields[1],[], "Concept", [("name", fields[0])],  "Concept", [("name", fields[2])])
            except Exception as e:
                print("Error:", e)
            
            
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
            kgiotdriver.mergeNode("Organization:Searchable", [("name", manufacturer),("url", url)])
            kgiotdriver.addEmbeddings("Searchable", "name", manufacturer, "embedding", clientOpenAI.get_embedding(manufacturer))
            printToFileFineTune(templateOrganization.format(organization=cleanForFineTune(manufacturer)))

            if(geo!=""):
                kgiotdriver.mergeNode("Country:Searchable", [("name", geo)])
                kgiotdriver.addEmbeddings("Searchable", "name", geo, "embedding", clientOpenAI.get_embedding(geo))
                kgiotdriver.mergeLink("nationality",[], "Organization", [("name", manufacturer),("url", url)], "Country", [("name", geo)])
                print("Inserting "+manufacturer+"-nationality-"+geo)
                printToFileFineTune(templateCountry.format(country=cleanForFineTune(geo), organization=cleanForFineTune(manufacturer)))
                
            if(model!=""):
                kgiotdriver.mergeNode("Product:Searchable", [("name", model)])
                kgiotdriver.addEmbeddings("Searchable", "name", model, "embedding", clientOpenAI.get_embedding(model))
                kgiotdriver.mergeLink("manufacturer",[], "Organization", [("name", manufacturer),("url", url)], "Product", [("name", model)])
                print("Inserting "+manufacturer+"-manufacturer-"+model)
                printToFileFineTune(templateProductOrganization.format(product=cleanForFineTune(model), organization=cleanForFineTune(manufacturer)))
                
            if(devicemode!=""):
                kgiotdriver.mergeNode("Service:Searchable", [("name", devicemode)])
                kgiotdriver.addEmbeddings("Searchable", "name", devicemode, "embedding", clientOpenAI.get_embedding(devicemode))
                kgiotdriver.mergeLink("providesService",[], "Product", [("name", model)],  "Service", [("name", devicemode)])
                print("Inserting "+model+"-providesService-"+devicemode)
                printToFileFineTune(templateProvidesService.format(service=cleanForFineTune(devicemode), product=cleanForFineTune(model)))
                
            if(devicetype!=""):
                kgiotdriver.mergeNode("Service:Searchable", [("name", devicetype)])
                kgiotdriver.addEmbeddings("Searchable", "name", devicetype, "embedding", clientOpenAI.get_embedding(devicetype))
                print("Creating devicetype "+devicetype)
            if(deviceusecase!=""):
                for x in deviceusecase.split(" "):
                    if any(char.isalnum() for char in x):
                        print("Inserting "+model+"-providesService-"+x)
                        kgiotdriver.mergeNode("Service:Searchable", [("name", x)])
                        printToFileFineTune(templateService.format(service=x))
                        kgiotdriver.addEmbeddings("Searchable", "name", x, "embedding", clientOpenAI.get_embedding(x))
                        kgiotdriver.mergeLink("providesService",[], "Product", [("name", model)],  "Service", [("name", x)]) 
                        printToFileFineTune(templateProvidesService.format(service=cleanForFineTune(x), product=cleanForFineTune(model))) 
                        
                        if(devicetype!=""):
                            kgiotdriver.mergeLink("serviceType",[], "Service", [("name", x)],  "Service", [("name", devicetype)])
                            print("Inserting "+x+"-serviceType-"+devicetype)
                            printToFileFineTune(templateServiceFather.format(service=cleanForFineTune(x), father=cleanForFineTune(devicetype)))
                            
            if(contactname!="" or contactmail!=""):
                kgiotdriver.mergeNode("Person:Searchable", [("name", contactname),("email", contactmail)])
                kgiotdriver.addEmbeddings("Searchable", "name", contactname, "embedding", clientOpenAI.get_embedding(contactname))
                kgiotdriver.mergeLink("WorksFor",[], "Person", [("name", contactname),("email", contactmail)],"Organization", [("name", manufacturer),("url", url)])
                print("Inserting "+contactname+"-WorksFor-"+manufacturer)
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(contactname), organization=cleanForFineTune(manufacturer)))
                
            if(tefcontactname!="" or tefcontactmail!=""):
                kgiotdriver.mergeNode("Person:Searchable", [("name", tefcontactname),("email", tefcontactmail)])
                kgiotdriver.addEmbeddings("Searchable", "name", tefcontactname, "embedding", clientOpenAI.get_embedding(tefcontactname))
                kgiotdriver.mergeLink("knowsAbout",[], "Person", [("name", tefcontactname),("email", tefcontactmail)],"Organization", [("name", manufacturer),("url", url)])
                print("Inserting "+tefcontactname+"-knowsAbout-"+manufacturer)
                kgiotdriver.mergeLink("WorksFor",[], "Person", [("name", tefcontactname),("email", tefcontactmail)],"Organization", [("name", "Telefonica"),("url", "http://www.telefonica.com")])
                print("Inserting "+tefcontactname+"-WorksFor-"+"Telefonica")
                printToFileFineTune(templateContact.format(contact=cleanForFineTune(tefcontactname), organization="Telefonica"))
                printToFileFineTune(templateKnows.format(contact=cleanForFineTune(tefcontactname), organization=cleanForFineTune(manufacturer)))
                
            if(ob!=""):
                kgiotdriver.mergeNode("Organization:Searchable", [("name", ob),("url", "http://www.telefonica.com")])
                kgiotdriver.addEmbeddings("Searchable", "name", ob, "embedding", clientOpenAI.get_embedding(ob))
                kgiotdriver.mergeLink("WorksFor",[], "Organization", [("name", manufacturer),("url", url)],"Organization", [("name", ob),("url", "http://www.telefonica.com")])
                print("Inserting "+manufacturer+"-WorksFor-"+ob)
                printToFileFineTune(templateWorksFor.format(provider=cleanForFineTune(manufacturer), provided=cleanForFineTune(ob)))
                kgiotdriver.mergeLink("ISPARTOF",[], "Organization", [("name", ob),("url", "http://www.telefonica.com")],"Organization", [("name", "Telefonica"),("url", "http://www.telefonica.com")])
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

kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))
kgiotdriver.mergeNode("Organization", [("name", "Telefonica"),("url", "http://www.telefonica.com")])

if args.kill :
    kgiotdriver.nukeBase()

if(args.dictionary != None):
    kgiotsynonims=KGIoTSynonims(args.dictionary)
else:
    kgiotsynonims=KGIoTSynonims("")

if args.format=="s" :
    loadSalvaFormat(args, kgiotsynonims, kgiotdriver)
elif args.format=="z" :
    loadZorzoFormat(args, kgiotsynonims, kgiotdriver)
elif args.format=="m" :
    loadCSVTabFormat(args, kgiotsynonims, kgiotdriver)