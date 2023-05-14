import pandas as pd


def checkProgName(progName):
    if len(progName) == 6:
        return progName
    elif len(progName) > 6:

        raise Exception('Program Name Length exceeds the 6 bytes limit')
    else:

        for i in range(len(progName), 6):
            progName = progName + 'x'
        return progName


def getH(df):
    H = 'H.'
    dataColumns = list(df.columns.values)
    Name = str(dataColumns[1]).upper()
    correctName = checkProgName(Name).upper()
    H += correctName + '.'
    start = str(dataColumns[3]).upper().zfill(6)
    H += start + '.'
    end = df.iloc[len(df) - 1, 0]
    length = hex(int(end, 16) - int(start, 16))[2:].upper().zfill(6)
    H += length + '.'
    return H[0:-1]


# print(getH(df))

def getE(df):
    E = 'E.'
    start = df.iloc[0, 0].zfill(6)
    E += start + '.'
    return E[0:-1]


def getT(df):
    f = 0
    l = 0
    text = []
    temp = 'T'
    while l < len(df):
        inst = df.iloc[l, 2]
        # check if the pointer is in START program or not
        if f == 0:
            # str to convert locationCounter from string to hex
            string = df.iloc[f, 0].zfill(6)
            str = int(df.iloc[f, 0], 16)
        else:
            str = int(df.iloc[f, 0], 16)
            string = df.iloc[f, 0].zfill(6)
        end = int(df.iloc[l, 0], 16)
        length = hex(end - str)
        diff = int(length, 16) - int('1E', 16)

        if inst == 'END':
            temp = temp[:2] + string + temp[1:]
            length = hex(end - str)[2:].zfill(2)
            temp = temp[:8] + '.' + length.upper() + '.' + temp[9:]
            text.append(temp)
            break

        elif inst == 'RESW' or inst == 'RESB':
            temp = temp[:2] + string + temp[1:]
            length = hex(end - str)[2:].zfill(2)
            temp = temp[:8] + '.' + length.upper() + '.' + temp[9:]
            text.append(temp)
            f = l + 1
            l = f
            temp = 'T'
        # if the length between two pointers are equal or more than 1E
        elif diff >= 0:
            temp = temp[:2] + string + temp[1:]
            if diff > 0:
                end = int(df.iloc[l - 1, 0], 16)
                length = hex(end - str)
                temp = temp[0: len(temp) - 7]
                l -= 1

            length = length[2:].zfill(2)
            temp = temp[:8] + '.' + length.upper() + '.' + temp[9:]
            text.append(temp)
            f = l
            temp = 'T'

        # if length less than 1E
        else:
            temp += '.' + df.iloc[l, 4]
            l += 1

    text = [i for i in text if len(i) > 11]
    return text


# print(getT(df))
def getRecord(df):
    # for Header
    H = getH(df)
    T = ''
    for i in getT(df):
        T += i + '\n'
    E = getE(df)
    return H + '\n' + T + E
