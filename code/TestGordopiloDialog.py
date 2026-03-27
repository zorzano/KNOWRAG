import unittest
import logging
import sys
from GordopiloDialog import GordopiloDialog, GordopiloParameters

logger = logging.getLogger(__name__)
logging.basicConfig(filename='testGordopiloDialog.log', level=logging.INFO)
gpp=GordopiloParameters()
gpp.of=open("TestGordopiloDialog.OutputFile.txt", 'w', encoding='utf-8')

class TestGordopiloDialog(unittest.TestCase):
    
    def setUp(self):
        print("setUp TestGordopiloDialog")
        self.gp=GordopiloDialog()
        self.gp.setParameters(gpp)

    def tearDown(self):
        print("tearDown TestGordopiloDialog")
        self.gp.close()
        gpp.LLMModel="gpt-4o-2024-11-20"
        gpp.KG=True
        gpp.nHitsKG=1
        gpp.extractTerms=0
        self.gp.setParameters(gpp)

    def test_01(self):
        self.assertTrue(1==1)
    
    def test_02(self):
        answer=self.gp.answerText("Quectel?")
        print(answer)
        self.assertTrue("Quectel" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)
    
    def test_03(self):
        answer=self.gp.answerText("Agrosmart?")
        print(answer)
        self.assertTrue("Agrosmart" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)

    def test_04(self):
        answer=self.gp.answerText("BC95?")
        print(answer)
        self.assertTrue("Quectel" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)

        
    def test_05(self):
        answer=self.gp.answerText("Gordopilo?")
        print(answer)
        self.assertTrue("Gordopilo" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)


    def test_06(self):
        answer=self.gp.answerText("NB-IoT?")
        print(answer)
        self.assertTrue("NB-IoT" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)

    def test_07(self):
        answer=self.gp.answerText("Cat1?")
        print(answer)
        self.assertTrue("Cat1" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)
        
    def test_08(self):
        answer=self.gp.answerText("¿Que sabes de Marta Cerezo <Marta.Cerezo@dahuatech.com>?")
        print(answer)
        self.assertTrue("Dahua" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)
   
    def test_09(self):
        answer=self.gp.answerText("Hablame de Asset Tracking.")
        print(answer)
        self.assertTrue("Tracking" in answer)
        self.assertTrue("[*]" not in answer)   
        self.assertTrue("Searchable" not in answer)
        
    def test_10(self):
        answer=self.gp.answerText("Normativa corporativa?")
        print(answer)
        self.assertTrue("ormativa" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)

    def test_11(self) :
        answer=self.gp.answerText("Hablame de la normativa corporativa.")
        print(answer)
        self.assertTrue("ormativa" in answer)
        self.assertTrue("[*]" not in answer)
        self.assertTrue("Searchable" not in answer)
        
    # LLM Model = None
    def test_12(self) :
        gpp.LLMModel=None
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Hablame de Telit.")
        print(answer)
        self.assertTrue("manufacturer:" in answer)
        self.assertTrue("Nieves" in answer)

    # KG = False
    def test_13(self) :
        gpp.KG=False
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Hablame de Telit.")
        print(answer)
        self.assertTrue("ódulo" in answer)
        self.assertTrue("Nieves" not in answer)

   #  nHitsKG=5
    def test_14(self) :
        gpp.nHitsKG=5
        gpp.LLMModel=None
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Hablame de Telit.")
        print(answer)
        self.assertTrue(answer.count("Name:")==5)
    
    #  nHitsKG=5    
    def test_15(self) :
        gpp.nHitsKG=5
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Hablame de Telit.")
        print(answer)
        self.assertTrue("ódulos" in answer)
        self.assertTrue("Nieves" in answer)
        
    #  extractTerms=5, no LLM
    def test_16(self) :
        gpp.extractTerms=5
        gpp.LLMModel=None
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Necesito que me den información sobre Telit y Qualcomm.")
        print(answer)
        self.assertTrue("odules" in answer)
        self.assertTrue("Douglas" in answer)

    #  extractTerms=5, no LLM
    def test_17(self) :
        gpp.extractTerms=5
        self.gp.setParameters(gpp)
        answer=self.gp.answerText("Necesito que me den información sobre Telit y Qualcomm.")
        print(answer)
        self.assertTrue("ódulo" in answer)
        self.assertTrue("Douglas" in answer)

        
if __name__ == '__main__':
    unittest.main()
