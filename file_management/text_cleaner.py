import json

# writes a formatted text file a json file
def write_json(input_file, output_file):
    file = open(input_file, "r", encoding='utf-8')

    separated_line = ""
    document_lines = []

    # writes each section to one line in the json file
    for line in file:
        if line.strip() == "":
            continue  # Skip empty lines
        # uses # to indicate new sections of text
        if line[0] == '#':
            if separated_line.strip():
                document_lines.append(separated_line.strip())  # add the current section to the list and strip any leading/trailing whitespace
            separated_line = ""
            line = line[1:]  # remove the first character when it is #
        separated_line += " " + line.strip()  # add a space between lines to avoid words being concatenated

    # append the last section if it exists
    if separated_line.strip():
        document_lines.append(separated_line.strip())

    file.close() 

    # write to a JSON file
    output = {'document': document_lines}
    with open(output_file, "w", encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4)
