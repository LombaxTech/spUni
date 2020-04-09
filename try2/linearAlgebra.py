import numpy as np

matrixA = np.array([
    [0, 1],
    [1, 1]
])

matrixB = np.array([
    [3, -1],
    [1, 11]
])

matrixC = np.array([
    [-3, 11],
    [4, 3]
])

matrixA = matrixA.astype(float)
matrixB = matrixB.astype(float)


# matrixC = matrixA @ matrixB

matrixList = []

matrixList.append(matrixA)
matrixList.append(matrixB)
matrixList.append(matrixC)

# product = 1
# product = matrixA
# print(product)

# if (matrixA != 1):
#     print('matrix a is not 1')

# print(type(1))
# print(type(matrixA))

# if (type(1) == int):
#     print('hello')


def productOfList(myList):
    product = 1
    for matrix in myList:
        if (type(product) == int):
            product = matrix
        else:
            product = product @ matrix
    return product


matrixListTwo = []

matrixListTwo.append(np.array([
    [0, 1],
    [1, 1]
]))

matrixListTwo.append(np.array([
    [3, -1],
    [1, 11]
]).astype(float))

# print(productOfList(matrixListTwo))
# print(productOfList(matrixList))


# list1 = [2, 5, 6]
# print(np.prod(list1))

# print(matrixC)

# print(type(matrixA[0][1]))
# print(type(matrixA[1][0]))


# try:
#     import numpy
# except ImportError:
#     print("numpy is not installed")


R = 5

resistanceMatrix = np.array([
    [1, (1/R)],
    [0, 1]
])

print(resistanceMatrix)
