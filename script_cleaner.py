## This script is used for the southpark script_text from my wiki crawler
## It will then pre-process my data for the RNN

import re

## Change data from CARTMAN \n screw you guys
## To cartman: screw you guys


# Match the characters and the newline after each
new_lines_after_chars = '(\n\n\W[A-Z].+)(\n)'
with open('script_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Sub out CARTMAN\n with CARTMAN:
new_text = re.sub(new_lines_after_chars, r'\2\1:', text)
script_lines = new_text.split("\n")

# Remove any lines from our text we didn't process
filtered_script = ''
for line in script_lines:
    if '::' in line:
        line = line.replace('::',':')
    if ':' in line:
        filtered_script += line[1:]+"\n"




# Save clean data
clean_data = open('clean_data.txt','w',encoding='utf-8')
clean_data.write(filtered_script)
clean_data.close()

# Convert from UTF8 to ascii (data loss expected)
# Save clean data in ascii
ascii_data = filtered_script.encode("ascii","ignore")
clean_data = open('clean_data_ASCII.txt','w')
clean_data.write(ascii_data.decode("ascii"))
clean_data.close()
