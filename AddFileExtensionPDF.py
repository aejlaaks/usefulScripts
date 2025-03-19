"""
Usage: AddFileExtensionPDF.py
----------------------------
This script adds a .pdf extension to files that don't have any file extension.
It's useful for fixing files that are meant to be PDFs but are missing their extensions.

Features:
- Processes all files in a specified directory (non-recursive)
- Only adds extension to files without an existing extension
- Leaves files with existing extensions unchanged
- Reports each file that is renamed

To use:
1. Run the script: python AddFileExtensionPDF.py
2. When prompted, enter the path to the directory containing files to process
3. The script will add .pdf extension to files without extensions and report changes
"""

import os

def add_pdf_extension_to_files(directory):
    """
    Add .pdf extension to files in the specified directory if they lack an extension.

    Args:
        directory (str): Path to the directory to process.
    """
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # Ensure it's a file, not a directory
            if os.path.isfile(file_path):
                # Check if the file has no extension
                if not os.path.splitext(filename)[1]:
                    new_filename = f"{filename}.pdf"
                    new_file_path = os.path.join(directory, new_filename)

                    # Rename the file
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {filename} -> {new_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory: ").strip()
    if os.path.isdir(directory_path):
        add_pdf_extension_to_files(directory_path)
    else:
        print("The provided path is not a valid directory.")
