import os
from html_cleaner import clean
from text_cleaner import write_json

html_output = "file_management/cleaned_html.txt"
json_output = "file_management/data.json"

# assign directory
directory = 'file_management/html_files'

# ensure the output text file is empty before processing
open(html_output, 'w').close()

# iterate over files in that directory
for index, filename in enumerate(os.scandir(directory)):
    if filename.is_file():
        print("File processed:", filename.path)
        mode = 'w' if index == 0 else 'a'  # use write mode for the first file, append mode for the rest
        clean(filename.path, html_output, mode)

write_json(html_output, json_output)
print("File written to JSON")
