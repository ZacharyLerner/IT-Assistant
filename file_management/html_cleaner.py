import re
from bs4 import BeautifulSoup

# cleans and formats the text
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean(input_file_path, output_file_path, mode):
    # Loads the HTML file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # extract the sections based on headers 
    sections = soup.find_all([ 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])

    # dictionary to hold the structured content
    structured_content = {}
    current_section = None

    # loop through the sections and structure the content
    for section in sections:
        if section.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            current_section = clean_text(section.get_text())
            structured_content[current_section] = []
        elif section.name == 'p' and current_section:
            structured_content[current_section].append(clean_text(section.get_text()))

    # output the structured content to a text file
    with open(output_file_path, mode, encoding='utf-8') as outfile:
        for section, texts in structured_content.items():
            outfile.write(f"#{section}\n")
            for text in texts:
                outfile.write(f"{text}\n")
            outfile.write("\n")


