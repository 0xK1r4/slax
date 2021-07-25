#!/usr/bin/env python3
from colorama import *
print ("\33[21m"+Fore.RED+'slax 3.2'+Fore.RESET+" by Cheat, ['type help for command list']\33[0m\n")
import time
import threading
import socket
import sys
import os
import subprocess
import ipaddress
import binascii
import platform
from datetime import datetime
import psutil
import readline
from tabulate import *

discoverx='normal'
name=socket.gethostname()
host=socket.gethostbyname(name)

try:
    iface=sys.argv[1]
    prompt='wlan0 > '
except:
    iface='wlan0'
    prompt=Back.YELLOW+Fore.BLACK+'condorslax'+Fore.RESET+Back.RESET+Fore.RED+' » '+Fore.RESET
    
data_ready = threading.Event()
kill_flag = threading.Event()
class MyCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options
                                    if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try:
            return self.matches[state]
        except IndexError:
            return None

completer = MyCompleter(["net.discover","quit","dump","connect", "port","help","net.info","net.show","show.mac","net.arpscan"])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')




def keyboard_poller():
    global key_pressed
    global discoverx

    loop = True

    while loop:
        time.sleep(0.1)

        if kill_flag.isSet():
            loop = False


        now = datetime.now()

        #config
        new='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '
        inf='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.YELLOW+'INF'+Fore.RESET+'] '
        #prompt=Fore.BLUE+'[connection]'+Fore.RESET+'# '

        error='['+Fore.RED+'ERROR'+Fore.RESET+'] '
        message='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'MSG'+Fore.RESET+']'

        ch=input(prompt)
        connect=ch[:7]
        port=ch[:4]
        if ch=='discover on':
           discoverx='on'

        dump=ch[:4]
        if ch=='discover off':
           print (inf+'stopping discover..')
           discoverx='off'

        if dump == 'dump':
           d=ch[5:]
           print ('\r'+new+f"dumping data '{d}'")
           x=open('.dump','w')
           x.write(d)
           x.close()
           sys.stdout.write('\r'+new+'\r')

           os.system('hexdump .dump > dumped')
           dum=open('dumped','r')
           dumped=dum.read()
           dum.close()
           dumpedx={"dumped": [dumped]}
           print('\r'+tabulate(dumpedx, headers='keys', tablefmt='grid')+'                ')
           os.system('rm .dump')
           os.system('rm dumped')
           print ('\r'+new+'dumped terminated\r')
           if discoverx=='on':
              pass
           else:
              pass
        if port=='port':
           fport=ch[5:]
           print (inf+'Port set =',fport)
        if connect == 'connect':
           targetx=ch[8:]
           target=targetx[:12]
           targetprompt=Fore.BLUE+'['+target+']'+Fore.RESET+'# '

           print ('\r'+inf+'attemping to connect')
           s=socket.socket()
           sys.stdout.write('\r'+prompt)
           try:
               s.connect((target,int(fport)))
               print ('\r'+new+'connected')

               while True:
                 c=s.recv(2049).decode()
                 print ('\r'+message+' '+c+'                             ')
                 sys.stdout.write('\r'+prompt)
           except:
                 print (error+'failed to connect')
        if ch=='help':
           print ('slax tool help modules')
           print ('normal modules:')
           print (f"""  {Fore.RED}dump {Fore.RESET}      - dump packed form to hex
  {Fore.RED}port {Fore.RESET}      - set port to connect
  {Fore.RED}quit {Fore.RESET}      - exit
  {Fore.RED}show.mac {Fore.RESET}  - show mac database{Fore.RESET}
  {Fore.RED}connect {Fore.RESET}   - connect to host
  {Fore.RED}show.ip {Fore.RESET}   - show ip database
  {Fore.RED}clear.data {Fore.RESET}- clear database""")

           print ('net modules:')
           print (f"""  {Fore.RED}net.discover {Fore.RESET}- scan net by icmp
  {Fore.RED}net.show {Fore.RESET}    - net info in table
  {Fore.RED}net.info {Fore.RESET}    - info of net
  {Fore.RED}net.arpscan {Fore.RESET} - scan mac devices""")

        if ch=='show.mac':
           macd=open('.scan','r')
           macf=macd.read()
           macd.close()
           ifaced=open('.scan2','r')
           ifacef=ifaced.read()
           ifaced.close()
           datamac={"mac-address": [macf], "mac-iface": [ifacef]}
           print('\r'+tabulate(datamac, headers='keys', tablefmt='fancy_grid')+'                ')
        if ch=='show.ip':
           ipc=open('.discover','r')
           ipf=ipc.read()
           ipc.close()
           pckc=open('.pck','r')
           pckf=pckc.read()
           pckc.close()
           dataip={"ip-address": [ipf], "packed-form": [pckf]}
           print('\r'+tabulate(dataip, headers='keys', tablefmt='fancy_grid')+'                ')
        if ch=='clear.data':
           os.system('rm .scan')
           os.system('rm .discover')
           os.system('rm .pck')
           os.system('rm .scan2')
           os.system('touch .scan')
           os.system('touch .discover')
           os.system('touch .pck')
           os.system('touch .scan2')
           print (inf+'sucessful! ')

        if ch:
            key_pressed = ch
            data_ready.set()


