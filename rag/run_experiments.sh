#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
    echo "Uso: $0 C001 C002 C004-C008 C301-C305"
    exit 1
fi

run_experiment() {
    local exp="$1"

    echo "========================================"
    echo "Ejecutando experimento $exp"
    echo "========================================"

    if [ ! -d "$exp" ]; then
        echo "ERROR: no existe el directorio $exp"
        exit 1
    fi

    if [ ! -f "$exp/config.txt" ]; then
        echo "ERROR: no existe $exp/config.txt"
        exit 1
    fi

    python3 ../code/RAGAskQuestions.py \
        -filename="$exp/config.txt"

    python3 ../code/RAGRateAnswers.py \
        -filename1="$exp/output.txt" \
        -resultfile="$exp/rateresults.txt"

    if [ -f "RAGCompareAnswers.log" ]; then
        mv RAGCompareAnswers.log "$exp/RAGCompareAnswers.log"
    else
        echo "AVISO: no se encontró RAGCompareAnswers.log para $exp"
    fi

    echo "Experimento $exp terminado"
}

expand_range() {
    local range="$1"
    local start="${range%-*}"
    local end="${range#*-}"

    if [[ ! "$start" =~ ^C[0-9]+$ || ! "$end" =~ ^C[0-9]+$ ]]; then
        echo "ERROR: rango no válido: $range"
        exit 1
    fi

    local prefix_start="${start:0:1}"
    local prefix_end="${end:0:1}"

    if [ "$prefix_start" != "$prefix_end" ]; then
        echo "ERROR: los rangos deben tener el mismo prefijo: $range"
        exit 1
    fi

    local start_num="${start:1}"
    local end_num="${end:1}"
    local width="${#start_num}"

    # Forzar base 10 para evitar problemas con ceros iniciales
    start_num=$((10#$start_num))
    end_num=$((10#$end_num))

    if [ "$start_num" -gt "$end_num" ]; then
        echo "ERROR: rango descendente no permitido: $range"
        exit 1
    fi

    for ((i=start_num; i<=end_num; i++)); do
        printf "C%0${width}d\n" "$i"
    done
}

for arg in "$@"; do
    if [[ "$arg" == *"-"* ]]; then
        while IFS= read -r exp; do
            run_experiment "$exp"
        done < <(expand_range "$arg")
    else
        if [[ ! "$arg" =~ ^C[0-9]+$ ]]; then
            echo "ERROR: experimento no válido: $arg"
            exit 1
        fi

        run_experiment "$arg"
    fi
done
