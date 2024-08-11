import os
from file_cleaner import clean_and_format_file
from text_cleaner import write_json

# files chosen to manage the file cleaning and json writing, can be changed 
file_output = "file_management/cleaned_html.txt"
json_output = "file_management/data2.json"

# Runs and write all files to a json file, great for updating but can have inaccuracies 
def update_files(directory):
    # assign directory
    # ensure the output text file is empty before processing
    open(file_output, 'w').close()

    # iterate over files in that directory
    for index, filename in enumerate(os.scandir(directory)):
        if filename.is_file():
            print("File processed:", filename.path)
            mode = 'w' if index == 0 else 'a'  # use write mode for the first file, append mode for the rest
            clean_and_format_file(filename.path, file_output, mode)

    write_json(file_output, json_output)
    print("File written to JSON")

# run a file directory to create a full json of those files, this can be manually view and edited to help assist search
write_json(file_output, json_output)
