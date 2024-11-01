import pandas as pd


def handle_line(l):
    if l[-1].endswith('\n'):
        l[-1] = l[-1][:-1]
    if not all(l):
        return None
    if not l[0].isdigit():
        f_out.write(l[0] + ' is not a valid customer_id.\n')
    if not l[1].replace(' ', '').replace('.', '').isalpha():
        f_out.write(l[1] + ' is not a valid name.\n')
    if not '@' in l[2]:
        f_out.write(l[2] + ' is not a valid email.\n')
    try:
        if not l[3].replace('.', '').isnumeric():
            f_out.write(l[3] + ' is not a valid purchase_amount.\n')
        try:
            l[3] = (l[3] + '.' + l[4])
            l.pop(4)
        except IndexError:
            pass
    except IndexError:
        f_out.write('purchase_amount is empty, changed to 0.00.\n')
        l.append('0.00')
    return l


with open('source_data1.csv') as file:
    # Header handling
    header = file.readline()
    header = header.split(sep=',')
    if header[-1].endswith('\n'):
        header[-1] = header[-1][:-1]

    # Error output in dmt_output.txt
    data_list = []
    f_out = open('dmt_output.txt', 'w', encoding='utf-8')
    while line := file.readline():
        line_split = line.split(sep=',')
        line_h = handle_line(line_split)
        if line_h:
            data_list.extend([line_h])
    f_out.close()

# Output data using Pandas
df_out = pd.DataFrame(data_list, columns=header)
df_out.to_csv('dmt_data.csv', index=False, encoding='utf-8')

# def find_datatype(lp):
#     try:
#         dt.date.fromisoformat(lp)
#         return 'date'
#     except ValueError:
#         pass
#     try:
#         dt.time.fromisoformat(lp)
#         return 'time'
#     except ValueError:
#         pass
#     if '@' in lp:
#         return 'email'
#     if any([x in lp for x in ['yahoo.com'|'google.com'|'hotmail.com']]):
#         return 'no@email'
#     if lp.isdecimal():
#         return 'integer'
#     if lp.replace('.','').replace('-','').isdecimal():
#         return 'decimal'
#     if lp.replace(' ','').isupper():
#         return 'uppercase'
#     if lp.replace(' ','').islower():
#         return 'lowercase'
#     if all(lp.split().istitle()):
#         return 'name'
#     return 'string'

# def line_data_types(l):
#     l_split = l.split()
#     lt = []
#     for lp in l_split:
#         lt.append(find_datatype(lp))
