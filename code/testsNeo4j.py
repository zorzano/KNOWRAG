from neo4j import GraphDatabase


print ("Hello World")

class TM(object):

    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", os.getenv('PWDNEO4J')), encrypted=False)

    def getConcept(self, conceptName):
        with self._driver.session() as session:
            txresult = session.read_transaction(self._getConcept, conceptName)

        return txresult

    @staticmethod
    def _listifyIterable(iterable):
        list=[]
        for record in iterable:
            print("a")
            list.append(record)
        return list

    @staticmethod
    def _getConcept(tx, Concept):
    #        result = tx.run("MATCH (a:Concept {name:$s1}) "
    #                        "RETURN a.name + ', from node ' + id(a)", s1=Concept)
            result = tx.run("MATCH (a:Manufacturer) "
                            "RETURN a")
#result = tx.run("CREATE (test:Manufacturer {name:'Telit'})")

    #        values=[]
    #        for record in result:
    #            print("x")
    #            values.append(record[0])
    #            print(values[-1])
            return TM._listifyIterable(result)

ttm = TM()

r=ttm.getConcept("vox")
print(type(r))
for record in r:
    print("Record:",record[0].values())

# Si pido RETURN a y luego imprimo record[0] me da <Node id=0 labels=frozenset({'Manufacturer'}) properties={'name': 'Quectel'}>
