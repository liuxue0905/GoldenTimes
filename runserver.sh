#!/bin/bash


PROG_PATH=${BASH_SOURCE[0]}      # this script's name
PROG_NAME=${PROG_PATH##*/}       # basename of script (strip path)
PROG_DIR="$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)"


echo $PROG_PATH
echo $PROG_NAME
echo $PROG_DIR

#echo "$BASH_SOURCE"
#echo "$(dirname "$BASH_SOURCE")"
#
#echo "$0"
#echo "$(dirname "$0")"

LOG_DIR=${PROG_DIR}/log

echo "PROG_DIR	: ${PROG_DIR}"
echo "LOG_DIR		: ${LOG_DIR}"

cd ${PROG_DIR}

echo "pwd		: $(pwd)"

test -d ${LOG_DIR} || mkdir -p ${LOG_DIR}

LOG_FILE_NAME=`date +"%Y%m%d_%H%M%S"`

LOG_FILE=${LOG_DIR}/nohup_${LOG_FILE_NAME}.out

echo "LOG_FILE	: ${LOG_FILE}"

command_runserver="python manage.py runserver 0:8000"
command="nohup "$command_runserver" > "${LOG_FILE}" 2>&1 &"

echo "command		: $command"

#output=$(eval $command)
#echo "$output"
