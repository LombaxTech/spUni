# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 09:12 2019 - ish
@author: eessrp
"""
import sys
import os
import re
import filecmp
import EE20084_functions_01 as EE84
import numpy as np


def test_char_by_char(logfile, nline, l1, l2):
    """ Test for equality, character by character, between two lines of text
        Outputs messages to log file.
    :param logfile - file pointer to opened file for log messages
    :param nline - line number within files being compared
    :param l1 - line of text from file one
    :param l2 - line of text from file two
    :return - True if difference is found
    """
    nc1 = len(l1)
    nc2 = len(l2)
    if (nc1 == nc2):
        jjdiff = -1
        err_found = False
        for jj in range(0, nc1):
            same = l1[jj] == l2[jj]
            if ((not same) and (not err_found)):
                jjdiff = jj
                err_found = True
                #st="Characters <%s> and <%s> differ at char %d\n"%(l1[jj],l2[jj],jj)
                # logfile.write(st)
        if (err_found):
            st = "Error found in line %d from character %d\n" % (nline, jjdiff)
            logfile.write(st)
            st = "L1=<%s>\n" % (l1)
            logfile.write(st)
            stb = "-"*(jjdiff+4)+"^\n"
            logfile.write(stb)
            st = "L2=<%s>\n" % (l2)
            logfile.write(st)
            logfile.write(stb)
        else:
            st = "Line %d is OK\n" % (nline)
            logfile.write(st)
    else:
        st = "Line length differs, perfect file line has %d character while user file has %d\n" % (
            nc1, nc2)
        logfile.write(st)
        err_found = True
    return(err_found)


def test_float_equality(logfile, nline, l1, l2, atol, rtol):
    """ Test for equality, character by character, between two lines of text
        Outputs messages to log file.
    :param logfile - file pointer to opened file for log messages
    :param nline - line number within files being compared
    :param l1 - line of text from file one
    :param l2 - line of text from file two
    :param atol - absolute tolerance for isclose equality test
    :param rtol - relative tolerance for isclose equality test
    :return - True if difference is found
    """
    error_in_line = False
    l1a = l1.replace("+j", " ")  # remove real/imag split
    l1 = l1a.replace("/_", " ")  # remove mag/phase split
    l2a = l2.replace("+j", " ")
    l2 = l2a.replace("/_", " ")
#    print("Line 1=",l1)
#    print("Line 1=",l2)
    l1s = l1.split()
    l2s = l2.split()
    nterms1 = len(l1s)
    nterms2 = len(l2s)
    # print("l1s[%d]="%(nterms1))
    # print(l1s)
    # print("l2s[%d]="%(nterms2))
    # print(l2s)
    if (nterms1 == nterms2):
        for ii in range(0, nterms1):
            v1 = float(l1s[ii])
            v2 = float(l2s[ii])
            ok = np.isclose(v1, v2, atol, rtol)
            if (not ok):
                st = "Line %d variable %d differs, perfect=%g, user=%g\n" % (
                    nline, ii, v1, v2)
                logfile.write(st)
                error_in_line = True
    else:
        error_in_line = True
        st = "Line %d contains different number of floats, perfect has %d, user has %d\n" % (
            nline, nterms1, nterms2)
        logfile.write(st)
    if (not error_in_line):
        st = "Line %d is OK\n" % (nline)
        logfile.write(st)
    return(error_in_line)


def test_equality(logfile, f1, f2, atol, rtol):
    """ Test for equality between contents of two output (.out) files
        Outputs messages to log file.
    :param logfile - file pointer to opened file for log messages
    :param f1 - text contents of file one
    :param f2 - text contents of file two
    :param atol - absolute tolerance for isclose equality test
    :param rtol - relative tolerance for isclose equality test
    :return - True if difference is found
    """
    f1split = f1.splitlines()
    f2split = f2.splitlines()
    nlines1 = len(f1split)
    nlines2 = len(f2split)
    len_diff = 0
    err_file = False
    if ((nlines1 > 0) and (nlines2 > 0) and (nlines1 == nlines2)):
        st = "Working on %d lines\n" % (nlines1)
        logfile.write(st)
        line1_err = test_char_by_char(logfile, 1, f1split[0], f2split[0])
        err_file = line1_err or err_file
        line2_err = test_char_by_char(logfile, 2, f1split[1], f2split[1])
        err_file = line2_err or err_file
        for iline in range(2, nlines1):
            float_err = test_float_equality(
                logfile, (iline+1), f1split[iline], f2split[iline], atol, rtol)
            err_file = float_err or err_file
            if (float_err):
                line_err = test_char_by_char(
                    logfile, (1+iline), f1split[iline], f2split[iline])
                err_file = line_err or err_file
    else:
        err_file = True
        st = "Files have different number of lines, perfect has %d lines, user has %d lines\n" % (
            nlines1, nlines2)
        logfile.write(st)
    return(err_file)


def test_near_equality(logfile, f1, f2, atol, rtol):
    f1split = f1.splitlines()
    f2split = f2.splitlines()
    nlines1 = len(f1split)
    nlines2 = len(f2split)
    len_diff = 0
    if ((nlines1 > 0) and (nlines2 > 0) and (nlines1 == nlines2)):
        st = "Working on %d lines\n" % (nlines1)
        logfile.write(st)
        test_char_by_char(logfile, 1, f1split[0], f2split[0])
        test_char_by_char(logfile, 2, f1split[1], f2split[1])
        error_in_line = False
        for iline in range(2, nlines1):
            #            test_char_by_char(logfile,(1+iline), f1split[iline], f2split[iline])
            # jdiff=-1
            # print("line[%d]="%(iline))
            l1 = f1split[iline]
            l1a = l1.replace("+j", " ")
            l1 = l1a.replace("/_", " ")
            # l1b=l1.split()
            l2 = f2split[iline]
            l2a = l2.replace("+j", " ")
            l2 = l2a.replace("/_", " ")
            # l2b=l2.split()
            #l2=f2split[iline].split(' ')
            nterms1 = len(l1)
            nterms2 = len(l2)
            print("l1[%d]=" % (nterms1))
            print(l1)
            print("l2[%d]=" % (nterms2))
            print(l2)
            l1s = l1.split()
            l2s = l2.split()
            nterms1 = len(l1s)
            nterms2 = len(l2s)
            # for jj in range(0,nterms1):
            #     wk=l1[jj].strip()
            #     if (len(wk)>0):
            #         l1s.append(wk)
            # for jj in range(0,nterms2):
            #     wk=l2[jj].strip()
            #     if (len(wk)>0):
            #         l2s.append(wk)
            # nterms1=len(l1s)
            # nterms2=len(l2s)
            print("l1s[%d]=" % (nterms1))
            print(l1s)
            print("l2s[%d]=" % (nterms2))
            print(l2s)
            if (nterms1 == nterms2):
                for ii in range(0, nterms1):
                    v1 = float(l1s[ii])
                    v2 = float(l2s[ii])
                    ok = np.isclose(v1, v2, atol, rtol)
                    if (not ok):
                        st = "Line %d variable %d differs, perfect=%g, user=%g\n" % (
                            iline+1, ii, v1, v2)
                        logfile.write(st)
                        error_in_line = True
            if (not error_in_line):
                st = "Line %d is OK\n" % (iline+1)
                logfile.write(st)
            #         wk2=l2[ii]
            #         nchars1=len(wk1)
            #         diff=""
            #         for jj in range(0,nchars1):
            #             if(not (wk1[jj]==wk2[jj])):
            #                 diff+=wk2[jj]
            #                 if (jdiff<0):
            #                     jdiff=jj
            #         #print("Diff[%d]=<%s>, len=%d"%(ii,diff,len(diff)))
            # if (jdiff>-1):
            #     print("Line %d differed at character %d"%(iline,jdiff))
#            if f2split[line] in f1split[line]:
#                print("f2 in f1")
#                print("len(f2)=%d, len(f1)=%d"%(len(f2split[line]),len(f1split[line])))
#                f1split[line].replace(f2split[line],'')
#                print("Replace <\n%s\n> in <\n%s\n>"%(f2split[line],f1split[line]))
#                len_diff=len(f1split[line])
#            if (len_diff==0):
#                print("Line %d equal"%(line))
#            else:
#                print("Line %d not equal, diff is <%s>"%(line,f1split[line]))


def run_tests(test_names, atol, rtol):
    correct_f = 0
    f_examined = 0
    c_list = []
    i_list = []
    for basename in test_names:
        net_file = "./Data_files/%s.net" % (basename)
        output_file = "./User_files/%s.out" % (basename)
        run_log = "./User_files/%s_run.log" % (basename)
        perfect_file = "./Data_files/%s.out" % (basename)
        compare_log = "./User_files/%s_compare.log" % (basename)
        cf_file = EE84.My_open_file(compare_log, "wt")
        st = 'python %s %s %s >%s 2>&1' % (
            sys.argv[1], net_file, output_file, run_log)
        # python configurations may need 'py' or 'python3' command
        #st='py %s %s %s >%s 2>&1'%(sys.argv[1],net_file,output_file,run_log)
        #st='python3 %s %s %s >%s 2>&1'%(sys.argv[1],net_file,output_file,run_log)
        print("Command is:%s\n" % (st))
        stc = ("Command is:%s\n" % (st))
        cf_file.write(stc)
        os_rtn = os.system(st)
        st = "OS returns %r from execution of command\n" % (os_rtn)
        print(st)
        cf_file.write(st)
        op = filecmp.cmp(perfect_file, output_file)
        st = ("For files %s and %s filecmp returns same=%r\n" %
              (perfect_file, output_file, op))
        cf_file.write(st)
        f_examined += 1
        if (op):
            correct_f += 1
            c_list.append(output_file)
        else:
            st = ("\t\t\tDetailed testing:\n")
            cf_file.write(st)
            file_1 = EE84.My_open_file(perfect_file, "rt")
            file_2 = EE84.My_open_file(output_file, "rt")
            buff1 = file_1.read()
            buff2 = file_2.read()
            unequal = test_equality(cf_file, buff1, buff2, atol, rtol)
            if unequal:
                i_list.append(output_file)
            else:
                correct_f += 1
                c_list.append(output_file)
        cf_file.close()
    return(correct_f, f_examined, c_list, i_list)


def usage():
    print("Command line should be:\npython AutoTest.py MyProg.py Abs_tol Rel_tol\n")
    print("Files need to be in subdirectories of the directory containing Autotest.py and MyProg.py. The input *.net and *.out files from the Moodle site should be in a subdirectory called Data_files. Output from MyProg.py will be written to a subdirectory called User_files\n")
    print("Autotest will run MyProg.py through all of the a_*.net, b_*.net, c_*.net, d_*.net and e_*.net example files from the Moodle site. All of the *.net files and their corresponding model output *.out files from the Moodle site are expected to be in the Data_files subdirectory.")
    #print("The input *.net files are expected to be in a subdirectory called Data_files.")
    print("The output *.out files produced by MyProg.py are written to a subdirectory called User_files.")
    print("Autotest then compares the output files in User_files with the model or 'perfect' output files in Data_files.")
    print("Autotest first uses filecmp to see if the user and model output files are identical.")
    print("If the files are not identical detailed character by character and value by value comparisons are made. The value by value tests are made using numpy.isclose() to see if values are similar enough. This comparison is controlled by the parameters Abs_tol and Rel_tol. The smaller these values the better the agreement needs to be between the model and user output files in order to pass the test. Typically 1.0e-14 is used for both to overcome numeric rounding uncertainty in floating point calculations.")
    print("At the end of the tests a summary is given showing how many files were examined, how many of the files correctly agreed with the model output files and how many were incorrect or different. A summary of the correct and incorrect file names is also printed.")
    print("After running the tests the User_files directory contains *_compare.log files containing some detail of the test, and in particular where the output files differ.")
    print("%s\n" % ('*'*80))


nargs = len(sys.argv)
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

if (nargs < 4):
    print("\n\t\tWrong number of arguments")
    usage()
    sys.exit(1)
Abs_tol = float(sys.argv[2])
Rel_tol = float(sys.argv[3])
print("Tolerances are Abs=%g, Rel=%g" % (Abs_tol, Rel_tol))
correct_files = 0
incorrect_files = 0
files_examined = 0
correct_list = []
incorrect_list = []
divider_line = '*'*80
a_tests = ["a_Test_Circuit_1", "a_Test_Circuit_1C",
           "a_Test_Circuit_BRX", "a_Test_Circuit_L7", "a_Test_Circuit_Ord"]
ncorr, nexam, clist, ilist = run_tests(a_tests, Abs_tol, Rel_tol)
print("%s\nA_test: %d files tested, %d correct, %d incorrect" %
      (divider_line, nexam, ncorr, (nexam-ncorr)))
print("Correct files are:", clist)
print("Incorrect files are:", ilist)
print(divider_line)
correct_files += ncorr
files_examined += nexam
correct_list.append(clist)
incorrect_list.append(ilist)
b_tests = ["b_CR", "b_RC", "b_Pi_03", "b_Pi_03R", "b_Tee_03", "b_Tee_03R"]
ncorr, nexam, clist, ilist = run_tests(b_tests, Abs_tol, Rel_tol)
print("%s\nB_test: %d files tested, %d correct, %d incorrect" %
      (divider_line, nexam, ncorr, (nexam-ncorr)))
print("Correct files are:", clist)
print("Incorrect files are:", ilist)
print(divider_line)
correct_files += ncorr
files_examined += nexam
correct_list.append(clist)
incorrect_list.append(ilist)
c_tests = ["c_LCR", "c_LCG"]
ncorr, nexam, clist, ilist = run_tests(c_tests, Abs_tol, Rel_tol)
print("%s\nC_test: %d files tested, %d correct, %d incorrect" %
      (divider_line, nexam, ncorr, (nexam-ncorr)))
print("Correct files are:", clist)
print("Incorrect files are:", ilist)
print(divider_line)
correct_files += ncorr
files_examined += nexam
correct_list.append(clist)
incorrect_list.append(ilist)
d_tests = ["d_LPF_B50", "d_LPF_B75",
           "d_LPF_B750", "d_LPF_Bess350", "d_LPF_C550"]
ncorr, nexam, clist, ilist = run_tests(d_tests, Abs_tol, Rel_tol)
print("%s\nD_test: %d files tested, %d correct, %d incorrect" %
      (divider_line, nexam, ncorr, (nexam-ncorr)))
print("Correct files are:", clist)
print("Incorrect files are:", ilist)
print(divider_line)
correct_files += ncorr
files_examined += nexam
correct_list.append(clist)
incorrect_list.append(ilist)
e_tests = ["e_Ladder_100", "e_Ladder_400"]
ncorr, nexam, clist, ilist = run_tests(e_tests, Abs_tol, Rel_tol)
print("%s\nE_test: %d files tested, %d correct, %d incorrect" %
      (divider_line, nexam, ncorr, (nexam-ncorr)))
print("Correct files are:", clist)
print("Incorrect files are:", ilist)
print(divider_line)
correct_files += ncorr
files_examined += nexam
correct_list.append(clist)
incorrect_list.append(ilist)


incorrect_files = files_examined-correct_files
print("\n%s\n\t\tTotals\n%d files tested, %d correct, %d incorrect" %
      (divider_line, files_examined, correct_files, incorrect_files))
print("Correct files are:", correct_list)
print("Incorrect files are:", incorrect_list)
print(divider_line)


#os.system('python Dtask_01.py ./Data_files/a_Test_Circuit_1C.net ./Data_files/a_Test_Circuit_1C.out >a_Test_Circuit_1C.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/a_Test_Circuit_BRX.net ./Data_files/a_Test_Circuit_BRX.out >a_Test_Circuit_BRX.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/a_Test_Circuit_L7.net ./Data_files/a_Test_Circuit_L7.out >a_Test_Circuit_L7.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/a_Test_Circuit_Ord.net ./Data_files/a_Test_Circuit_Ord.out >a_Test_Circuit_Ord.log 2>&1')
## st=input("Enter something to continue:")
#
#os.system('python Dtask_01.py ./Data_files/b_CR.net ./Data_files/b_CR.out >b_CR.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/b_RC.net ./Data_files/b_RC.out >b_RC.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/b_Pi_03.net ./Data_files/b_Pi_03.out >b_Pi_03.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/b_Pi_03R.net ./Data_files/b_Pi_03R.out >b_Pi_03R.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/b_Tee_03.net ./Data_files/b_Tee_03.out >b_Tee_03.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/b_Tee_03R.net ./Data_files/b_Tee_03R.out >b_Tee_03R.log 2>&1')
#
#os.system('python Dtask_01.py ./Data_files/c_LCR.net ./Data_files/c_LCR.out >c_LCR.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/c_LCG.net ./Data_files/c_LCG.out >c_LCG.log 2>&1')
#
#os.system('python Dtask_01.py ./Data_files/d_LPF_B50.net ./Data_files/d_LPF_B50.out >d_LPF_B50.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/d_LPF_B75.net ./Data_files/d_LPF_B75.out >d_LPF_B75.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/d_LPF_B750.net ./Data_files/d_LPF_B750.out >d_LPF_B750.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/d_LPF_Bess350.net ./Data_files/d_LPF_Bess350.out >d_LPF_Bess350.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/d_LPF_C550.net ./Data_files/d_LPF_C550.out >d_LPF_C550.log 2>&1')
#
#
#os.system('python Dtask_01.py ./Data_files/FE_Q1_Series_Shunt.net ./Data_files/FE_Q1_Series_Shunt.out >FE_Q1_Series_Shunt.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/FE_Q2_Series_Shunt.net ./Data_files/FE_Q2_Series_Shunt.out >FE_Q2_Series_Shunt.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/FE_Q2Q3_Series_Shunt.net ./Data_files/FE_Q2Q3_Series_Shunt.out >FE_Q2Q3_Series_Shunt.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/FE_Q4_Shunt_Series.net ./Data_files/FE_Q4_Shunt_Series.out >FE_Q4_Shunt_Series.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/FE_Q5Q6_Shunt_Series.net ./Data_files/FE_Q5Q6_Shunt_Series.out >FE_Q5Q6_Shunt_Series.log 2>&1')
#
#os.system('python Dtask_01.py ./Data_files/e_Ladder_100.net ./Data_files/e_Ladder_100.out >e_Ladder_100.log 2>&1')
#os.system('python Dtask_01.py ./Data_files/e_Ladder_400.net ./Data_files/e_Ladder_400.out >e_Ladder_400.log 2>&1')
#
