import os
import sys
import threading
filename = sys.argv[1]
lock = threading.Lock()
f = open(filename,"r")
q = open("/tmp/spectre_results.csv","a+")
p = open("/tmp/scandata","r")
x = []
y = []
for line in f:
    line = line.rstrip('\n')
    x.append(line)
f.close()
def execute(s):
    cmd1 = "ssh -o PasswordAuthentication=no -o ConnectTimeout=1 -o StrictHostKeyChecking=no {0}".format(s)
    y = os.system(cmd1)
    if y == 0:
        cmd2 = "scp /export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh {0}:/export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh".format(s)
        os.system(cmd2)
        cmd3 = "scp /export/home/bs/NagiosCommand/NagiosAgent/libexec/spectre-meltdown-checker.sh {0}:/export/home/bs/NagiosCommand/NagiosAgent/libexec/spectre-meltdown-checker.sh".format(s)
        os.system(cmd3)
        cmd4 = "ssh -t {0} sudo /export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh meltdown > /tmp/scandata".format(s)
        os.system(cmd4)
        for line in p:
            if '#' in line:
                pass
            else:
                y.append(line.replace('\n',''))
        op = ';'.join(y)
        lock.acquire()
        q.write("{0};{1}\n".format(s,op))
        lock.release()    
def scp():
    cmdx = "scp /tmp/spectre_results.csv splk001:/app01/splunk/var/run/splunk/csv/spectre-meltdown.csv"
    os.system(cmdx)

for item in x:
    t = threading.Thread(target = execute, args = (item,))
    t.start()

while threading.active_count()>1:
    pass
else:
    scp()
    p.close()
    q.close()
    
        