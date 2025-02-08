import os
import re
from difflib import SequenceMatcher


def normalize_header(text):
    """Normalize header text for comparison"""
    # Convert to lowercase and remove special chars
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Remove extra whitespace
    return ' '.join(text.split())


def headers_are_similar(header1, header2, threshold=0.85):
    """Check if headers are similar using fuzzy matching"""
    return SequenceMatcher(None, header1, header2).ratio() >= threshold


def remove_duplicate_headers_in_folder(folder_path, similarity_threshold=0.85):
    """
    Removes duplicate headers from all Markdown files in a folder and its subfolders.

    Parameters:
        folder_path (str): Path to the folder containing Markdown files.
    """
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    input_file = os.path.join(root, file)

                    with open(input_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    seen_headers = []
                    cleaned_lines = []

                    header_pattern = re.compile(r'^(#{1,6})\s*(.+)$')  # Matches Markdown headers

                    for line in lines:
                        match = header_pattern.match(line)
                        if match:
                            header_content = match.group(2).strip()
                            normalized = normalize_header(header_content)

                            # Check if similar to any seen header
                            is_duplicate = any(
                                headers_are_similar(normalized, seen, similarity_threshold)
                                for seen in seen_headers
                            )

                            if is_duplicate:
                                continue  # Skip similar header
                            seen_headers.append(normalized)
                        cleaned_lines.append(line)

                    with open(input_file, 'w', encoding='utf-8') as f:
                        f.writelines(cleaned_lines)

        print(f"Duplicate headers removed and files updated in {folder_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
folder_path = input("Enter the path to the folder containing Markdown files: ").strip()
threshold = float(input("Enter similarity threshold (0.0 to 1.0, default 0.85): ") or "0.85")
remove_duplicate_headers_in_folder(folder_path, threshold)