def scan():
    now = datetime.now()
    new='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '
    inf='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.YELLOW+'INF'+Fore.RESET+'] '
    error='['+Fore.RED+'ERROR'+Fore.RESET+'] '
    message='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'MSG'+Fore.RESET+']'


    ip = '192.168.0.1'
    ipDividida = ip.split('.')

    try:
        red = ipDividida[0]+'.'+ipDividida[1]+'.'+ipDividida[2]+'.'
        comienzo = 1
        fin = 20
    except:
        print("[!] Error")
        sys.exit(1)


    if (platform.system()=="Windows"):
        ping = "ping -n 1"
    else :
        ping = "ping -c 1"

    tiempoInicio = datetime.now()
    print (inf+'mode discover is running')
    for subred in range(comienzo, fin+1):


        direccion = red+str(subred)
        response = os.popen(ping+" -b "+direccion)
        for line in response.readlines():
             if ("ttl" in line.lower()):
                 ADDRESSES = [
                   direccion,
                 ]
                 for ip in ADDRESSES:
                     if discoverx=='off':
                        main()

                     addr = ipaddress.ip_address(ip)
                     time.sleep(0.1)
                     now=datetime.now()
                     discover=open('.discover','a')
                     discover.write('\n'+direccion)
                     discover.close()
                     packed=open('.pck','a+')
                     packed.write(binascii.hexlify(addr.packed).decode()+'\n')
                     packed.close()
                     print ('\r'+'['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '+'Device '+Fore.RED+direccion+Fore.RESET,binascii.hexlify(addr.packed).decode())
                     sys.stdout.write('\r'+prompt)
                     break



    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio

def info():
    now=datetime.now()
    new='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '
    inf='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.YELLOW+'INF'+Fore.RESET+'] '

    print (inf+'mode info is running')
    while True:
     now=datetime.now()
     aaa = subprocess.Popen('iwconfig '+iface+' | grep level', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
     inf = aaa.stderr.read()+aaa.stdout.read()
     slu = (inf[:49])
     signallvl = (slu[43:].decode())
     time.sleep(1)
     print ('\r'+'['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '+'power: '+signallvl)
     sys.stdout.write('\r'+prompt)

def show():
    time.sleep(1)
    nada=''
    aaa = subprocess.Popen('iwconfig '+iface+' | grep level', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    inf = aaa.stderr.read()+aaa.stdout.read()
    slu = (inf[:49])
    signallvl = (slu[43:].decode())
    power=Fore.GREEN+'-'+signallvl+Fore.RESET
    showtab={"power": [power], "net-iface": [iface]}
    print('\r'+tabulate(showtab, headers='keys', tablefmt='fancy_grid')+'                ')
    sys.stdout.write('\r'+prompt)

def scanmac():
    now=datetime.now()

    new='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '

    ip = '192.168.0.1'
    ipDividida = ip.split('.')

    try:
        red = ipDividida[0]+'.'+ipDividida[1]+'.'+ipDividida[2]+'.'
        comienzo = 1
        fin = 20
    except:
        print("[!] Error")
        sys.exit(1)


    if (platform.system()=="Windows"):
        ping = "ping -n 1"
    else :
        ping = "ping -c 1"





    tiempoInicio = datetime.now()
    for subred in range(comienzo, fin+1):

        try:
            direccion = red+str(subred)

            response = os.popen('arp -a '+direccion)
            for line in response.readlines():
                if ("[ether]" in line.lower()):

                   aaa = subprocess.Popen('arp -a '+direccion, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                   mac = aaa.stderr.read()+aaa.stdout.read()

                   mac2 = mac[19:].decode()
                   mcv=mac2[:18].replace(' ','')
                   iface=mac2[29:].replace(' ','').replace('\n','')
                   a=open('.scan','a')
                   a.write('\n'+mcv)
                   a.close()
                   w=open('.scan2','a')
                   d=w.write('\n'+iface)
                   w.close()

                   if mcv=='no match found.\n':
                      break
                   print ('\r'+new+'Device '+str(mcv)+' on '+iface+'                              ')
                   sys.stdout.write('\r'+prompt)
                   break

        except:
            print ('stopped')


    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio

def main():
    curr_millis = time.time() * 1000
    prev_millis = curr_millis

    poller = threading.Thread(target=keyboard_poller)
    poller.start()

    loop = True


    while loop:
        now = datetime.now()
        error='['+Fore.RED+'ERROR'+Fore.RESET+'] '
        message='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'MSG'+Fore.RESET+']'
        new='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.GREEN+'NEW'+Fore.RESET+'] '
        inf='['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'] '+'['+Fore.YELLOW+'INF'+Fore.RESET+'] '

        curr_millis = time.time() * 1000
        if (curr_millis - prev_millis) >=1000:

            prev_millis = curr_millis
            # Do some extra stuff here

        if data_ready.isSet():
            if key_pressed.lower() == "quit":
                kill_flag.set()
                loop = False
                exit()
            else:
                pass

        if data_ready.isSet():
            dump=key_pressed.lower()[:4]
            connect=key_pressed.lower()[:7]
            port=key_pressed.lower()[:4]
            if key_pressed.lower() == "net.discover":
                scan()
            if key_pressed.lower() == 'net.info':
                info()
            if key_pressed.lower() == 'net.show':
                show()
            if key_pressed.lower() == 'net.arpscan':
                scanmac()

            data_ready.clear()
if __name__ == "__main__":
    main()
    exit()
    exit()
