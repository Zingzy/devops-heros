#!/bin/bash

current_date=$(date)
host=$(hostname)
user=$(whoami)

echo "Date     : $current_date"
echo "Hostname : $host"
echo "User     : $user"

echo
echo "Disk usage:"
df -h

echo
echo "Running processes (top 10 by CPU usage):"
ps aux | sort -rk 3 | head -n 10

echo
read -p "Enter a directory name to store the report: " dir_name
read -p "Enter a file name for the process list: " file_name

mkdir -p "$dir_name"
report="$dir_name/$file_name"
touch "$report"

ps aux > "$report"

echo
echo "Saved $(wc -l < "$report") lines of process information to $report"
ls -l "$report"
