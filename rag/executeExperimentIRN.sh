#!/bin/bash

../data/loadbaseIRN.sh

#IRN World Cup
python3 ../code/RAGAskQuestions.py -filename=C301/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C301/output.txt -resultfile=C301/rateresults.txt
mv RAGCompareAnswers.log C301/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C302/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C302/output.txt -resultfile=C302/rateresults.txt
mv RAGCompareAnswers.log C302/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C303/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C303/output.txt -resultfile=C303/rateresults.txt
mv RAGCompareAnswers.log C303/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C304/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C304/output.txt -resultfile=C304/rateresults.txt
mv RAGCompareAnswers.log C304/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C305/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C305/output.txt -resultfile=C305/rateresults.txt
mv RAGCompareAnswers.log C305/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C306/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C306/output.txt -resultfile=C306/rateresults.txt
mv RAGCompareAnswers.log C306/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C307/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C307/output.txt -resultfile=C307/rateresults.txt
mv RAGCompareAnswers.log C307/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C308/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C308/output.txt -resultfile=C308/rateresults.txt
mv RAGCompareAnswers.log C308/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C309/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C309/output.txt -resultfile=C309/rateresults.txt
mv RAGCompareAnswers.log C309/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C310/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C310/output.txt -resultfile=C310/rateresults.txt
mv RAGCompareAnswers.log C310/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C311/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C311/output.txt -resultfile=C311/rateresults.txt
mv RAGCompareAnswers.log C311/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C312/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C312/output.txt -resultfile=C312/rateresults.txt
mv RAGCompareAnswers.log C312/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C313/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C313/output.txt -resultfile=C313/rateresults.txt
mv RAGCompareAnswers.log C313/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C314/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C314/output.txt -resultfile=C314/rateresults.txt
mv RAGCompareAnswers.log C314/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C315/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C315/output.txt -resultfile=C315/rateresults.txt
mv RAGCompareAnswers.log C315/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C316/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C316/output.txt -resultfile=C316/rateresults.txt
mv RAGCompareAnswers.log C316/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C317/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C317/output.txt -resultfile=C317/rateresults.txt
mv RAGCompareAnswers.log C317/RAGCompareAnswers.log


python3 ../code/RAGCompileResults.py > out.txt

