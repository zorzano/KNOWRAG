#/bin/sh

#rm finetune.txt
# Destruction line
python3 ../code/KGIoTLoader.py -k dictionary.txt

nohup python3 ../code/KGIRNLoader.py IRN/WC2014.ammend.1.txt  >salida.log 2>&1 &

