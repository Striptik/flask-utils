import sys


def log(*argv):
    string_to_print = ""
    for index, arg in enumerate(argv):
        if index == (len(argv) - 1):
            string_to_print += str(arg)
        else:
            string_to_print += "{}, ".format(str(arg))
    print("{}".format(string_to_print), file=sys.stderr)
