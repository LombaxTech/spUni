# * opening the file
file = open('testCircuit1.net')

# * getting the lines of the file
lines = file.readlines()

circuitSwitch = False

# * use a FOR LOOP to read the lines more clearly

# for line in lines:
#     print(line)

# * GET RID OF COMMENTS

for line in lines:
    if (line[0] != '#'):

        if ('<CIRCUIT>' in line):
            circuitSwitch = True

        elif('</CIRCUIT>' in line):
            circuitSwitch = False

        elif(circuitSwitch == True):
            print(line)


# sentence = 'Hello my name is Rakib'
# print('Wei' in sentence)


# myNameList = ['rakib', 'zac', 'wei']
# myNumberList = [1, 3, 5]

# for item in myNumberList:
#     print(number + 1)
