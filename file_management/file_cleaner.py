import re
from bs4 import BeautifulSoup
from docx import Document
import os

# Cleans and formats the text
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# Function to read and format DOCX files
def read_docx_and_format(file_path):
    # Open the document
    doc = Document(file_path)
    
    # Initialize an empty list to hold the formatted content
    content = []

    # Read the content of each paragraph in the document
    for paragraph in doc.paragraphs:
        if paragraph.text:
            # Split paragraph text by question marks
            parts = paragraph.text.split('?')
            formatted_question = ' '.join(f'{part.strip()}?' for part in parts[:-1] if part.strip())
            if formatted_question:
                content.append(f'# {formatted_question}\n')
            last_part = parts[-1].strip()
            if last_part:
                content.append(f'{last_part}\n\n')

    # Join the content into a single string
    formatted_content = ''.join(content).strip()  # Remove any leading/trailing whitespace
    return formatted_content

# Function to clean and format HTML files
def clean_html(input_file_path):
    # Loads the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract the sections based on headers 
    sections = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])

    # Dictionary to hold the structured content
    structured_content = {}
    current_section = None

    # Loop through the sections and structure the content
    for section in sections:
        if section.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            current_section = clean_text(section.get_text())
            structured_content[current_section] = []
        elif section.name == 'p' and current_section:
            structured_content[current_section].append(clean_text(section.get_text()))

    # Build the formatted content
    content = []
    for section, texts in structured_content.items():
        content.append(f"#{section}\n")
        for text in texts:
            content.append(f"{text}\n")
        content.append("\n")
    
    return ''.join(content).strip()

# Main function to determine the file type and clean the file accordingly
def clean_and_format_file(input_file_path, output_file_path, mode):
    file_extension = os.path.splitext(input_file_path)[1].lower()

    if file_extension == '.docx':
        formatted_content = read_docx_and_format(input_file_path)
    elif file_extension == '.html' or file_extension == '.htm':
        formatted_content = clean_html(input_file_path)
    else:
        raise ValueError("Unsupported file format")

    # Output the formatted content to a text file
    with open(output_file_path, mode, encoding='utf-8') as outfile:
        outfile.write(formatted_content)

    outfile.close()




