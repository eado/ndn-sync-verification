#!/usr/bin/bash

# https://unix.stackexchange.com/questions/30370/how-to-get-the-pid-of-the-last-executed-command-in-shell-script
$1 > /dev/null 2>/dev/null &
echo $!
