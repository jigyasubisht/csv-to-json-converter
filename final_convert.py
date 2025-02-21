import pandas as pd
import json
import re

# Load the CSV file
csv_file_path = 'C:/Users/verve/Desktop/CSV_TO_JASON/Hicksville.csv'
df = pd.read_csv(csv_file_path)

# Drop the 'Unnamed: 0' column if it exists to clean up previous indices
if 'Unnamed: 0' in df.columns:
    df.drop('Unnamed: 0', axis=1, inplace=True)

# Add a new column with the desired index format ("" as the column name)
df.insert(0, '', range(len(df)))

# Convert the DataFrame to JSON format
json_data = df.to_json(orient='records', lines=False, indent=4)

# Adjust JSON formatting: ensure a space after the colon for all key-value pairs
json_data = re.sub(r'("\w*":)(?! \d)', r'\1 ', json_data)  # Adding a space after the colon if not followed by a space

# Save the JSON data to a file
json_file_path = 'C:/Users/verve/Desktop/CSV_TO_JASON/output.json'
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print("CSV has been successfully converted to JSON!")
