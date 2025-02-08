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
