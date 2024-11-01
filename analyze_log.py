import pandas as pd
import datetime as dt

log_read = []
log_output = []
output_list = []

# Read file into list
with open('app_log.txt') as file:
    while line := file.readline():
        log_line = line.split(sep=" ", maxsplit=3)
        if log_line[-1].endswith('\n'):
            log_line[-1] = log_line[-1][:-1]
        log_read.append([log_line[2], dt.date.fromisoformat(log_line[0]),
                         dt.time.fromisoformat(log_line[1]), log_line[3]])

# Sort and add headers
log_read = sorted(log_read, key=lambda x: [x[0], x[1], x[2]])
log_df = pd.DataFrame(log_read, columns=['Category', 'Date', 'Time', 'Message'])

# Dropping searchable dates and times again
log_df['Date'] = log_df['Date'].astype(str)
log_df['Time'] = log_df['Time'].astype(str)

# Attempt at user input...
cat_input = input('Which data do you want to write?\n1. Errors\n2. Warnings\n3. Info\n4. Success\n')
if '1' in cat_input:
    output_list.append('ERROR')
if '2' in cat_input:
    output_list.append('WARNING')
if '3' in cat_input:
    output_list.append('INFO')
if '4' in cat_input:
    output_list.append('SUCCESS')

# Writing categories in output_list to file
for cat in output_list:
    log_output = log_df.loc[log_df['Category'].isin([cat])]
    log_output = log_output.values.tolist()
    with open(cat.lower() + '_log.txt', 'w') as file:
        for line in log_output:
            file.write(' '.join(line[1:4]) + '\n')
    file.close()
