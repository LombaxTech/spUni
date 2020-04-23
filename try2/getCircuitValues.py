import numpy as np

file = open('testCircuit2.net')
lines = file.readlines()

circuitSwitch = False

for line in lines:
    if (line[0] == '#'):
        pass
    else:
        if ("<CIRCUIT>" in line):
            circuitSwitch = True

        elif ("</CIRCUIT>" in line):
            circuitSwitch = False

        elif (circuitSwitch == True):

            nodeOne = line[3]
            nodeTwo = line[8]

            nodeOne = int(nodeOne)
            nodeTwo = int(nodeTwo)

            if (line[10] == 'R'):
                R = line[12:]
                R = float(R)
                print('Value of R:', R)
            elif(line[10] == 'G'):
                G = line[12:]
                G = float(G)
                R = 1/G
                print('Value of G:', G, 'Value of R:', R)
            elif(line[10] == 'C'):
                C = line[12:]
                C = float(C)
                R = 1 / (1j * 60 * C)

                print('C:', C)
                print('R:', R)
                print('Type of C:', type(C))
                print('Type of R:', type(R))

            # nodeTwo = 0 => shunt, else => series
            # if (nodeTwo == 0):
            #     matrixList.append(np.array([
            #         [1, 0],
            #         [(1/R), 1]
            #     ]).astype(float))
            # else:
            #     matrixList.append(np.array([
            #         [1, R],
            #         [0, 1]
            #     ]).astype(float))


# resultantMatrix = productOfList(matrixList)
# print(resultantMatrix)
