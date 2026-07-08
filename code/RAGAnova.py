#!/usr/bin/env python3

import sys
import re
import pandas as pd
from statsmodels.stats.anova import AnovaRM


def parse_line(line):
    """
    Formato esperado:
    C001/rateresults.txt: 112111...
    """
    match = re.match(r"(C\d+)/rateresults\.txt:\s*([1-5]+)", line.strip())

    if not match:
        raise ValueError(f"Línea no válida: {line}")

    config = match.group(1)
    scores = [int(ch) for ch in match.group(2)]

    return config, scores


def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} fichero_resultados.txt")
        sys.exit(1)

    data = []

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(parse_line(line))

    if len(data) < 2:
        print("ERROR: hacen falta al menos dos configuraciones.")
        sys.exit(1)

    lengths = {len(scores) for _, scores in data}
    if len(lengths) != 1:
        print("ERROR: todas las configuraciones deben tener el mismo número de puntuaciones.")
        for config, scores in data:
            print(f"{config}: {len(scores)}")
        sys.exit(1)

    n_questions = lengths.pop()

    rows = []

    for config, scores in data:
        for question_id, score in enumerate(scores, start=1):
            rows.append({
                "question": question_id,
                "config": config,
                "score": score
            })

    df = pd.DataFrame(rows)

    print("Configuraciones:")
    for config, scores in data:
        mean = sum(scores) / len(scores)
        print(f"  {config}: mean={mean:.4f}")

    print()
    print("=== Repeated Measures ANOVA ===")

    anova = AnovaRM(
        data=df,
        depvar="score",
        subject="question",
        within=["config"]
    )

    result = anova.fit()
    print(result)


if __name__ == "__main__":
    main()
