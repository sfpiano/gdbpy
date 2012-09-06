#source ~/.gdb/gdbStlUtils
source ~/.gdb/autoload.py

set $COLOREDPROMPT = 1
if $COLOREDPROMPT == 1
  set prompt \033[32mgdb$ \033[0m
end
