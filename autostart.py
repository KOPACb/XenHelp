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

def get_detail(uuid):
    '''get details of VM
    '''
    plain_detail = open(uuid,'r')
    autostart = False
    backup = False
    migrate = False
    for line in plain_detail:
        try:
            field , value = line.split(':')
            if field.find('name-label') != -1:
                name = value.strip()
            if field.find('power-state') != -1:
                state = value.strip()
            if field.find('tags') != -1:
                tags = value.strip()
                if tags.find('autostart') != -1:
                    autostart = True
                if tags.find('backup') != -1:
                    backup = True
                if tags.find('migrate') != -1:
                    migrate = True
            else:
                continue
        except ValueError: continue
    result = dict(uuid=uuid, name=name, state=state, autostart=autostart, backup=backup, migrate=migrate, tags=tags)
    return result



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
        yield uuid
    result = read_uuid(p_list)
    return result


def formatting(p_list):
    i = 0
    lst = {}
    for uuid in p_list:
        try:
            lst[uuid] = get_detail(uuid)
            i += 1
        except ValueError: continue

    return lst
def main():
    '''main unit'''
    p_list = get_list()
    log = list(read_uuid(p_list))
    print(log)
    data = formatting(log)
    print(type(data))
    print(data)

main()

