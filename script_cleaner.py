## This script is used for the southpark script_text from my wiki crawler
## It will then pre-process my data for the RNN

import re
import operator

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
# Also count up the character
characters = {}
for line in script_lines:
    if '::' in line:
        line = line.replace('::',':')
    if ':' in line:
        filtered_script += line[1:]+"\n"
        character = line.split(":")[0]
        if character in characters: characters[character] = characters[character] + 1
        else: characters[character] = 0



# Now, we want to only grab the top 10 most common characters to help our data set
sorted_chars = sorted(characters.items(), key=operator.itemgetter(1))

# Top 10 characters in a list
popular_chars = sorted_chars[-10:]
top10 = []
for char in popular_chars:
    top10.append(char[0][1:])

# Split up the lines so far
# apply a second filter (If you are the most popular character)
filtered_lines = filtered_script.split("\n")
second_filter = ''
for line in filtered_lines:
    split = line.split(":")
    if split[0] == top10[9]:
        second_filter += split[1] +"\n"


# Apply a third filter, remove all the [emotes] from the data set
third_filter=re.sub(r'\[.+\]', r'', second_filter)
# print(third_filter)

# Now, remove all weird double newlines and start of sentence spaces
third_filter_lines = third_filter.split("\n")
fourth_filter = ''
for line in third_filter_lines:
    if len(line) > 3:
        line.replace("\n","")
        line  = line.strip()
        spaceCount = 0
        for char in line:
            if char == " ":
                spaceCount += 1
            else:
                break
        line = line[spaceCount:]
        fourth_filter += line + "\n"

# print(fourth_filter)
# Convert from UTF8 to ascii (data loss expected)
# Save clean data in ascii
ascii_data = fourth_filter.encode("ascii", "ignore")
clean_data = open('cartman_data.txt', 'w')
clean_data.write(ascii_data.decode("ascii"))
clean_data.close()

