#!/bin/sh
# Script to delete vm-template.
# Usage: template_rm.sh [UUID]
XE=/usr/bin/xe
GREP=/bin/grep
if [ "$1" == "" ]; then
        echo "No UUID present. Usage:" $0 "[UUID]. "
        exit 0
fi

if [ "${#1}" = 36 ]; then
        $XE template-list uuid=$1
        echo "  "
        $XE template-param-list uuid=a6f46bd7-e2b7-dff9-043a-6797cec7661c | $GREP "other-config"
        echo "If you want to delete this template type 'yes'"
        read CHOISE
else
        echo "UUID not valid. use "xe template-list name-label=[Template name]""
        exit 0
fi


if [ "$CHOISE" = "yes" ]; then
        echo "deleting template"
        $XE template-param-set other-config:default_template=false uuid=$1
        $XE template-param-set is-a-template=false uuid=$1
        $XE vm-destroy uuid=$1
        exit 0
else
        exit 0
fi

exit 0


