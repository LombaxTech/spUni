def checkIfNumber(input):
    if ((input != 0) and (input != 1) and (input != 2) and (input != 3) and (input != 4) and (input != 5) and (input != 6) and (input != 7) and (input != 8) and (input != 9) and (input != '0') and (input != '1') and (input != '2') and (input != '3') and (input != '4') and (input != '5') and (input != '6') and (input != '7') and (input != '8') and (input != '9') and (input != '.')):
        return False
    else:
        return True


def getPositionOfSpace(startPosition):
    spaceFound = False
    countUntilSpace = 0
    while(spaceFound == False):
        if (checkIfNumber(line[startPosition + countUntilSpace]) == False):
            spaceFound = True
        else:
            countUntilSpace += 1
    return (startPosition + countUntilSpace)


file = open('testCircuit1.net')
lines = file.readlines()

termSwitch = False

for line in lines:
    if (line[0] == '#'):
        pass
    else:
        if ("<TERMS>" in line):
            termSwitch = True

        elif ("</TERMS>" in line):
            termSwitch = False

        elif (termSwitch == True):
            position = line.find('VT')
            if (position != -1):
                positionOfSpace = getPositionOfSpace(position + 3)
                # print(line[position + 3: positionOfSpace])
                VT = line[position + 3: positionOfSpace]
                VT = float(VT)

            position = line.find('RS')
            if (position != -1):
                positionOfSpace = getPositionOfSpace(position + 3)
                # print(line[position + 3: positionOfSpace])
                RS = line[position + 3: positionOfSpace]
                RS = float(RS)

            position = line.find('RL')
            if (position != -1):
                positionOfSpace = getPositionOfSpace(position + 3)
                # print(line[position + 3: positionOfSpace])
                RL = line[position + 3: positionOfSpace]
                RL = float(RL)

            position = line.find('GS')
            if (position != -1):
                positionOfSpace = getPositionOfSpace(position + 3)
                # print(line[position + 3: positionOfSpace])
                GS = line[position + 3: positionOfSpace]
                GS = float(GS)


print(VT)
print(RS)
print(RL)
