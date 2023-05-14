import pandas as pd 
import utilities
from pandasgui import show

## reading the file to get the memory start,length and end
#get start and end of the memory
def GetLimits():
    f =  open('in_test_no_dots.txt','r') 
    header = f.readline() 
    start_address = header[7:-7]
    end_address = utilities.add_hex(start_address,header[-6:])
    real_end_address = end_address[:-1] + '0'
    f.close()
    get_addresses(start_address, real_end_address)
     


# gettinng all the hex addresses and Adding them to an empty list
def get_addresses (start_address, real_end_address):
    addresses = []
    start_address = start_address[:-1]+'0'
    start_int = int(start_address,16) 
    end_int = int(real_end_address,16)
    next_address = start_int
    while next_address < end_int+16:
        addresses.append(hex(next_address)[2:].upper())
        next_address = start_int + 16
        start_int = next_address
    initailize_df(addresses)
    
   
#creating a dataframe for the memory graph
def initailize_df(addresses):
    df = pd.DataFrame()
    df = df.assign(**{'Addresses':addresses,'0': 'X', '1': 'X', '2': 'X','3':'X','4':'X','5':'X','6':'X','7':'X','8':'X','9':'X','A':'X','B':'X','C':'X','D':'X','E':'X','F':'X'})
    df = df.set_index('Addresses')
    get_memory_graph(df)
    

#how to fill the rows and get the memory graph
def get_memory_graph(df):
    file = open('in_test_no_dots.txt')
    T_rec = file.readlines()[1:-1]
    

    for record in T_rec:
        startT = record[1:7][2:]
        col = startT[-1].upper()
        startT = startT[:-1] + '0'

        rest = record[9:]
        i = 0

        while i <  len(rest) - 1:

            df.at[startT, col] = (rest[i] + rest[i + 1])
            if int(col, 16) < 15:
                col = utilities.add_hex(col,'1')

            else:
                col = "0"
                startT = utilities.add_hex(startT,'10')

            i = i + 2
    file.close()
    show(df)
    
    




