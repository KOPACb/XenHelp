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


def get_list():
    '''get list of VM by open file with output xe vm-list'''
    plain_list = open('list','r')
    return plain_list.readlines()



def main():
    '''main unit'''
    p_list = get_list()
    l = print(len(p_list))

    uuid = re.compile('uuid', re.IGNORECASE)
    name = re.compile('name-label', re.IGNORECASE)
    state = re.compile('power-state',re.IGNORECASE)

    print(p_list[0])



main()

