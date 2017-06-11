#encoding: utf-8
import subprocess

def monitor():

    _fh = open('/proc/meminfo')
    _total = float(_fh.readline().split()[1])
    _free = float(_fh.readline().split()[1])
    _available= float(_fh.readline().split()[1])
    _buffer = float(_fh.readline().split()[1])
    _fh.close()

    shell_ip = "ifconfig ens33|grep -E 'inet[^6]' |awk -F'[ :]+' '{print $4}'"
    result_ip = subprocess.Popen(shell_ip,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    ip = result_ip.stdout.read().decode('utf-8').strip()
    if len(ip) == 0 :
        ip = result_ip.stderr.read()

    value_mem = {
        "ip":ip,
        "item":"memory",
        "mem_total":_total,
        "mem_free":_free,
        "mem_available":_available,
        "buffer":_buffer
    }
    # print(value_mem)
    return value_mem

if __name__=="__main__":
    monitor()




    