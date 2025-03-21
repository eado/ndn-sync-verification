#!/usr/bin/env bash


# https://unix.stackexchange.com/questions/30370/how-to-get-the-pid-of-the-last-executed-command-in-shell-script

$1 >> 'all_log.log' 2>all_error.log &
echo $!