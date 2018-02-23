import os
import sys
import threading
import commands
filename = sys.argv[1]
lock = threading.Lock()
f = open(filename,"r")
x = []
for line in f:
    line = line.rstrip('\n')
    x.append(line)
f.close()
def execute(s):
    cmd1 = "ssh -o PasswordAuthentication=no -o ConnectTimeout=1 -o StrictHostKeyChecking=no {0} exit".format(s)
    z = os.system(cmd1)
    if z == 0:
        cmd2 = "scp /export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh {0}:/export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh".format(s)
        os.system(cmd2)
        cmd3 = "scp /export/home/bs/NagiosCommand/NagiosAgent/libexec/spectre-meltdown-checker.sh {0}:/export/home/bs/NagiosCommand/NagiosAgent/libexec/spectre-meltdown-checker.sh".format(s)
        os.system(cmd3)
        cmd4 = "ssh -t {0} sudo /export/home/bs/NagiosCommand/NagiosAgent/libexec/os-scan.sh meltdown > /tmp/scandata".format(s)
        os.system(cmd4)
        lock.acquire()
        scandata = commands.getoutput("cat /tmp/scandata |grep -v '#'|tr '\n' ';'")
        print scandata
        cmdz = "echo -e '${0};{1}' >> /tmp/out_spectre_results.csv".format(s,scandata)
        os.system(cmdz)
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
    
        
