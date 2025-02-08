import os

def replace_brackets_in_file(file_path):
    """Replaces \[ \], \( and \) with $$ in a given file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            # Replace \[ and \], \( and \) with $$
            updated_lines.append(line.replace('\\[', '$$').replace('\\]', '$$'))

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(updated_lines))

        print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    """Walks through the directory and processes all markdown files."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                replace_brackets_in_file(file_path)

if __name__ == "__main__":
    directory = input("Enter the path to the directory: ").strip()

    if os.path.isdir(directory):
        process_directory(directory)
        print("All markdown files have been processed.")
    else:
        print("The provided path is not a valid directory.")
