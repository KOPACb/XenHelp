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
    '''возвращает вывод xe vm-list'''
    plain_list = open('list','r')
    return plain_list.readlines()



def main():
    '''основное тело'''
    p_list = get_list()
    #print(p_list) #вывод списка машин
    uuid = re.compile('uuid', re.IGNORECASE)
    name = re.compile('name-label', re.IGNORECASE)
    state = re.compile('power-state',re.IGNORECASE)
    print(uuid,end='')


main()

