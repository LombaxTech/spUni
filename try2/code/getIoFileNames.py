import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

print('input file:', inputFile)
print('output file:', outputFile)


# file = open(inputFile)
# lines = file.readlines()

# print(lines)

# for line in lines:
#     position = line.find('File_name')
#     if (position != -1):
#         # print(line[12:])
#         outputFile = line[12:]

# try:
#     outputFile
# except:
#     inputFile = inputFile[:-4]
#     outputFile = inputFile + '.out'

# print(outputFile)
