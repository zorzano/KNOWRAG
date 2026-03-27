#/bin/sh

rm finetune.txt
# Destruction line
python3 ../code/KGIoTLoader.py -k dictionary.txt

python3 ../code/KGIoTLoader.py DeviceManufacturers.v2.csv -d dictionary.txt -f z
python3 ../code/KGIoTLoader.py manufacturers.csv -d dictionary.txt -f s
python3 ../code/KGWikiLoader.py TTTWiki.3.txt
python3 ../code/KGCSVLoader.py kiticontent.csv

#python3 ../code/KGMINTQALoader.py MINTQA-POP.red.json

