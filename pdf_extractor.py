import pdfplumber
import pandas as pd
import re
import os

with pdfplumber.open('/Users/dylanpan/Desktop/PycharmProjects/pythonProject1/雅思基础词汇.pdf') as pdf:
    extracted_text = ""
    for page in pdf.pages:
        extracted_text += page.extract_text()

lines = extracted_text.split("\n")

data = []
regex = r"^(\d+)(\w+)\s+"

for line in lines:
    parts = line.split(" ",2)
    if len(parts) == 3:
        word = parts[0]
        chinese = parts[2]

        data.append((word,chinese))

df = pd.DataFrame(data,columns=['word','translation'])
df = df.iloc[2:]

df[['code', 'word']] = df['word'].str.extract(r'(\d+)(\D+)')
df = df[['code', 'word','translation']]
df = df.reset_index(drop=True)
df = df.dropna(subset=['code', 'word'])

print(df)

directory = '/Users/dylanpan/Desktop/PycharmProjects/pythonProject1'
file_path = os.path.join(directory, 'words_basic.csv')
if not os.path.exists(directory):
    os.makedirs(directory)

