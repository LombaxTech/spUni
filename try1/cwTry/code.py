import re

file = open('testCircuit1.net')

# for line in file:
#     if (line[0] == '#'):
#         pass
#     else:
#         print(line)

nodes = []

lines = file.readlines()
# print(lines)
for line in lines:
    if re.search("n1=", line):
        # print(line.strip())
        # print(line[3])
        # print(line[8])
        nodes.append(line[3])
        nodes.append(line[8])

largestNode = max(nodes)

print(max(nodes))

# list = ['1', '20', '3303', '22']
# print(max(list))

file.close()