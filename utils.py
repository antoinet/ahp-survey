#!/usr/bin/env python

import string
import random

def generate_pairs(char, *args):
    res = []
    for i in range(0, len(args)):
        for j in range(i + 1, len(args)):
            res.append(args[i] + char + args[j])
    return res

def generate_random_string(length):
    alphabet = string.lowercase + string.digits
    return ''.join(random.sample(alphabet, length))