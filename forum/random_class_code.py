from random import *
import string


def random_string_generator():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    return "".join(choice(allchar) for x in range(randint(min_char, max_char)))

