import pandas as pd 
import utilities
from pandasgui import show
import re

## reading the file to get the memory start,length and end
def get_ext_symb_table():

    f =  open('sicxe2.txt','r') 
    ExtSymTab = {}

# First Pass SIC/XE

    LOC =input('Enter the starting address please\n').upper().strip() 
    oldLOC = LOC

    for line in f:

        if line[0] == "H":

            ExtSymTab[line[1:7].strip()] = [LOC.upper(), line[-6:-1]]
            LOC = utilities.add_hex(LOC, line[-7:-1]).zfill(6)

        elif line[0] == "D":
        
            subLine = line[1:-1]
            i = 0
        
        # 6 bytes name + 6 bytes location = 12
        # (subLine[12 * 0 : 12 * 0 + 6] = subLine[0:6]) = (subLine[12 * 0 + 6 : 12 * 0 + 12] = subLine[6:12])

            defenitions = re.findall('............',subLine)
            
            for defenition in defenitions:
                
            
                while i < int(len(subLine) / 12):
                    ExtSymTab[subLine[12 * i: 12 * i + 6].strip()] = [utilities.add_hex(subLine[12 * i + 6: 12 * i + 12] , oldLOC).zfill(6)]
                    i = i + 1

                oldLOC = LOC

    f.close()

    headers = ['control section', ' Symbol Name', 'Address','Length']
    df = pd.DataFrame(columns = headers)
    
    for key in ExtSymTab.keys():
        if len(ExtSymTab[key]) >1 :
            row = {'control section': key, ' Symbol Name':'', 'Address': ExtSymTab[key][0] ,'Length' : ExtSymTab[key][1]}
            df_temp = pd.DataFrame([row])
            df = pd.concat([df,df_temp], axis= 0 , ignore_index= True)
            
            
        else : 
            row = {'control section': '', ' Symbol Name': key, 'Address': ExtSymTab[key][0],'Length' :''}
            df_temp = pd.DataFrame([row])
            df = pd.concat([df,df_temp], axis= 0 , ignore_index= True)
            
    f = open('symbol_table.txt', 'w')
    df_String = df.to_string(header=True, index=False)
    f.write(df_String)
    f.close()
    
    return  ExtSymTab, LOC


# Second Pass SIC/XE
# making the addresses columns
def get_addressesXE(ExtSymTab,LOC):
    addresses = []
    start_int = list(ExtSymTab.values())[0][0]       #First Address indictionary
    start_int = int(start_int[:-1] + "0",16)

    end_int = int(LOC, 16)
    next_address = start_int

    while next_address < (end_int + 16):

        addresses.append(hex(next_address)[2:].zfill(6).upper())
        next_address = start_int + 16
        start_int = next_address
    
    return addresses

# #creating a dataframe for the memory graph
def initialize_dfxe(memory, ExtSymTab):
    df = pd.DataFrame()
    df = df.assign(**{'Addresses':memory,'0': 'X', '1': 'X', '2': 'X','3':'X','4':'X','5':'X','6':'X','7':'X','8':'X','9':'X','A':'X','B':'X','C':'X','D':'X','E':'X','F':'X'})
    df = df.set_index('Addresses')

    f =  open('sicxe2.txt','r') 

    progStart = ""
    
    for line in f:

        if line[0] == "H":
            progStart = ExtSymTab[line[1:7].strip()][0]

        if line[0] == "T":
            startT = hex(int(line[1:7], 16) + int(progStart, 16))[2:].zfill(6).upper()
            col = startT[-1].upper()
            startT = startT[:-1] + '0'

            modified = line[9:]
            i = 0

            while i <  len(modified) - 1:

                df.at[startT, col] = (modified[i] + modified[i + 1])

                if int(col, 16) < 15:
                    col = hex(int(col, 16) + 1)[2:].upper()

                else:
                    col = "0"
                    startT = hex(int(startT, 16) + 16)[2:].upper().zfill(6)

                i = i + 2

        if line[0] == "M":

            startT = hex(int(line[1:7], 16) + int(progStart, 16))[2:].zfill(6).upper()
            col = startT[-1].upper()
            startT = startT[:-1] + '0'

            colCopy = col
            startTCopy = startT

            modified = df.loc[startT, col]
            i = 0

            while i < 2:
                if int(col, 16) < 15:
                    col = hex(int(col, 16) + 1)[2:].upper()
                    modified += df.loc[startT, col]

                else:
                    col = "0"
                    startT = hex(int(startT, 16) + 16)[2:].upper().zfill(6)
                    modified += df.loc[startT, col]

                i = i + 1

            if line[8] == "5":
                firstChar = modified[0]

                if line[9] == "+":
                    modified = hex(int(modified[1:], 16) + int(ExtSymTab[line[10:-1]][0], 16))[2:].zfill(5).upper()

                else:
                    modified = hex((int(modified[1:], 16) - int(ExtSymTab[line[10:-1]][0], 16)) & (2**24-1))[2:].zfill(5).upper()

                modified = firstChar + modified

            else:
                
                if line[9] == "+":

                    modified = hex(int(modified, 16) + int(ExtSymTab[line[10:-1]][0], 16))[2:].zfill(6).upper()
                    modified = modified[-6:]


                else:

                    modified = hex((int(modified, 16) - int(ExtSymTab[line[10:-1]][0], 16)) & (2**24-1))[2:].zfill(6).upper()
                    modified = modified[-6:]

            i = 0
            while i < 5:

                df.at[startTCopy, colCopy] = (modified[i] + modified[i + 1])

                if int(colCopy, 16) < 15:
                    colCopy = hex(int(colCopy, 16) + 1)[2:].upper()

                else:
                    colCopy = "0"
                    startTCopy = hex(int(startTCopy, 16) + 16)[2:].upper().zfill(6)

                i = i + 2
    
    return df
   
def get_limtisXE():

    [ExtSymTab , LOC] = get_ext_symb_table()
    memory = get_addressesXE(ExtSymTab , LOC)
    show(initialize_dfxe(memory, ExtSymTab))