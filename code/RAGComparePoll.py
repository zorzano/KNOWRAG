#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


RESULTS_PATTERN = re.compile(
    r"^\s*(\d+)\s+Grade:\s*([0-5])\s+Question:",
    re.IGNORECASE
)

SURVEY_PATTERN = re.compile(
    r"\[(C\d{3})-(\d{1,3})-([0-5])\]"
)


def load_rateresults(base_dir: Path):
    """
    Devuelve un diccionario:
        (directorio, numero_pregunta) -> grado
    Ejemplo:
        ("C001", 3) -> 2
    """

    grades = {}

    for subdir in sorted(base_dir.iterdir()):
        if not subdir.is_dir():
            continue

        if not re.fullmatch(r"C\d{3}", subdir.name):
            continue

        result_file = subdir / "rateresults.txt"

        if not result_file.exists():
            continue

        with result_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Las primeras 12 líneas se ignoran
        for line in lines[1:]:
            match = RESULTS_PATTERN.search(line)
            if not match:
                continue

            question_number = int(match.group(1))
            grade = int(match.group(2))

            grades[(subdir.name, question_number)] = grade

    return grades


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("survey_file", help="Fichero de texto con la encuesta")
    args = parser.parse_args()

    base_dir = Path(".")
    survey_path = Path(args.survey_file)

    grades = load_rateresults(base_dir)

    with survey_path.open("r", encoding="utf-8", errors="ignore") as f:
        survey_text = f.read()

    ntotal=0
    ncorrectas=0
    MAE=0

    pxct=0
    pxnull=0
    px0=0
    px1=0
    px2=0
    px3p=0

    for match in SURVEY_PATTERN.finditer(survey_text):
        cxxx = match.group(1)
        question_number = int(match.group(2))
        survey_grade = int(match.group(3))
        
        real_grade = grades.get((cxxx, question_number), "NOT_FOUND")

        if survey_grade != 0:
          ntotal+=1
          if survey_grade == real_grade:
                ncorrectas+=1
          MAE+=abs(survey_grade-real_grade)

        pxct+=1
        delta=abs(survey_grade - real_grade)

        if survey_grade==0:
            pxnull+=1
        elif delta==0:
            px0+=1
        elif delta==1:
            px1+=1
        elif delta==2:
            px2+=1
        elif delta>=3:
            px3p+=1

        if pxct==10:
            print(f"{pxnull},{px0},{px1},{px2},{px3p}")
            pxct=0
            pxnull=0
            px0=0
            px1=0
            px2=0
            px3p=0

    print(ncorrectas, ntotal)      
    print("Correct ratio: ",  float(ncorrectas)/float(ntotal))
    print("MAE: ", (float(MAE)/4.0)/float(ntotal))

if __name__ == "__main__":
    main()
