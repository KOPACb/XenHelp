#-------------------------------------------------------------------------------
# Name:        XEN help
# Purpose:
#
# Author:      KOPACb
#
# Created:     06.11.2012
# Copyright:   (c) KOPACb 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
from itertools import tee


def get_list():
    '''get list of VM by open file with output xe vm-list'''
    plain_list = open('list','r')
    return plain_list.readlines()

def readlog():
    for line in open('list'):
        try:
            x, value = line.split(':')
        except ValueError: continue
        yield value.strip()
    result = tee(readlog(), 3)
    return result

def main():
    '''main unit'''
    p_list = get_list()
    l = print(len(p_list))

    uuid = re.compile('uuid', re.IGNORECASE)
    name = re.compile('name-label', re.IGNORECASE)
    state = re.compile('power-state',re.IGNORECASE)

    log = readlog()
    log[1]



main()

