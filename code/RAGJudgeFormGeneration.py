#!/usr/bin/env python3

import argparse
import sys


MARCAS = {"<Q>", "<R>", "<P>", "<A>"}


def limpiar(texto: str) -> str:
    return texto.strip()


def parsear_registros(contenido: str):
    registros = []
    actual = None
    campo = None

    for linea in contenido.splitlines():
        linea_limpia = linea.strip()

        if linea_limpia in MARCAS:
            if linea_limpia == "<Q>":
                if actual is not None:
                    registros.append(actual)

                actual = {
                    "pregunta": [],
                    "referencia": [],
                    "prompt": [],
                    "respuesta": [],
                }
                campo = "pregunta"

            elif actual is not None:
                if linea_limpia == "<R>":
                    campo = "referencia"
                elif linea_limpia == "<P>":
                    campo = "prompt"
                elif linea_limpia == "<A>":
                    campo = "respuesta"

            continue

        if actual is not None and campo is not None:
            actual[campo].append(linea)

    if actual is not None:
        registros.append(actual)

    return registros


def main():
    parser = argparse.ArgumentParser(
        description="Convierte registros <Q><R><P><A> a formato de salida."
    )
    parser.add_argument("id", help="Identificador que se usará en PREGUNTA [id]-[contador]")
    parser.add_argument("fichero", help="Fichero de texto de entrada")

    args = parser.parse_args()

    try:
        with open(args.fichero, "r", encoding="utf-8") as f:
            contenido = f.read()
    except OSError as e:
        print(f"Error abriendo el fichero: {e}", file=sys.stderr)
        sys.exit(1)

    registros = parsear_registros(contenido)

    for contador, reg in enumerate(registros, start=1):
        pregunta = limpiar("\n".join(reg["pregunta"])).replace('"', '')
        referencia = limpiar("\n".join(reg["referencia"])).replace('"', '')
        respuesta = limpiar("\n".join(reg["respuesta"])).replace('"', '')
       
        # Discard too long questions
        if (len(pregunta)+len(referencia)+len(respuesta) < 1500 ) and (len(referencia)<150):
            print(
                f'"PREGUNTA: {pregunta}\n'
                f'REFERENCIA: {referencia}\n'
                #f'RESPUESTA: {respuesta}" | OPCION_MULTIPLE | "Incorrecto. La respuesta no incluye ninguna información de la REFERENCIA.,La respuesta admite que no puede proporcionar una respuesta o carece de contexto; es honesta.,La respuesta tiene parte de la información de la REFERENCIA.,La respuesta es aceptable; contiene la información de la REFERENCIA pero no es exhaustiva.,La respuesta contiene toda la información de la REFERENCIA. Es fácil de leer."'
                # Problema P6J
                f'RESPUESTA: {respuesta}" | OPCION_MULTIPLE | "Incorrecto. La respuesta no incluye ninguna información de la REFERENCIA. [{args.id}-{contador}-1],La respuesta admite que no puede proporcionar una respuesta o carece de contexto; es honesta. [{args.id}-{contador}-2],La respuesta tiene parte de la respuesta correcta según la REFERENCIA. [{args.id}-{contador}-3],La respuesta es aceptable; contiene la información de la REFERENCIA pero no es exhaustiva. [{args.id}-{contador}-4],La respuesta es correcta de acuerdo a la REFERENCIA. Es fácil de leer. [{args.id}-{contador}-5],No puedo responder o no entiendo. [{args.id}-{contador}-0]"'                
            )


if __name__ == "__main__":
    main()

