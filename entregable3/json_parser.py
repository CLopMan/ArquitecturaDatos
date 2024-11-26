import re

count_keys = 0

with open("sample.json", "r", encoding="ISO-8859-1") as f:
    file_content = f.read()
    file_parsed = re.sub(r"(?<!}\s)\n(?!\s{)", "", file_content)

with open("sample_parsed.json", "w", encoding="ISO-8859-1") as f:
    f.write(file_parsed)
    
