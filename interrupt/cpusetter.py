import sys, os, getopt
from os.path import expanduser

'''
Notes:
This setter requires some manual tweaking depending on the system you use it on.
Currently it accepts via command line the number of cores to allocate to cos and Linux
but it is not being used. Right now, the workers are manually allocated to cpusets with 
the CPUs that should be used. This code also assumes you have a linux kernel named
"linux-2.6.36-b" (b for benchmark) in your $HOME/research directory. 

The cosactive global will be used to test for configurations with just Linux or Linux/Cos.

Possible problem: parent tasks within a cpuset _should_ delegate any child processes to
the same cpuset. This is very important for the worker set to function properly because
the compile process spawns a lot of different tasks during the entire process

'''

cosactive = 0 # for testing with just linux or coslinux

def config(coscores, lincores):

    cos_cpu = int(coscores)
    linux_cpu = int(lincores) - 1

    # Setting up
    os.system("echo -1 > /proc/sys/kernel/sched_rt_runtime_us")

    if not(os.path.isdir("/dev/cpuset")):
        os.system("mkdir -p /dev/cpuset")
    if not(os.path.isfile("/dev/cpuset/cpuset.cpus")):
        os.system("mount -t cgroup -ocpuset cpuset /dev/cpuset")
    ## Ethernet affinity
    os.system("echo c0 > /proc/irq/16/smp_affinity")
    
    # Composite
    if cosactive:    
        if not(os.path.isdir("/dev/cpuset/cos")):
            os.system("mkdir -p /dev/cpuset/cos")
        #os.system("echo 0-" + str(cos_cpu) +  " > /dev/cpuset/cos/cpuset.cpus")
        os.system("echo 0 > /dev/cpuset/cos/cpuset.cpus")

    # Worker 1 - wget a large file
    if not(os.path.isdir("/dev/cpuset/worker1")):
        os.system("mkdir -p /dev/cpuset/worker1")
    #os.system("echo 0-" + str(linux_cpu) + " > /dev/cpuset/worker1/cpuset.cpus")
    os.system("echo 6-7 > /dev/cpuset/worker1/cpuset.cpus")

    os.system("wget --output-document=/dev/null speedtest.qsc.de/10GB.qsc")
    os.system("WPID=$(ps aux | grep '[s]peedtest' | awk -v WPID=$WPID '{ print $2 }')")
    os.system("echo $WPID > /dev/cpuset/worker1/tasks")

    # Worker 2 - compile linux
    print("Worker 2 executing...\n   ...cleaning kernel src tree")
    os.system("(cd /home/rezie/research/linux-2.6.36-b/; fakeroot make-kpkg clean)")

    if not(os.path.isdir("/dev/cpuset/worker2")):
        os.system("mkdir -p /dev/cpuset/worker2")
    os.system("echo 1-5 > /dev/cpuset/worker2/cpuset.cpus")

    homedir = expanduser("~")
    os.system("(cd " + homedir + "/research/linux-2.6.36-b/; fakeroot make-kpkg --initrd --append-to-version=-b kernel-image kernel-headers)")
    os.system("WPID=$(ps aux | grep '[s]peedtest' | awk -v WPID=$WPID '{ print $2 }'")
    os.system("echo $WPID > /dev/cpuset/worker2/tasks")

def setclean():
    os.system()

def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'c:l:r', ["cos=", "linux=", "clean"])
    except getopt.GetoptError:
        print 'Usage: filter.py -c <coscores> -l <linuxcores>'
        return
    for opt, arg in opts:
        if opt in ('-c', '--cos'):
            coscores = arg
        if opt in ('-l', '--linux'):
            lincores = arg
        if opt in ('-r', '--clean'):
            setclean()
            return

    config(coscores, lincores)

if __name__ == "__main__":
    main(sys.argv[1:])
