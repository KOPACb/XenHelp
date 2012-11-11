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

def readlog(p_list):
    '''format list vms with uuid:%uuid,name:%name,state:%state
    '''
    for line in p_list:
        try:
            x, value = line.split(':')
            if x.find('uuid') != -1:
                value = 'uuid:' + value.strip()
            if x.find('state') != -1:
                value = 'state:' + value.strip()
            if x.find('name') != -1:
                value = 'name:' + value.strip()
        except ValueError: continue
        yield value.strip()
    result = readlog(p_list)
    return result

def read_uuid(p_list):
    '''
    get list of uuid`s
    '''
    for line in p_list:
        try:
            x, value = line.split(':')
            if x.find('uuid') != -1:
                uuid = value.strip()
            else:
                continue
        except ValueError: continue
        yield uuid.strip()
    result = read_uuid(p_list)
    return result


def formatting(list):
    i = 0
    for line in list:
        try:
            f, value = line.split(':')

        except ValueError: continue


def main():
    '''main unit'''
    p_list = get_list()
    l = print(len(p_list))

    log = list(read_uuid(p_list))
    print(log)



main()

