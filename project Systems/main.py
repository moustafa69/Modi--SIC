from pass_1 import intermidiate_maker as Parsing
from pass_1 import pass1, symbol_table
from pass_2 import pass2, HTE


input_path = 'Inputs/in5.txt'
# parsing input file
df = Parsing.parser(input_path)
# x
f = open('outputs\\intermdiate.txt', 'w')
df_toString = df.to_string(header=False, index=False)
f.write(df_toString)
f.close()

# Get Location Counter'
df_lcounter = pass1.pass1extractor(df)
f = open('outputs\\locationCounter.txt', 'w')
df_toString = df_lcounter.to_string(header=False, index=False)
f.write(df_toString)
f.close()

# Get symbol Table
df_symbolTable = symbol_table.getSymbolTable(df_lcounter)
f = open('outputs\\symbolTable.txt', 'w')
df_toString = df_symbolTable.to_string(header=False, index=False)
f.write(df_toString)
f.close()

# Get objectCode
df_objCode = pass2.pass2Extractor(df)
f = open('outputs\\objectCode.txt', 'w')
df_toString = df_objCode.to_string(header=False, index=False)
f.write(df_toString)
f.close()

# Get HTE Record
HTE = HTE.getRecord(df_objCode)
f = open('outputs\\HTE.txt', 'w')
f.write(HTE)
f.close()

