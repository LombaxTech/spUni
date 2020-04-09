# Functions
import sys


def checkIfNumber(input):
    if ((input != 0) and (input != 1) and (input != 2) and (input != 3) and (input != 4) and (input != 5) and (input != 6) and (input != 7) and (input != 8) and (input != 9) and (input != '0') and (input != '1') and (input != '2') and (input != '3') and (input != '4') and (input != '5') and (input != '6') and (input != '7') and (input != '8') and (input != '9')):
        return False
    else:
        return True
# end of functions


# Start of main program

file = open('testCircuit1.net')

lines = file.readlines()

# for line in lines:
#     if (line[0] == '#'):
#         pass
#     else:
#         print(line)

VT = 0
RS = 0
RL = 0
IN = 0
countUntilSpace = 0
spaceFound = False

termsSwitch = False

# *GETTING VALUES IN TERMS BLOCK

for line in lines:
    if (line[0] == '#'):
        pass
    else:
        if ("<TERMS>" in line):
            termsSwitch = True

        elif ("</TERMS" in line):
            termsSwitch = False

        elif (termsSwitch == True):
            # print(line)
            # if (('VT' in line) or ('RL' in line)):
            position = line.find('RS')
            if (position != -1):
                while(spaceFound == False):
                    if (checkIfNumber(line[position + 3 + countUntilSpace]) == False):
                        spaceFound = True
                    else:
                        countUntilSpace += 1

                # print(countUntilSpace)
                # print(line[position + 3: position + 3 + countUntilSpace])
                RS = line[position + 3: position + 3 + countUntilSpace]
                print(RS)


# print(checkIfNumber('6'))
