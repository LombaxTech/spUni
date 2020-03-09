import sys
import os


def find_int(string_to_search, name, noisy):

    # string_to_search - the text string to be searched
    # name - text string of the item to be sought in string_to_search
    # noisy - boolean, if true produces more output to the screen
    # @return rtn - integer value found, or particular negative values when not found
    # @return ok - boolean, true if name and integer found otherwise false

    # looks for name in string_to_search
    pp = string_to_search.find(name)

    # name has been found
    if (pp > -1):
        lname = len(name)
        # points at character after name
        idx = pp + lname
        # copy from idx to end
        new_str = string_to_search[idx:]
        # search for equals sign
        qqe = new_str.find('=')

        # equals found
        if (qqe > -1):
            # point at character after equals sign
            idx = qqe + 1
            valstring = new_str[idx:]
            #variables need to be separated by commas
            substring = valstring.split(',')
            # strip gets rid of spare spaces
            teststring = substring[0].strip()
            try:
                rtn = int(teststring)  #convert string to integer
                if noisy:
                    print("Found %s = %g from <%s>" % (name, rtn, teststring))
                ok = True
            except ValueError:
                if noisy:
                    print(
                        'ERROR:\nTried to find int <%s> in string <%s>, valstring is <%s>, teststring is <%s>'
                        % (name, string_to_search, valstring, teststring))
                rtn = -987654321
                ok = False
        else:  # equals not found
            rtn = -113355
            ok = False
            if noisy:
                print(
                    'ERROR:\nTried to find int <%s> in string <%s>. Found <%s> but no equals symbol'
                    % (name, new_str))
    else:  # name not found in string_to_search
        rtn = -123456789
        if noisy:
            print("Failed to find <%s> in <%s>" % (name, str))
        ok = False
    return (rtn, ok)


# main program

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

if (len(sys.argv) < 2):
    print("\n\tError, program needs two arguments to run\n")
    sys.exit(1)

# now open file
input_filename = sys.argv[1]

try:
    fin = open(input_filename, 'rt')
except FileNotFoundError:
    print('File <%s> not found' % (input_filename))
    current_location = os.getcwd()
    # gets the directory where the program is executing from the operating
    # system as this is where the file is expected to be
    print("executing program in directory: " + current_location)
    sys.exit(
        1)  # exits the program, returning a value of 1 to the operating system

#now interpret file
file_lines = fin.readlines()
for index, line in enumerate(file_lines):
    print("Line[%d] =<%s>" % (index, line))
    n1, n1_found = find_int(line, "Node1",
                            True)  # look for Node1 in line with extra output
    n2, n2_found = find_int(line, "Node2",
                            False)  # look for Node2 in line with less output
    happy = n1_found and n2_found
    if (not happy):
        print(
            "Failed to find input in line <%s>\nn1=%d, n1_found=%r, n2=%d, n2_found=%r"
            % (line, n1, n1_found, n2, n2_found))
    else:
        print("Found nodes: n1=%d, n2=%d" % (n1, n2))

#test=input("Enter a value: ")
fin.close()
