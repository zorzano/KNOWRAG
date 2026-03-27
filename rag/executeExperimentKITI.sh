#!/bin/bash

 ../data/loadbase.sh
# Lineas con el C000test para pruebas
#python3 ../code/RAGAskQuestions.py -filename=C000test/config.txt
#python3 ../code/RAGRateAnswers.py -filename1=C000test/output.txt -resultfile=C000test/rateresults.txt
#python3 ../code/RAGRateAnswers.py -filename1=C000test/output.txt -filename2=C000test/output.txt -resultfile=C000C000.txt

python3 ../code/RAGAskQuestions.py -filename=C001/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C001/output.txt -resultfile=C001/rateresults.txt
mv RAGCompareAnswers.log C001/RAGCompareAnswers.log


python3 ../code/RAGAskQuestions.py -filename=C002/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C002/output.txt -resultfile=C002/rateresults.txt
mv RAGCompareAnswers.log C002/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C003/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C003/output.txt -resultfile=C003/rateresults.txt
mv RAGCompareAnswers.log C003/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C004/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C004/output.txt -resultfile=C004/rateresults.txt
mv RAGCompareAnswers.log C004/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C005/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C005/output.txt -resultfile=C005/rateresults.txt
mv RAGCompareAnswers.log C005/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C006/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C006/output.txt -resultfile=C006/rateresults.txt
mv RAGCompareAnswers.log C006/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C007/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C007/output.txt -resultfile=C007/rateresults.txt
mv RAGCompareAnswers.log C007/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C008/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C008/output.txt -resultfile=C008/rateresults.txt
mv RAGCompareAnswers.log C008/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C009/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C009/output.txt -resultfile=C009/rateresults.txt
mv RAGCompareAnswers.log C009/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C010/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C010/output.txt -resultfile=C010/rateresults.txt
mv RAGCompareAnswers.log C010/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C011/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C011/output.txt -resultfile=C011/rateresults.txt
mv RAGCompareAnswers.log C011/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C012/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C012/output.txt -resultfile=C012/rateresults.txt
mv RAGCompareAnswers.log C012/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C013/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C013/output.txt -resultfile=C013/rateresults.txt
mv RAGCompareAnswers.log C013/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C014/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C014/output.txt -resultfile=C014/rateresults.txt
mv RAGCompareAnswers.log C014/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C015/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C015/output.txt -resultfile=C015/rateresults.txt
mv RAGCompareAnswers.log C015/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C016/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C016/output.txt -resultfile=C015/rateresults.txt
mv RAGCompareAnswers.log C016/RAGCompareAnswers.log

python3 ../code/RAGAskQuestions.py -filename=C017/config.txt
python3 ../code/RAGRateAnswers.py -filename1=C017/output.txt -resultfile=C015/rateresults.txt
mv RAGCompareAnswers.log C017/RAGCompareAnswers.log

python3 ../code/RAGCompileResults.py > out.txt

