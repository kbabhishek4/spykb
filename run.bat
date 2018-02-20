@echo off
title spykb Run
color 1b

echo spykb by: Kbabhishek4
echo #################################
: execute
echo Please Type Command:
set /p command=Command:
python run.py %command%
goto execute
