outputFile = open('exampleOutput.txt', 'w')

outputFile.write('      Freq           Vin                   Vout                    Iin                   Iout                    Pin                   Zout                   Pout                    Zin                     Av                     Ai          ')
outputFile.write('\n        Hz             V                      V                      A                      A                      W                   Ohms                      W                   Ohms                      L                      L          ')

values = {
    'frequency': 10.0,
    'Vin': 3.6149110389092414+0j,
    'Vout': -0.0460440770310109+0j,
    'Iin': 0.02770177922181517+0j,
    'Iout': -0.0006139210270801454-02209j,
    'Pin': 0.1001394675063663-2290j,
    'Zout': -83.85027371883254+0j,
    'Pout': -2.8267427061835543e-05+0j,
    'Zin': -130.49382171317345+0j,
    'Av': 0.012737264219067526+0j,
    'Ai': 0.02216179048155442-1010j
}

outputFile.write('\n')

for key in values:

    realPart = values[key].real
    imaginaryPart = values[key].imag

    realPart = '%.3e' % realPart
    imaginaryPart = '%.3e' % imaginaryPart

    if (key == 'frequency'):
        # print(realPart)
        outputFile.write(' ' + realPart)
    else:
        # * IMAGINARY POSITIVE & REAL POSITIVE
        if ((float(imaginaryPart) >= 0) and (float(realPart) >= 0)):
            outputFile.write('  ' + realPart + '+j ' + imaginaryPart)

        # * IMAGINARY NEGATIVE & REAL POSTIVE
        elif((float(imaginaryPart) < 0) and (float(realPart) >= 0)):
            outputFile.write('  ' + realPart + '+j' + imaginaryPart)

        # * IMAGINARY POSITIVE & REAL NEGATIVE
        if ((float(imaginaryPart) >= 0) and (float(realPart) < 0)):
            outputFile.write(' ' + realPart + '+j ' + imaginaryPart)

        # * IMAGINARY NEGATIVE & REAL NEGATIVE
        elif((float(imaginaryPart) < 0) and (float(realPart) < 0)):
            outputFile.write(' ' + realPart + '+j' + imaginaryPart)


# testValue = 0.1001-0.000000002188j

# realPart = testValue.real
# imaginaryPart = testValue.imag

# realPart = '%.3e' % realPart
# imaginaryPart = '%.3e' % imaginaryPart

# realPart = float(realPart)
# imaginaryPart = float(imaginaryPart)

# print(imaginaryPart)


# if (realPart < 0):
#     print('real is negative')
# else:
#     print('real is positive')

# print('\nReal: ', realPart, 'Complex:', imaginaryPart)
# if (values[key] == )

# print(values[key].real, values[key].imag)

# print('%.3e' % 1.11111)

# myNumber = '%.3e' % 1.11111

# print(myNumber)

# outputFile.write('\n')
# for key in values:
#     outputFile.write('  ' + str(values[key]) + '   ')

# listOfValues = [values, values, values]

# print(len(listOfValues))
# print(listOfValues[])

# i = 0

# # * RAKIB WORKING CODE :)
# while (i < len(listOfValues)):
#     print(listOfValues[i])
#     print('\n')
#     i = i + 1
# # ! WEI WEI CODE NOT WORKING qwq T_T
# while (listOfValues[i] != ' '):
#     print(listOfValues[i])
#     i = i + 1
#     print('\n')
