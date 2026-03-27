import os

# Ruta del directorio raíz donde están los subdirectorios
root_dir = '.'

# Lista para almacenar las líneas de salida
output_lines = []

# Recorrer todos los subdirectorios en el directorio raíz
for subdir in sorted(os.listdir(root_dir)):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        result_path = os.path.join(subdir_path, 'result.txt')
        rateresults_path = os.path.join(subdir_path, 'rateresults.txt')

        if not os.path.exists(rateresults_path):
           continue
        # Inicializar variables para almacenar los datos extraídos
        total_questions = embedding_tokens = completion_tokens = seconds = None
        rates = [0] * 6  # Para los valores de 0 a 5

        # Leer el archivo result.txt
        with open(result_path, 'r') as file:
            for line in file:
                if 'Total questions:' in line:
                    total_questions = int(line.split(':')[1].strip())
                elif 'Embedding Tokens:' in line:
                    embedding_tokens = int(line.split(':')[1].strip())
                elif 'Completion Tokens:' in line:
                    completion_tokens = int(line.split(':')[1].strip())
                elif 'Seconds:' in line:
                    seconds = float(line.split(':')[1].strip())

        # Leer el archivo rateresults.txt
        with open(rateresults_path, 'r') as file:
            for line in file:
                if line[0].isdigit():
                    parts = line.split(':')
                    if len(parts) == 2:
                        rate = int(parts[0].strip())
                        count = int(parts[1].strip())
                        if 0 <= rate <= 5:
                            rates[rate] = count

        # Crear la línea de salida
        output_line = f"{subdir}\t{total_questions}\t{embedding_tokens}\t{completion_tokens}\t{seconds}"
        output_line += '\t' + '\t'.join(map(str, rates))

        # Añadir la línea a la lista de salida
        output_lines.append(output_line)

# Imprimir o guardar el resultado final
for line in output_lines:
    print(line)
