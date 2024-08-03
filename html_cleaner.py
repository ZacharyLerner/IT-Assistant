import json
from bs4 import BeautifulSoup

# Parses the HMTL file and extracts all paragraphs for information 
def parse_html(html_file):
    # Reads the file using Beautiful Soup 
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Selects only the paragraphs from the file
        paragraphs = [p.get_text(separator=' ') for p in soup.find_all('p')]
        return paragraphs

# Creates a jason from the extracted paragraphs
def create_json(content, output_json):
    content_dict = {"content": content}
    
    # Save the JSON file
    with open(output_json, 'w', encoding='utf-8') as file:
        json.dump(content_dict, file, indent=4, ensure_ascii=False)

# File paths
html_file_path = 'website_files/URI ITSD Internal - Brightspace.html'
output_json_path = 'output_files/test.json'

# Parse HTML and extract content
html_content = parse_html(html_file_path)

# Create JSON file from extracted content
create_json(html_content, output_json_path)

print(f"Recreated JSON file saved at {output_json_path}")




