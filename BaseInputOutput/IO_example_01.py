# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 09:12 2019 - ish
@author: eessrp
"""
import sys
import os

def find_int(string_to_search,name,noisy):
    """
    @param string_to_search - the text string to be searched
    @param name - text string of the item to be sought in string_to_search
    @param noisy - boolean, if true produces more output to the screen
    @return rtn - integer value found, or particular negative values when not found
    @return ok - boolean, true if name and integer found otherwise false
    """
    pp=string_to_search.find(name)    # looks for name in string_to_search
    if (pp>-1):     # name has been found
        lname=len(name)
        idx=pp+lname   # points at character after name
        new_str=string_to_search[idx:]  # copy from idx to end
        qqe=new_str.find('=')  # search for equals sign
        if (qqe>-1):   # equals found
            idx=qqe+1  # point at character after equals sign
            valstring=new_str[idx:]
            substring=valstring.split(',') #variables need to be separated by commas
            teststring=substring[0].strip() # strip gets rid of spare spaces
            try:
                rtn=int(teststring)  #convert string to integer
                if noisy:
                    print("Found %s = %g from <%s>"%(name,rtn,teststring))
                ok=True
            except ValueError:
                if noisy:
                    print('ERROR:\nTried to find int <%s> in string <%s>, valstring is <%s>, teststring is <%s>'%(name,string_to_search,valstring,teststring))
                rtn=-987654321
                ok=False
        else:  # equals not found
            rtn=-113355
            ok=False
            if noisy:
                print('ERROR:\nTried to find int <%s> in string <%s>. Found <%s> but no equals symbol'%(name,new_str))
    else:  # name not found in string_to_search
        rtn=-123456789
        if noisy:
            print("Failed to find <%s> in <%s>"%(name, str))
        ok = False
    return(rtn, ok)
#

# main program
    
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))
if (len(sys.argv)<2):
    print("\n\tError, program needs two arguments to run\n" )
    sys.exit(1)
# now open file
input_filename=sys.argv[1]
try:
    fin=open( input_filename,'rt')
except FileNotFoundError:
    print('File <%s> not found'%(input_filename))
    current_location=os.getcwd() 
    # gets the directory where the program is executing from the operating 
    # system as this is where the file is expected to be
    print("executing program in directory: "+current_location) 
    sys.exit(1)  # exits the program, returning a value of 1 to the operating system 
#now interpret file
file_lines=fin.readlines()
for index,line in enumerate(file_lines):
    print("Line[%d] =<%s>"%(index,line))
    n1, n1_found=find_int(line,"Node1",True) # look for Node1 in line with extra output
    n2, n2_found=find_int(line,"Node2",False) # look for Node2 in line with less output
    happy=n1_found and n2_found
    if (not happy):
        print("Failed to find input in line <%s>\nn1=%d, n1_found=%r, n2=%d, n2_found=%r"%(line,n1,n1_found,n2,n2_found))
    else:
        print("Found nodes: n1=%d, n2=%d"%(n1,n2))

#test=input("Enter a value: ")
fin.close()




