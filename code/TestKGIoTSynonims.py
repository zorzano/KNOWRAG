import unittest
import os
from KGIoTSynonims import KGIoTSynonims

class TestKGIoTSynonims(unittest.TestCase):
    # Instantiate the final driver to test. And remember to import the corresponding class

    def setUp(self):
        print("setUp TestKGIoTSynonims")
        f = open("KGIoTSynonimsTest.txt", "w")
        f.write("Hola\n")
        f.write(" Caracola\n")
        f.write("Andres\n")
        f.write(" Ruiz\n")
        f.write(" Escudero\n")
        f.close()

    def tearDown(self):
        print("tearDown TestKGIoTSynonims. Limpiando la base")
        os.remove("KGIoTSynonimsTest.txt")

    def test_map01(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.map("Caracola")=="Hola")

    def test_map02(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.map("Escudero")=="Andres")
        self.assertTrue(sn.map("Ruiz")=="Andres")

    def test_map03(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.map("Cara")=="Cara")

    def test_map031(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.map("")=="")
        self.assertTrue(sn.map(" ")==" ")
        self.assertTrue(sn.map("  ")=="  ")

    def test_map04(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.substituteAny("CaraRuiz")=="CaraAndres")

    def test_map05(self):
        sn=KGIoTSynonims("KGIoTSynonimsTest.txt")
        self.assertTrue(sn.substituteAny("")=="")
        self.assertTrue(sn.substituteAny(" ")==" ")



if __name__ == '__main__':
    unittest.main()
