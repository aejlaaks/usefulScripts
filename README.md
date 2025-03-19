# Useful Scripts

A collection of Python scripts for various text processing, file management, and Markdown-related tasks.

## Script Overview

### File & Directory Management

- **add_sequence_number.py** - Organizes directories by renaming with sequential numbers based on creation date
- **AddFileExtensionPDF.py** - Adds .pdf extension to files without extensions
- **CheckCharacterLengthFilesFolders.py** - Shortens file/directory names to prevent path length issues
- **removeExtraCharactersFilesFolders.py** - Sanitizes file/directory names by removing special characters
- **removeIfKorjattu.py** - Removes files/directories containing 'korjattu' in their names
- **removeNonHtmlFiles.py** - Removes non-HTML files and duplicate HTML files
- **renameFolderFiles.py** - Renames directories to match the name of the first file they contain
- **removeWantedText.py** - Removes specified text patterns and numeric patterns from file/directory names

### Markdown & Content Processing

- **changeCharachtersInMD.py** - Replaces LaTeX-style escaped brackets with $$ in Markdown files
- **fixMermaid.py** - Fixes common syntax errors in Mermaid diagrams without using AI
- **fixMermaidWithDeepSeek.py** - Uses DeepSeek API to fix Mermaid syntax errors
- **FixMermaidWithOpenAi.py** - Uses OpenAI API to fix Mermaid syntax errors
- **FixMermaidAzureAi.py** - Uses Azure OpenAI to fix Mermaid syntax errors
- **removeDupilcateMermaidTags.py** - Removes duplicate code fence markers in Markdown files
- **removeDuplicateHeaders.py** - Removes duplicate headers from Markdown files
- **removeSameSentencesByThreshold.py** - Removes duplicate sentences from Markdown files
- **replateDOT.py** - Replaces ```dot with ```graphviz in Markdown files

### Content Generation & Conversion

- **DPAssignmentGeneratori.py** - Generates educational tasks using DeepSeek API
- **DPAssignmentGeneratoriLOGO.py** - Enhanced version with rate limiting and error handling
- **mergCSV.py** - Combines multiple CSV files into a single file

### JavaScript Tools

- **generate-pdf.js** - Converts HTML files to PDF using Puppeteer

## Usage

Each script has detailed usage instructions at the top of the file. To run a script:

```bash
python script_name.py
```

Most scripts will prompt for input parameters such as directories to process.

## Requirements

- Python 3.6+
- Various Python packages depending on the script:
  - openai
  - pandas
  - markdown/markdown2
  - beautifulsoup4
  - python-docx
  - pdfkit
  - httpx
  
For the JavaScript tool:
- Node.js
- Puppeteer

## Note on API Usage

Some scripts use external APIs (OpenAI, DeepSeek, Azure OpenAI). You'll need to:
1. Register for the relevant API services
2. Get your API keys
3. Update the scripts with your own API keys 