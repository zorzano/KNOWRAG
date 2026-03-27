from neo4j import GraphDatabase
from KGIoTDriver import KGIoTDriver
import os

class KGIoTDriverNeo4j(KGIoTDriver):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    @staticmethod
    def _listifyIterable(iterable):
        list=[]
        for record in iterable:
            list.append(record)
        return list

    @staticmethod
    def _createValueHolder(attributes):
        if (len(attributes) >0):
            valueHolder=" {"
            for atr,val in attributes:
                valueHolder+=str(atr)+":'"+str(val)+"' ,"
            valueHolder=valueHolder[:-1]
            valueHolder+="} "
        else:
            valueHolder=""
        return valueHolder
        
    def _createValueHolderPartial(attributes):
        if (len(attributes) >0):
            valueHolder=""
            for atr,val in attributes:
                valueHolder+="toLower(c1."+str(atr)+") CONTAINS toLower('"+str(val)+"') AND "
            valueHolder=valueHolder[:-4] #Delete the last AND
        else:
            valueHolder=""
        return valueHolder

    def nukeBase(self, attributes=[]):
        with self._driver.session() as session:
            txresult = session.execute_write(self._nukeBase, attributes)
            return txresult

    # Type is a string with the item name.
    # attributes = [("a", 1), ("b", 2), ("c", 3)]
    # returns an array of arrays of dictionaries. The [0][0] dictionary is composed by atr-val pairs
    def readNode(self, type, attributes, partial=False):
        with self._driver.session() as session:
            txresult = session.execute_read(self._readNode, type, attributes, partial)
            return txresult

    def readNodeAndLinked(self, type, attributes, partial=False):
        with self._driver.session() as session:
            txresult = session.execute_read(self._readNodeAndLinked, type, attributes, partial)
            return txresult

    # Type is a string with the item name.
    # attributes = [("a", 1), ("b", 2), ("c", 3)]
    # Creates or merges the node. Returns TRUE if can do it.
    def mergeNode(self, type, attributes):
        with self._driver.session() as session:
            txresult = session.execute_write(self._mergeNode, type, attributes)
            return txresult

    # Type is a string with the item name.
    # attributes = [("a", 1), ("b", 2), ("c", 3)]
    # Creates or merges the node. Returns TRUE if can do it.
    def mergeLink(self, typeLink, attributesLink, typeA, attributesA, typeB, attributesB):
        with self._driver.session() as session:
            txresult = session.execute_write(self._mergeLink, typeLink, attributesLink, typeA, attributesA, typeB, attributesB)
            return txresult
    
    # self.kgiotdriver.searchLinkChain("Service", "name", "Tracking", [("serviceType|providesService", 1), ("manufacturer",0)], "Organization")
    # Given a node, search for a chain of links in a specific direction, including options. Provide me with a list of all the objects you find 
    # 1 outgoing, 2 inoming, 0, any direction
    def searchLinkChain(self, typeOrigin, attributesA, listLinks, typeResults):
        with self._driver.session() as session:
            txresult = session.execute_read(self._searchLinkChain, typeOrigin, attributesA, listLinks, typeResults)
            return txresult
            
    # add a vector to an item, for embeddings
    def addEmbeddings(self, typeObject, objectIdParameter, objectIdValue, nameParameter, embeddings):
        with self._driver.session() as session:
            txresult = session.execute_write(self._addEmbeddings, typeObject, objectIdParameter, objectIdValue, nameParameter, embeddings)
            return txresult
    # search an item according to a vector, for embeddings
    def searchByEmbeddings(self, indexName, numberResults, targetVector, idParameter):
        with self._driver.session() as session:
            txresult = session.execute_read(self._searchByEmbeddings, indexName, numberResults, targetVector, idParameter)
            return txresult

    @staticmethod
    def _nukeBase(tx, attributes):
        valueHolder=KGIoTDriverNeo4j._createValueHolder(attributes)
        result = tx.run("MATCH ("+valueHolder+")-[r]-() "
                        "DELETE r ")
        result = tx.run("MATCH (a"+valueHolder+") "
                        "DELETE a ")

        return KGIoTDriverNeo4j._listifyIterable(result)


    @staticmethod
    def _readNode(tx, type, attributes, partial):
        if partial :
            valueHolder=KGIoTDriverNeo4j._createValueHolderPartial(attributes)
            result = tx.run("MATCH (c1:"+type+")"
                            "WHERE "+valueHolder+" "
                            "RETURN c1")
        else:
            valueHolder=KGIoTDriverNeo4j._createValueHolder(attributes)
            result = tx.run("MATCH (c1:"+type+valueHolder+") "
                            "RETURN c1 ")
        return KGIoTDriverNeo4j._listifyIterable(result)
        

    @staticmethod
    def _readNodeAndLinked(tx, type, attributes, partial):
        if partial :
            valueHolder=KGIoTDriverNeo4j._createValueHolderPartial(attributes)
            result = tx.run("MATCH (c1:"+type+")-[r]-(c2)"
                            "WHERE "+valueHolder+" "
                            "RETURN c1, r, c2")
            
        else:
            valueHolder=KGIoTDriverNeo4j._createValueHolder(attributes)
            result = tx.run("MATCH (c1:"+type+valueHolder+")-[r]-(c2)"            
                            "RETURN c1, r, c2")            
            
        resultlist=KGIoTDriverNeo4j._listifyIterable(result)
         
        if not resultlist:
            if partial: 
                result = tx.run("MATCH (c1:"+type+")"
                                "WHERE "+valueHolder+" "
                                "RETURN c1")
            else:
                result = tx.run("MATCH (c1:"+type+valueHolder+") "
                                "RETURN c1 ")
            resultlist=KGIoTDriverNeo4j._listifyIterable(result)
         
        return resultlist
        

    @staticmethod
    def _mergeNode(tx, type, attributes):
        valueHolder=KGIoTDriverNeo4j._createValueHolder(attributes)
        result = tx.run("MERGE (c1:"+type+valueHolder+") "
                        "RETURN c1.name ")

        return True

    @staticmethod
    def _mergeLink(tx, typeLink, attributesLink, typeA, attributesA, typeB, attributesB):
        valueHolderLink=KGIoTDriverNeo4j._createValueHolder(attributesLink)
        valueHolderA=KGIoTDriverNeo4j._createValueHolder(attributesA)
        valueHolderB=KGIoTDriverNeo4j._createValueHolder(attributesB)


        result = tx.run("MATCH (o:"+typeA+valueHolderA+") "
                        "MATCH (d:"+typeB+valueHolderB+") "
                        "MERGE (o)-[:"+typeLink+valueHolderLink+"]->(d);")
        return True

    @staticmethod
    def _searchLinkChain(tx, typeOrigin, attributesA, listLinks, typeResults):
        linkSequence=""
        for index, item in enumerate(listLinks):
            if index != 0:
                linkSequence+="()"
            if item[1]==2:
                linkSequence+="<"
            linkSequence+="-[:"+item[0]+"*1..]-"
            if item[1]==1:
                linkSequence+=">"
        valueHolderA=KGIoTDriverNeo4j._createValueHolder(attributesA)    
        # print("MATCH (t1:"+typeOrigin+"{"+atrIdOrigin+":'"+valueIdOrigin+"'})"+linkSequence+"(t4:"+typeResults+") ")    
        result=tx.run("MATCH (t1:"+typeOrigin+valueHolderA+")"+linkSequence+"(t4:"+typeResults+") "
                      "RETURN DISTINCT t4;")
        return KGIoTDriverNeo4j._listifyIterable(result)
    
    @staticmethod
    def _addEmbeddings(tx, typeObject, objectIdParameter, objectIdValue, nameParameter, embeddings):
        result = tx.run("MATCH (n:"+typeObject+" {"+objectIdParameter+": $qobjectIdValue}) "
                        "CALL db.create.setNodeVectorProperty(n, '"+nameParameter+"', $qembeddings) "
                        "RETURN n; ", 
                        qobjectIdValue=objectIdValue, qembeddings=embeddings)
        return result
        
    @staticmethod
    def _searchByEmbeddings(tx, indexName, numberResults, targetVector, idParameter):
        result = tx.run("CALL db.index.vector.queryNodes('"+indexName+"', $qnumberResults, $qtargetVector) "
                        "YIELD node AS xnode, score "
                        "MATCH (xnode) "
                        #"RETURN xnode."+idParameter+", score;", 
                        "RETURN xnode, score;", 
                        qnumberResults=numberResults, qtargetVector=targetVector)
        return KGIoTDriverNeo4j._listifyIterable(result)