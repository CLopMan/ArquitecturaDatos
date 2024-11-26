import re

count_keys = 0

with open("sample.json", "r", encoding="ISO-8859-1") as f:
    file_content = f.read()
    file_parsed = re.sub(r"(?<!}\s)\n(?!\s{)", "", file_content)
    file_parsed = re.sub(r" +", " ", file_parsed)
    file_parsed = "[" + file_parsed + "]"
    file_parsed = re.sub(r"\n(?!\s])", ",\n", file_parsed)

with open("sample_parsed.json", "w", encoding="ISO-8859-1") as f:
    f.write(file_parsed)
    
