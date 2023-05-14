from pass_1 import formats

def pass1extractor(df):

    loc_counter = []
    dataColumns = list(df.columns.values)
    start = str(dataColumns[2]).upper()

    # print(start)
    loc_counter.append(start)
    for i in range(0, len(df)):
        instruction = str(df.iloc[i, 1]).upper().strip()
        if instruction in formats.Format1.keys():
            # print(loc_counter)
            next = hex(int(loc_counter[-1], 16) + 1).upper()
            loc_counter.append(next[2:].zfill(4))
        elif instruction in formats.Format3.keys():
            # print(loc_counter)
            next = hex(int(loc_counter[-1], 16) + 3).upper()
            loc_counter.append(next[2:].zfill(4))
        elif instruction == 'RESW':
            variables = int(df.iloc[i, 2])
            # print(loc_counter)
            next = hex(int(loc_counter[-1], 16) + (variables * 3)).upper()
            loc_counter.append(next[2:].zfill(4))
        elif instruction == "RESB":
            variables = int(df.iloc[i, 2])
            # print(loc_counter)
            next = hex(int(loc_counter[-1], 16) + variables).upper()
            loc_counter.append(next[2:].zfill(4))
        elif instruction == 'WORD':
            # print(loc_counter)
            next = hex(int(loc_counter[-1], 16) + 3)
            loc_counter.append(next[2:].zfill(4))
        elif instruction == 'BYTE':
            characters = str(df.iloc[i, 2])

            if characters[0].upper() == 'C':

                # print(loc_counter)
                next = hex(int(loc_counter[-1], 16) + (len(characters) - 3)).upper()
                loc_counter.append(next[2:].zfill(4))
            elif characters[0].upper() == 'X':
                # print(loc_counter)
                next = hex((int(loc_counter[-1], 16)) + (int((len(characters) - 3) / 2))).upper()
                loc_counter.append(next[2:].zfill(4))
            else:

                raise Exception('please enter a vaild chacarcter " C or X" ')
        elif instruction == 'END':
            continue
        else:
            raise Exception('Please enter a valid instruction, or please check the spelling of your inputs')

    df.insert(0, 'location counter', loc_counter)
    # print(df)
    return df


