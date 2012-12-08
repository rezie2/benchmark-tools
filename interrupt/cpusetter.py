import sys, os

'''
To get the PIDs, save them to a file when forking. 1 child PID per fork.

'''

cosactive = 0 # for testing with just linux or coslinux

def config():

    cos_cpu = 6
    linux_cpu = 7

    # Setting up
    os.system("echo -1 > /proc/sys/kernel/sched_rt_runtime_us")

    if not(os.path.isdir("/dev/cpuset")):
        os.system("mkdir -p /dev/cpuset")
    if not(os.path.isfile("/dev/cpuset/cpuset.cpus")):
        os.system("mount -t cgroup -ocpuset cpuset /dev/cpuset")

    # Composite
    if cosactive:    
        if not(os.path.isdir("/dev/cpuset/cos")):
            os.system("mkdir -p /dev/cpuset/cos")
        #os.system("echo 0-" + str(cos_cpu) +  " > /dev/cpuset/cos/cpuset.cpus")
        os.system("echo 0 > /dev/cpuset/cos/cpuset.cpus")

    # Worker 1
    if not(os.path.isdir("/dev/cpuset/worker1")""
        os.system("mkdir -p /dev/cpuset/worker1")
    os.system("echo 0-" + str(linux_cpu) + " > /dev/cpuset/worker1/cpuset.cpus")

    os.system("wget --output-document=/dev/null speedtest.qsc.de/10GB.qsc")
    os.system("WPID=$(ps aux | grep '[s]peedtest' | awk -v WPID=$WPID '{ print $2 }')")
    os.system("echo $WPID > /dev/cpuset/worker1/tasks")


def main():

    try:
        opts, args = getopt.getopt(argv, 'c:l:', ["cos=", "linux="])
    except getopt.GetoptError:
        print 'Usage: filter.py -c <coscores> -l <linuxcores>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-c', '--cos'):
            iname = arg


    filter(iname, maximum, minimum, multiple)

if __name__ == "__main__":
    main()
