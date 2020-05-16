#!/bin/bash

dir_home="$(eval echo $HOME)"
echo "dir_home	: $dir_home"
#echo "\${dir_home%/*}: " ${dir_home%/*}
#echo "\$(dirname \${dir_home}): " $(dirname ${dir_home})

gt_parent="/media/flash"

echo "gt_parent	: $gt_parent"

dir_project=${gt_parent}/GoldenTimes
dir_log=${gt_parent}/log

echo "dir_project	: $dir_project"
echo "dir_log		: $dir_log"

cd ${dir_project}

echo "pwd		: $(pwd)"

test -d ${dir_log} || mkdir -p ${dir_log}

file_log=${dir_log}/nohup.out

echo "file_log	: $file_log"

command_runserver="python manage.py runserver 0:8000"
command="nohup "$command_runserver" > "$file_log" 2>&1 &"

echo "command		: $command"

output=$(eval $command)
echo "$output"
