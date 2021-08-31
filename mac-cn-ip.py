#!/usr/bin/env python3

import platform
import requests
import textwrap
import subprocess


def generate_up_and_down():
    print("Fetching IP data from https://github.com/misakaio/chnroutes2, it might take a few minutes, please wait...")
    url = r'https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt'
    r = requests.get(url).text
    ip_data = [line for line in r.split("\n") if match_ip(line) and line[0] != "#"]

    up_header = textwrap.dedent("""\
    #!/bin/sh
    
    export PATH="/bin:/sbin:/usr/sbin:/usr/bin"
    
    OLDGW=`netstat -nr | grep '^default' | grep -v 'ppp' | sed 's/default *\\([0-9\.]*\\) .*/\\1/' | awk '{if($1){print $1}}'`
    
    if [ ! -e /tmp/pptp_oldgw ]; then
        echo "${OLDGW}" > /tmp/pptp_oldgw
    fi
    
    dscacheutil -flushcache
    
    # local-ip
    route add 10.0.0.0/8 "${OLDGW}"
    route add 172.16.0.0/12 "${OLDGW}"
    route add 192.168.0.0/16 "${OLDGW}"
    
    # cn-ip
    """)

    with open('ip-up', 'wt') as f:
        f.write(up_header)
        for ip_and_mask in ip_data:
            f.write('route add %s "${OLDGW}"\n' % ip_and_mask)

    down_header = textwrap.dedent("""\
    #!/bin/sh
    export PATH="/bin:/sbin:/usr/sbin:/usr/bin"
    
    if [ ! -e /tmp/pptp_oldgw ]; then
            exit 0
    fi
    
    OLDGW=`cat /tmp/pptp_oldgw`
    
    # local-ip
    route delete 10.0.0.0/8 "${OLDGW}"
    route delete 172.16.0.0/12 "${OLDGW}"
    route delete 192.168.0.0/16 "${OLDGW}"
    
    # cn-ip
    """)
    with open('ip-down', 'wt') as f:
        f.write(down_header)
        for ip_and_mask in ip_data:
            f.write('route delete %s "${OLDGW}"\n' % ip_and_mask)

    print("Generate ip-up and ip-down in /etc/ppp folder.")


def match_ip(ip: str):
    ip_item = ip.split("/")
    if len(ip_item[0].split(".")) == 4 and len(ip_item[1]) == 2 and ip_item[1].isdigit():
        return True
    else:
        return False


if __name__ == '__main__':

    if platform.system() != 'Darwin':
        print("Platform not support.")
        exit(1)

    generate_up_and_down()

    command = "chmod +x ip-up ip-down"
    subprocess.call(command, shell=True)
    command2 = "cp ip-up ip-down /etc/ppp"
    subprocess.call(command2, shell=True)
