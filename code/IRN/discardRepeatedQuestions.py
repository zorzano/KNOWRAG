import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        return

    filename = sys.argv[1]
    seen = set()

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if not parts:
                    continue
                first_field = parts[0]
                if first_field not in seen:
                    print(line, end='')  # print line as is
                    seen.add(first_field)
    except FileNotFoundError:
        print(f"File not found: {filename}")

if __name__ == "__main__":
    main()
