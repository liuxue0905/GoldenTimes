#!/bin/bash

#echo "$BASH_SOURCE"
#echo "$(dirname "$BASH_SOURCE")"
#echo "$0"
#echo "$(dirname "$0")"

echo "pwd		:$(pwd)"

#PROG_PATH=${BASH_SOURCE[0]} # this script's name
PROG_PATH=$0 # this script's name
PROG_NAME=${PROG_PATH##*/}  # basename of script (strip path)
PROG_DIR="$(cd "$(dirname "${PROG_PATH:-$PWD}")" 2>/dev/null 1>&2 && pwd)"

echo "PROG_PATH	:$PROG_PATH"
echo "PROG_NAME	:$PROG_NAME"
echo "PROG_DIR	:$PROG_DIR"

LOG_DIR=${PROG_DIR}/log

echo "PROG_DIR	:${PROG_DIR}"
echo "LOG_DIR		:${LOG_DIR}"

#RET=$(cd "${PROG_DIR}" || exit)
RET=$(cd "${PROG_DIR}" 2>&1 || exit)
echo "RET		:${RET}"

test -d "${LOG_DIR}" || mkdir -p "${LOG_DIR}"

LOG_FILE_NAME=$(date +"%Y%m%d_%H%M%S")

LOG_FILE=${LOG_DIR}/nohup_${LOG_FILE_NAME}.out

echo "LOG_FILE	: ${LOG_FILE}"

#COMMAND_RUNSERVER="python manage.py runserver 0:8000"
#COMMAND_RUNSERVER="gunicorn -b 0:8000 -w 3 --threads 2 GoldenTimes.wsgi"
COMMAND_RUNSERVER="gunicorn GoldenTimes.wsgi -c gunicorn.conf.py"
COMMAND="nohup ${COMMAND_RUNSERVER} > ${LOG_FILE} 2>&1 &"

echo "COMMAND		: ${COMMAND}"

#output=$(eval "${COMMAND}")
#echo "$output"
