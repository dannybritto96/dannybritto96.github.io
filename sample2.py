import threading
import os
import re
import sys
lock = threading.Lock()
filename = sys.argv[1]
f = open(filename,"r")
p = open("output_file","w+")
q = open("fail","w+")
x = []
for line in f:
    line = line.rstrip('\n')
    x.append("ssh {0} grep common /export/home/bs/.profile|grep -v '#'".format(line))
def execute(l):           
    for item in l:
        server = re.search(r'ssh (.*?) grep',item).group(1)
        try:
            y = os.system(item)
            if y is 0:
                lock.acquire()
                p.writelines("{0}\n".format(server))
                lock.release()
        except:
            lock.acquire()
            q.writelines("{0}\n".format(server))
            lock.release()
            
chunks = [x[i:i+5] for i in xrange(0, len(x), 5)]
for item in chunks:
    t = threading.Thread(target = execute, args = (item,))
    t.start()
    
while threading.active_count()>1:
    pass
else:
    p.close()