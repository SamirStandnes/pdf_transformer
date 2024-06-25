import re
import pandas as pd
import pdfplumber

# Function to extract all text from the PDF
def extract_all_text(file_path):
    all_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            all_text.append(text)
    return all_text

# Function to filter rows starting with a date
def filter_date_rows(all_text):
    date_rows = []
    date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{2}')
    for page_text in all_text:
        lines = page_text.split('\n')
        for line in lines:
            if date_pattern.match(line):
                date_rows.append(line)
    return date_rows

# Improved parsing logic to handle descriptions with numerical values correctly
def parse_row_improved(row):
    parts = re.split(r'(\d{2}\.\d{2}\.\d{2})', row)
    if len(parts) >= 3:
        date = parts[1]
        rest = parts[2].strip().rsplit(' ', 4)
        if len(rest) == 5:
            description = ' '.join(rest[:-4])
            count = rest[-4]
            price = rest[-2]
            amount = rest[-1]
            return [date, description.strip(), count, price, amount]
    return None

# Path to your PDF file
file_path = "path_to_your_pdf_file.pdf"

# Extract all text from the PDF file
all_text = extract_all_text(file_path)

# Filter and parse rows starting with a date
parsed_data_improved = []
date_rows = filter_date_rows(all_text)
for row in date_rows:
    parsed_row = parse_row_improved(row)
    if parsed_row:
        parsed_data_improved.append(parsed_row)

# Create a dataframe
df_improved = pd.DataFrame(parsed_data_improved, columns=["Dato", "Beskrivelse", "Antall", "Pris", "Beløp"])

# Display the dataframe
print(df_improved.head())
