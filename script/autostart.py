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
import sys
import subprocess
import os
import time


pidfile = "/tmp/autostart.pid"

def check_pid(pid):        #habr_user glebkk TY
    """ Check For the existence of a unix pid. """
    try:
      os.kill(pid, 0)
    except OSError:
      return False
    else:
      return True

def get_list():
    '''get list of VM by open file with output xe vm-list'''
    #plain_list = open('list','r')
    vm_list = ['/usr/bin/xe', 'vm-list']
    (plain_list, err) = subprocess.Popen(vm_list,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
    lst = []
    l = ''
    for line in plain_list:
        l = l + line
        if line == '\n':
                lst.append(l)
                l = ''
    return lst

def get_plain_detail(uuid):
    '''get xe vm-param list '''
    uuid =  'uuid=' + uuid
    param = ['/usr/bin/xe', 'vm-param-list', uuid]
    (plain_detail, err) = subprocess.Popen(param ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
    lst = []
    l = ''
    for line in plain_detail:
        l = l + line
        if line == '\n':
                lst.append(l)
                l = ''
    return lst


def get_detail(uuid):
    '''process xe vm-param-list option
    OUTPUT is
    {uuid:uuid, name=name, state:state, autostart=tag_autostart_bool, backup:tag_backup_bool, migrate:migrate_tag_bool, tags:list_of_tags}
    '''
    plain_detail = get_plain_detail(uuid)
    autostart = False
    backup = False
    migrate = False
    name = ''
    state = ''
    tags = ''
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

def get_boot_state(uuid):
    plain_detail = get_plain_detail(uuid)
    for string in plain_detail:
        try:
            splitted = string.split(':')
            if 'networks' in splitted[0]:
                if 'ip' in splitted[1]:
                    return True
                    break
                else:
                    return False
                    break
        except ValueError: continue
    return False



def read_uuid(p_list):
    '''
    get list of uuid`s
    '''
    uuids = []
    for line in p_list:
        try:
            x, value = line.split(':')
            if x.find('uuid') != -1:
                uuids.append(value.strip())
            else:
                continue
        except ValueError: continue
    return uuids


def formatting(p_list):
    '''
    compare UUID`s with needed parameters
    output as DICT of DICTS
    {uuid:{params}}
    '''
    i = 0
    lst = {}
    for uuid in p_list:
        try:
            lst[uuid] = get_detail(uuid)
            i += 1
        except ValueError: continue

    return lst

def start(uuid):
    uuid =  'uuid=' + uuid
    param = ['/usr/bin/xe', 'vm-start', uuid]
    (out, err) = subprocess.Popen(param ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
    return out

def wait_up(uuid):
    while not(get_boot_state(uuid)):
            time.sleep(10)
    return 'started'

def main():
    '''main unit'''
    pid = -1
    if os.path.isfile(pidfile):
        pid = long(open(pidfile, 'r').read())
    if check_pid(pid):
      print "%s already exists, exiting" % pidfile
      sys.exit()
    pid = str(os.getpid())
    file(pidfile, 'w').write(pid)
    # actual code


    p_list = get_list()                     #get VM_list
    log = list(read_uuid(p_list))           #make uuid list
    data = formatting(log)                  #make parameters for working with

    for uuid in data:
        try:
            if data[uuid]['state'] == 'halted' and data[uuid]['autostart'] == True:
                start(uuid)
                print('start called for uuid:', uuid, 'name:', data[uuid]['name'])
                print(wait_up(uuid))
            else: continue
        except ValueError:continue


    # finish
    os.unlink(pidfile)


main()

