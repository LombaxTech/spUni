
# # textTwo = ('''Hello
# #                 What
# #                 is
# #                 up
# #                 ''',
# #            name)

# # print(text)

file = open('exampleFile.txt', 'a+')
# file.write('\nhello')

values = {
    'frequency': 10.0,
    'Vin': (3.6149110389092414+0j),
    'Vout': (0.0460440770310109+0j),
    'Iin': (0.02770177922181517+0j),
    'Iout': (0.0006139210270801454+0j),
    'Pin': (0.1001394675063663+0j),
    'Zout': (83.85027371883254+0j),
    'Pout': (2.8267427061835543e-05+0j),
    'Zin': (130.49382171317345+0j),
    'Av': (0.012737264219067526+0j),
    'Ai': (0.02216179048155442+0j)
}


for key in values:
    print(key, values[key])
    file.write()

# ! IMPORTANT
# file.write('      Freq           Vin                   Vout                    Iin                   Iout                    Pin                   Zout                   Pout                    Zin                     Av                     Ai          ')
# file.write('\n        Hz             V                      V                      A                      A                      W                   Ohms                      W                   Ohms                      L                      L          ')
# ! IMPORTANT


file.close()
