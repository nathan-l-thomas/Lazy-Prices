import pandas as pd
import datetime
import os


# import html.parser
import os
import re


FOLDER_TO_PARSE = r'C:\Users\Nate\Documents\Code\School\Lazy Prices\RawDocuments'
CSV_OUTPUT_FOLDER = r'C:\Users\Nate\Documents\Code\School\Lazy Prices\Dataset'


table_dictionary = {
    'CIK': [],
    'FilingDate': [],
    'Form': [],
    'Word Count': [],
    'Folder': [],
    'Parent Folder': [],
}

for root, dirs, files in os.walk(FOLDER_TO_PARSE):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f'Currently parsing and cleaning <{file}>...')

                # Read the content of the file
                file_content = f.read()

                delimited_filename = file.strip().split('_')

                # Ensure there are enough parts in the filename
                if len(delimited_filename) > 4:
                    filing_date = delimited_filename[0]
                    form_type = delimited_filename[1]
                    cid = delimited_filename[4]

                    folder_name = os.path.basename(root)
                    parent_folder = os.path.basename(os.path.dirname(root))

                    # Append values to the dictionary
                    table_dictionary['CIK'].append(cid)
                    table_dictionary['FilingDate'].append(
                        filing_date)
                    table_dictionary['Form'].append(form_type)
                    table_dictionary['Word Count'].append(
                        len(file_content))
                    table_dictionary['Folder'].append(folder_name)
                    table_dictionary['Parent Folder'].append(
                        parent_folder)
                else:
                    print(f"Filename '{file}' does not have enough parts.")


final_df = pd.DataFrame(table_dictionary)


output_filename = 'MainDataset.csv'
output_path = CSV_OUTPUT_FOLDER
path_out = os.path.join(output_path, output_filename)
print(path_out)


final_df.to_csv()
final_df = pd.DataFrame(table_dictionary)

output_filename = 'MainDataset.csv'
output_path = CSV_OUTPUT_FOLDER
path_out = os.path.join(output_path, output_filename)

print(path_out)


final_df.to_csv(path_out, index=False)  # Use path_out for the correct path
