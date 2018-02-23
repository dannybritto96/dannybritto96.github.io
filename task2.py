import os
import sys
import threading
filename = sys.argv[1]
lock = threading.Lock()
f = open(filename,"r")
x = []
for line in f:
    line = line.rstrip('\n')
    x.append(line)
def execute(s):
    os.system("./spectre.sh {0}".format(s))
for item in x:
    t = threading.Thread(target = execute, args = (item,))
    t.start()

while threading.active_count()>1:
    pass
else:
    f.close()
