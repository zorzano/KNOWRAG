#!/usr/bin/env python3

import sys
import re
from scipy.stats import friedmanchisquare


def parse_line(line):
    """
    Ejemplo:
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

    if len(data) < 3:
        print("ERROR: Friedman requiere al menos 3 configuraciones.")
        sys.exit(1)

    lengths = {len(scores) for _, scores in data}

    if len(lengths) != 1:
        print("ERROR: todas las configuraciones deben tener el mismo número de preguntas.")
        for name, scores in data:
            print(f"{name}: {len(scores)}")
        sys.exit(1)

    print("Configuraciones analizadas:")
    for name, scores in data:
        mean = sum(scores) / len(scores)
        print(f"  {name}: media={mean:.4f}")

    print()

    score_lists = [scores for _, scores in data]

    statistic, p_value = friedmanchisquare(*score_lists)

    print("=== Friedman Test ===")
    print(f"Statistic = {statistic:.6f}")
    print(f"p-value   = {p_value:.6g}")
    print()

    if p_value < 0.05:
        print("Resultado: existen diferencias estadísticamente significativas entre las configuraciones.")
    else:
        print("Resultado: no se han detectado diferencias estadísticamente significativas.")


if __name__ == "__main__":
    main()
