import numpy as np

#  * functions


def productOfList(myList):
    product = 1
    for matrix in myList:
        if (type(product) == int):
            product = matrix
        else:
            product = product @ matrix
    return product


file = open('testCircuit3.net')
lines = file.readlines()

toBeSortedMatrixList = []
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

            elif(line[10] == 'G'):
                G = line[12:]
                G = float(G)
                R = 1/G

            elif(line[10] == 'C'):
                C = line[12:]
                C = float(C)
                R = 1 / (1j * 2 * 3.14 * frequency * C)

            elif(line[10] == 'L'):
                L = line[12:]
                L = float(L)
                R = 1j * 2 * 3.14 * frequency * L

            # ? nodeTwo = 0 => shunt, else => series

            if (nodeTwo == 0):
                toBeSortedMatrixList.append({
                    'nodeOne': nodeOne,
                    'matrix': np.array([
                        [1, 0],
                        [(1/R), 1]
                    ])
                })
            else:
                toBeSortedMatrixList.append({
                    'nodeOne': nodeOne,
                    'matrix': np.array([
                        [1, R],
                        [0, 1]
                    ])
                })

# for matrix in toBeSortedMatrixList:
#     print(matrix)

sortedList = sorted(toBeSortedMatrixList, key=lambda i: i['nodeOne'])
sortedMatrixList = []


# for item in sortedList:
#     print(item)

for obj in sortedList:
    # print(obj['matrix'])
    sortedMatrixList.append(obj['matrix'])

# print(sortedMatrixList)
print(productOfList(sortedMatrixList))

# print sorted(lis, key = lambda i: i['age'])
