from KGIoTDriverNeo4j import KGIoTDriverNeo4j
import unittest
import logging
import sys
import os

class TestKGIoTDriver(unittest.TestCase):
    # Instantiate the final driver to test. And remember to import the corresponding class
    kgiotdriver = KGIoTDriverNeo4j("bolt://localhost:7687", "neo4j", os.getenv('PWDNEO4J'))

    def setUp(self):
        print("setUp TestKGIoT")

    def tearDown(self):
        print("tearDown TestKGIoT. Limpiando la base")
        # Comment this line to leave the base full
        self.kgiotdriver.nukeBase([("universe","test")])
        # self.kgiotdriver.nukeBase()

    def test_mergeNode01(self):
        res=self.kgiotdriver.mergeNode("Organization", [("name", "Telit"), ("contact", "me"), ("universe","test")])
        self.assertTrue(res==True)
        # Returns list of lists of Nodes.
        # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.graph.Node
        res=self.kgiotdriver.readNode("Organization", [("name", "Telit")])
        self.assertTrue(res[0][0]["name"]=="Telit")

    def test_mergeNode02(self):
        res=self.kgiotdriver.mergeNode("Organization", [("universe","test")])
        self.assertTrue(res==True)

    def test_mergeLink01(self):
        self.kgiotdriver.mergeNode("Organization", [("name", "Telit"), ("contact", "me"), ("universe","test")])
        self.kgiotdriver.mergeNode("Organization", [("name", "Quectel"), ("contact", "him"), ("universe","test")])
        res=self.kgiotdriver.mergeLink("IS",[("name", "theLink"), ("universe","test")], "Organization", [("name", "Telit"), ("contact", "me"), ("universe","test")], "Organization", [("name", "Quectel"), ("universe","test")])
        self.assertTrue(res==True)
        
    def test_mergeLinkPartialAttributes(self):
        self.kgiotdriver.mergeNode("Organization", [("name", "Telit"), ("contact", "me"), ("universe","test")])
        self.kgiotdriver.mergeNode("Organization", [("name", "Quectel"), ("contact", "him"), ("universe","test")])
        res=self.kgiotdriver.mergeLink("IS",[("name", "theLink"), ("universe","test")], "Organization", [("name", "Telit")], "Organization", [("name", "Quectel")])
        self.assertTrue(res==True)

    def test_readNodeAndLinked(self):
        self.kgiotdriver.mergeNode("Organization", [("name", "Queclink"), ("universe","test")])
        self.kgiotdriver.mergeNode("Product", [("name", "GL300W"), ("universe","test")])
        self.kgiotdriver.mergeNode("Country", [("name", "China"), ("universe","test")])
        self.kgiotdriver.mergeLink("manufacturer",[("name", "theLink"), ("universe","test")], "Organization", [("name", "Queclink"), ("universe","test")], "Product", [("name", "GL300W"), ("universe","test")])
        self.kgiotdriver.mergeLink("nationality",[("name", "theLink"), ("universe","test")], "Organization", [("name", "Queclink"), ("universe","test")], "Country", [("name", "China"), ("universe","test")])
        res=self.kgiotdriver.readNodeAndLinked("Organization", [("name", "Queclink"), ("universe","test")])
        # print(res[1])
        # print(isinstance(res[0][0], neo4j.graph.Relationship))
        self.assertTrue(res[0][1]["name"]=="theLink")
        self.assertTrue(res[1][1]["name"]=="theLink")
        self.assertTrue(res[0][0]["name"]=="Queclink")
        self.assertTrue(res[1][0]["name"]=="Queclink")
        self.assertTrue((res[0][2]["name"]=="China") or (res[0][2]["name"]=="GL300W"))
        self.assertTrue((res[1][2]["name"]=="China") or (res[1][2]["name"]=="GL300W"))
        # The type is in labels, which is a frozenset
        # x, *_ = (res[0][0].labels)


    def test_searchLinkChain1(self):
        self.kgiotdriver.mergeNode("Organization", [("name", "Queclink"),("universe","test")])
        self.kgiotdriver.mergeNode("Product", [("name", "GL300W"),("universe","test")])
        self.kgiotdriver.mergeNode("Service", [("name", "Asset Tracker"),("universe","test")])
        self.kgiotdriver.mergeNode("Service", [("name", "Tracking"),("universe","test")])
        self.kgiotdriver.mergeLink("manufacturer",[("name", "theLink"),("universe","test")], "Organization", [("name", "Queclink"),("universe","test")], "Product", [("name", "GL300W"),("universe","test")])
        self.kgiotdriver.mergeLink("providesService",[("name", "theLink"),("universe","test")], "Product", [("name", "GL300W"),("universe","test")], "Service", [("name", "Asset Tracker"),("universe","test")])
        self.kgiotdriver.mergeLink("serviceType",[("name", "theLink"),("universe","test")], "Service", [("name", "Asset Tracker"),("universe","test")], "Service", [("name", "Tracking"),("universe","test")])
        # Given a node, search for a chain of links in a specific direction, including options. Provide me with a list of all the objects you find 
        # Link direction: 1 outgoing, 2 incoming
        # First: test without directions
        res=self.kgiotdriver.searchLinkChain("Service", [("name", "Tracking"),("universe","test")], [("serviceType|providesService", 0), ("manufacturer",0)], "Organization")
        self.assertTrue(res[0][0]["name"]=="Queclink")

        # Next: test with directions
        res=self.kgiotdriver.searchLinkChain("Service", [("name", "Tracking"),("universe","test")], [("serviceType|providesService", 2), ("manufacturer",2)], "Organization")
        self.assertTrue(res[0][0]["name"]=="Queclink")
    
    def test_addEmbeddings(self):
        self.kgiotdriver.mergeNode("Process:Searchable", [("name", "Eat fruit"),("text", "TestTest"),("universe","test")]) 
        self.kgiotdriver.mergeNode("Process:Searchable", [("name", "Eat potatoes"),("text", "TestTest"),("universe","test")]) 
        thevector = [0] * 1536
        thevector[0]=0
        thevector[1]=1
        self.kgiotdriver.addEmbeddings("Searchable", "name", "Eat fruit", "embedding", thevector)
        thevector[0]=1
        thevector[1]=0
        self.kgiotdriver.addEmbeddings("Searchable", "name", "Eat potatoes", "embedding", thevector)
        thevector[0]=0.75
        thevector[1]=0
        res=self.kgiotdriver.searchByEmbeddings("allembeddings", 2, thevector, "name")
        self.assertTrue(res[0][0]["name"]=="Eat potatoes")
        self.assertTrue(res[0][1]==1)
        #self.assertTrue(res[1][0]["name"]=="Eat fruit")
        #self.assertTrue(res[1][1]<1)
        
        
if __name__ == '__main__':
    unittest.main()
