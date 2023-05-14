
import sic
import sicxe
import pandas as pd 
from pandasgui import show

print('What do you want to see ? ')
while 1:

    x = input('for Sic press 1, for Sicxe press 2\n')
    if x == '1':
        sic.GetLimits()
        break
    elif x == '2':
        sicxe.get_limtisXE()
        break
    else :
        print('please enter your choice correctly')
