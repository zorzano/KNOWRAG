#!/usr/bin/env python3

import sys
import re
from scipy.stats import wilcoxon


def parse_line(line):
    """
    Ejemplo de línea:
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

    input_file = sys.argv[1]

    data = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                config, scores = parse_line(line)
                data.append((config, scores))

    if len(data) < 2:
        print("ERROR: hacen falta al menos dos configuraciones.")
        sys.exit(1)

    baseline_name, baseline_scores = data[0]

    print(f"Baseline: {baseline_name}")
    print()

    for config_name, scores in data[1:]:
        if len(scores) != len(baseline_scores):
            print(f"{baseline_name} vs {config_name}: ERROR - longitudes distintas")
            print(f"  {baseline_name}: {len(baseline_scores)}")
            print(f"  {config_name}: {len(scores)}")
            continue

        statistic, p_value = wilcoxon(
            baseline_scores,
            scores,
            alternative="two-sided",
            zero_method="wilcox"
        )

        mean_baseline = sum(baseline_scores) / len(baseline_scores)
        mean_config = sum(scores) / len(scores)

        print(f"{baseline_name} vs {config_name}")
        print(f"  mean {baseline_name}: {mean_baseline:.4f}")
        print(f"  mean {config_name}: {mean_config:.4f}")
        print(f"  diff: {mean_config - mean_baseline:.4f}")
        print(f"  Wilcoxon statistic: {statistic}")
        print(f"  p-value: {p_value:.6g}")
        print()


if __name__ == "__main__":
    main()
