#!/bin/bash
# Utworzenie listy elementow
COMMAND_ARR=(man passwd pwd ls mkdir cp mv rm chmod chown touch mount umount cat head tail)
COMMAND_ARR+=(htop kill mail scp wc printenv find grep xargs ps uname df du cron passwd history)
echo "# AUTOR: v0jt4s"
echo "# Web: http://python-programming.marzec.eu"
echo 
echo "# HOT 16"
echo 
licz=0
for val in ${COMMAND_ARR[@]}
do
    licz=$((licz+1))
    echo "# ${licz}. $val"
    if [ "$val" == "cd" ] 
    then
        echo "# cd - change directory"
    else
        COMMAND_NAME=$(man $val |head -4 |tail -1)
        echo "# $COMMAND_NAME"
    fi
    echo 
    if [ $licz == 16 ]
    then
        echo 
        echo 
        echo "# HOT 32"
        echo     
    fi
done


