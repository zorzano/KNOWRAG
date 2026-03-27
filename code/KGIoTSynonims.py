
class KGIoTSynonims():



    def __init__(self, pathfile):
        self.dicti={}
        if(pathfile==""):
            return
        else:
            with open(pathfile) as f:
                line = f.readline()
                while line:
                    if (not line.startswith((" ", "\t"))):
                        left=line.strip()
                    else:
                        self.dicti[line.strip()]=left
                    line = f.readline()
        #print(self.dicti)


    def map(self, input):
        return self.dicti.get(input, input)

    #Pretty heavy function.
    def substituteAny(self, input):
        theString=input
        for x in self.dicti:
            theString=theString.replace(x, self.dicti[x])
        return theString
