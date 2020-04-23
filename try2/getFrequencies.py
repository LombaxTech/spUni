
file = open('testCircuit1.net')
# file = open('testCircuit1.net')
lines = file.readlines()

termsSwitch = False

nFrequencies = 0
fStart = 10.0
fEnd = 10e+6
gap = (fEnd - fStart)/(nFrequencies - 1)

for line in lines:
    if (line[0] == '#'):
        pass
    else:
        if ("<TERMS>" in line):
            termsSwitch = True

        elif ("</TERMS>" in line):
            termsSwitch = False

        elif (termsSwitch == True):
            position = line.find('Nfreqs')
            if (position != -1):
                # print(line[position + 7:])
                nFrequencies = line[position + 7:]
                nFrequencies = float(nFrequencies)

fStart = 10.0
fEnd = 10e+6
nFreqs = 50

gap = (fEnd - fStart)/(nFreqs - 1)

# A LIST
freqs = []

for n in range(nFreqs):
    freqs = freqs + [fStart + n*gap]

print(freqs)


for frequency in freqs:
    getMatrix(frequency)
