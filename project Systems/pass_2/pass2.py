from pass_1 import formats


def dataframe_to_dict(df):
    dicti = {}
    for i in range(0, len(df) - 1):
        dicti[df.iloc[i, 1]] = df.iloc[i, 0]

    return dicti


def pass2Extractor(df):
    object_code = []
    mapp = dataframe_to_dict(df)
    for i in range(0, len(df)):
        instruction = df.iloc[i, 2].upper()
        if instruction in formats.Format1.keys():
            object_code.append(formats.Format1[instruction])
        # print(object_code)
        elif instruction == 'RSUB':
            object_code.append(formats.Format3[instruction] + '0000')
        # print(object_code)
        elif instruction == 'BYTE':
            characters = str(df.iloc[i, 3])

            if characters[0] == 'X':
                X_value = characters[2:-1]
                # print(X_value)
                object_code.append(X_value)
            # print(object_code)
            elif characters[0] == 'C':
                C_value = characters[2:-1]
                ascii_code = C_value.encode('utf-8').hex().upper()
                object_code.append(ascii_code)
                # print(ascii_code)
            else:
                raise Exception('invalid character in BYTE instruction')
        elif instruction == 'WORD':
            characters = int(df.iloc[i, 3])
            hexa = format(characters, '02x')
            hexa = hexa.zfill(6)
            # print(hex)
            object_code.append(hexa)
        elif instruction == 'RESW' or instruction == 'RESB':
            object_code.append(' ')

        elif instruction in formats.Format3.keys() and df.iloc[i, 3][0] == '#':

            immediate_code = formats.Format3[instruction]
            #  print("{0:08b}".format(int(immediate_code, 16)))
            # print(immediate_code)
            immediate_code = "{0:08b}".format(int(immediate_code, 16))[:7] + '1'
            # print( immediate_code)
            # print(address_hexa)
            address_hexa = hex(int(df.iloc[i, 3][1:]))[2:].upper()
            address = "{0:016b}".format(int(address_hexa, 16))
            ob_code = immediate_code + address
            # print(ob_code)
            ob_code = hex(int(ob_code, 2))[2:].upper()
            ob_code = ob_code.zfill(6)
            # print( ob_code)
            object_code.append(ob_code)

        elif instruction in formats.Format3.keys() and df.iloc[i, 3].find(',X') > -1:
            x_op_code = formats.Format3[instruction]
            x_op_code_binary = "{0:08b}".format(int(x_op_code, 16))
            # print(x_op_code)
            # print(x_op_code_binary)
            x_address = mapp[df.iloc[i, 3][:-2]]
            x_address_binary = "{0:016b}".format(int(x_address, 16))
            # print(x_address)
            # print(x_address_binary)
            x_address_binary_modified = '1' + x_address_binary[1:]
            # print(x_address_binary_modified)
            x_object_code = x_op_code_binary + x_address_binary_modified
            # print(x_object_code)
            x_object_code_hexa = hex(int(x_object_code, 2))[2:].upper()
            # print(x_object_code_hexa)
            object_code.append(x_object_code_hexa.zfill(6))

        elif instruction in formats.Format3.keys():
            op_code = formats.Format3[instruction]
            adress = mapp[df.iloc[i, 3]]
            # print(adress)
            format3_ob = op_code + adress
            object_code.append(format3_ob)
            # print(object_code)
        else:

            object_code.append(" ")
    df.insert(4,'Object Code',object_code)
    print(df)
    return df

# print(object_code)
# print(len(object_code))
# df.insert(4,'Object Code',object_code)
# df.to_csv('pass2_out.txt','\t', index=False )
# df.to_excel("Pass2.xlsx", encoding='utf-8', index=False)

# pass2Extractor('pass1_out.txt')
