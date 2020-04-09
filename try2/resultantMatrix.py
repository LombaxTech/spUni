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

circuitSwitch = False

for line in lines:
    if (line[0] == '#'):
        pass
    else:
        if ("<CIRCUIT>" in line):
            circuitSwitch = True

        elif ("</CIRCUIT" in line):
            circuitSwitch = False

        elif (circuitSwitch == True):
            nodeOne = line[3]
            nodeTwo = line[8]

            nodeOne = int(nodeOne)
            nodeTwo = int(nodeTwo)

            if (nodeTwo == 0):
                pass
                # print('this is a shunt')
            else:
                pass
                # print('this is a series')

            if (line[10] == 'R'):
                R = line[12:getPositionOfSpace(12)]
                R = float(R)
                print(R)
            elif(line[10] == 'G'):
                G = line[12:getPositionOfSpace(12)]
                G = float(G)
                R = 1/G
                print('R is:', R, 'G is:', G)
