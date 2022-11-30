#!/usr/bin/env python

import re

phone_number_re = re.compile('(\\+\\d+)? \\((\\d\\d\\d)\\) (\\d\\d\\d)-(\\d\\d\\d\\d)')


def reverse_string(x):
    return reverse_string(x[1:] + x[0])


def clean_phone_number(phone_number):
    groups = phone_number_re.match(phone_number).groups()
    return ''.join(groups)
