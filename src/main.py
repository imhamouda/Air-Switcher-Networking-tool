#!/usr/bin/env python3
import subprocess
import os 
import ctypes
import threading
import time
import shutil
Solution = True
color_azrag = "\033[34m"
color_akhthar = "\033[92m"
color_idk = "\033[93m"
color_red = "\033[91m"
normal = "\033[0m"
peak = r"""
   _____  .__        _________       .__  __         .__                  
  /  _  \ |__|______/   _____/_  _  _|__|/  |_  ____ |  |__   ___________ 
 /  /_\  \|  \_  __ \_____  \\ \/ \/ /  \   __\/ ___\|  |  \_/ __ \_  __ \
/    |    \  ||  | \/        \\     /|  ||  | \  \___|   Y  \  ___/|  | \/
\____|__  /__||__| /_______  / \/\_/ |__||__|  \___  >___|  /\___  >__|   
        \/                 \/                      \/     \/     \/       
        """
def print_banner():
    terminal_width = shutil.get_terminal_size().columns
    print(color_azrag, end="")
    for line in peak.splitlines():
        print(line.center(terminal_width))
    print(normal, end="")

def main():
    is_running = True
    while is_running:
        subprocess.run(["clear"])
        print(f"{color_akhthar}--- WELCOME ---{normal}".center(125))
        print(f"{color_idk}Welcome to AirSwitcher v0.1-alpha{normal}")
        print_banner()
        range1 = 0
        ready_to_go = []
        range_of_interfaces = []
        wireless_interfaces = []
        directory = "/sys/class/net"
        for iface in os.listdir(directory):  
            if os.path.exists(os.path.join(directory , iface , "wireless")):
                wireless_interfaces.append(iface)
                range1+=1
                range_of_interfaces.append(range1)
                strings = [str(n)  for n in range_of_interfaces]
                ready = strings[wireless_interfaces.index(iface)] + "." + " " + iface
                ready_to_go.append(ready)
        
        result = " \n ".join(ready_to_go) 
        print(f"{color_akhthar}Choose a wireless interface to work with:{normal}")
        print(f"{color_azrag}------------{normal}")
        print(f"[*] Detected wireless interfaces:\n {result}\n")
        try:
            Choice = int(input("> "))
            interface = wireless_interfaces[Choice - 1]
            subprocess.run(["clear"])
            print(f"{color_akhthar}--- Main menu ---{normal}\n".center(125))
            print(f"{color_akhthar}Select an option:{normal}")
            print(f"{color_azrag}------------{normal}")
            print("0. Select another interface")
            print("1. Put interface in monitor mode")
            print("2. Put interface in managed mode")
            print(f"{color_azrag}------------{normal}")
            try:
                Choice2 = int(input("> "))
                if Choice2 == 0:
                    interface = None
                    continue
                elif Choice2 == 1:
                    subprocess.run(["clear"])
                    print(f"{color_akhthar}--- Work section ---{normal}\n".center(125))
                    print(killing_proc())
                    print(monitor_mode(interface))
                    print(f"{color_azrag}------------{normal}")
                    print(f"{color_akhthar}Select an option:{normal}")
                    print(f"{color_azrag}------------{normal}")
                    print("1. 802.11 (Wi-Fi) sniffing (Beta)")
                    print(f"{color_azrag}------------{normal}")
                    Choice3 = int(input("> "))
                    try:
                        if Choice3 == 1:
                            subprocess.run(["clear"])
                            print(f"{color_idk}You can select one channel (1-14) , with denying it will switch to channel hopping mode{normal}")
                            Choice4 = input("Channel (Press 'n' to deny): ")
                            if Choice4.upper() == "N":
                                subprocess.run(["clear"])
                                sniff_until_stopped(interface)
                                is_running = False
                            elif 1<= int(Choice4) <=14:
                                global Solution
                                Solution = False
                                channel_specifier(Choice4 , interface)
                                sniff_until_stopped(interface)
                                is_running = False
                            elif int(Choice4) < 0 or int(Choice4) > 14:
                                print(f"[-] Bro ")

                        else:
                             print(f"{color_red}[-] Well , we dont have another option like option {Choice2} {normal}\n")
                             input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
                             continue

                    except ValueError:
                         print(f"{color_red}[-] Type your option's number{normal}\n")
                         input(f"{color_akhthar}[+] Press Enter to continue...{normal}")

                elif Choice2 == 2:
                    print(managed_mode(interface))
                    print(f"{color_akhthar}[+] Auto exiting...{normal}")
                    is_running = False
                else:
                    print(f"{color_red}[-] Well we dont have another option like option {Choice2} {normal}\n")
                    input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
                    continue
            except ValueError:
                        print(f"{color_red}[-] Type your option's number\n{normal}")
                        input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
        except IndexError:
            print(f"{color_red}[-] You dont have {Choice} wireless interfaces , try again{normal}\n")
            input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
        except KeyboardInterrupt:
            print(f"\n{color_akhthar}[+] Exiting AirSwitcher v0.1-alpha script...{normal}\n")
            is_running = False
            return
        except ValueError:
            print(f"{color_red}[-] Type your wireless card number\n{normal}")
            input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
        except EOFError:
            print(f"\n{color_akhthar}[+] Exiting AirSwitcher v0.1-alpha script...{normal}\n")
            is_running = False
        except OSError:
            print(f"{color_red}[-] Path error , go check path for libsniffer-test.so , it should be in /Air-Switcher/build{normal}")
            input(f"{color_akhthar}[+] Press Enter to continue...{normal}")
          
        
def killing_proc():
    processes = ["NetworkManager" , "wpa_supplicant" , "dhclient" , "avahi-deamon" , "dhcpcd" , "systemd-network"] 
    for proc in processes:
        subprocess.run(["sudo" , "killall" , proc] ,
        stdout = subprocess.DEVNULL , 
        stderr = subprocess.DEVNULL )
    return f"{color_akhthar}[+] Finished killing processes{normal}\n"

def monitor_mode(interface):
    subprocess.run(["sudo" , "ip" , "link" , "set" , interface , "down"] , check=True)
    subprocess.run(["sudo" , "iw", "dev" , interface , "set" , "type" , "monitor"] , check=True) 
    subprocess.run(["sudo" , "ip" , "link" , "set" , interface , "up"], check=True)
    return f"{color_akhthar}[+] {interface} set to monitor mode\n{normal}"

def managed_mode(interface):
    processes = ["NetworkManager" , "wpa_supplicant" , "avahi-daemon" , "systemd-networkd"]
    subprocess.run(["sudo" , "ip" , "link" , "set" , interface , "down"] , check=True)
    subprocess.run(["sudo" , "iw" , "dev" , interface , "set" , "type" , "managed"] , check=True)
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
    for proc in processes:
        subprocess.run(["sudo" , "systemctl" , "start" , proc])
    return f"{color_akhthar}[+] {interface} set to managed mode{normal}"

def channel_hopper_ahhhh(interface , stop_event):
    channel = 1
    global Solution
    while Solution:
        while not stop_event.is_set():
            subprocess.run(
                ["sudo" , "-n" , "iw" , "dev" , interface , "set" , "channel" , str(channel)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1
            )
            channel += 1
            if channel > 12:
                channel = 1
            time.sleep(0.3)

def channel_specifier(channel , interface):
    subprocess.run(["sudo" , "-n" , "iw" , "dev" , interface , "set" , "channel" , str(channel)],
               stdout=subprocess.DEVNULL, 
               stderr=subprocess.DEVNULL
               )



_lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "build", "libsniffer-test.so")
_lib = ctypes.CDLL(_lib_path)

_lib.sniffing.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
_lib.sniffing.restype = ctypes.c_int

_lib.stop_capture.argtypes = []
_lib.stop_capture.restype = None

def sniff_until_stopped(interface: str):
    total_packets = ctypes.c_int(0)
    stop_event = threading.Event()

    capture_thread = threading.Thread(
        target=_lib.sniffing,
        args=(interface.encode("utf-8"), ctypes.byref(total_packets)),
    )
    capture_thread.start()
    hopper_thread_nigga = threading.Thread(
        target=channel_hopper_ahhhh , 
        args=(interface , stop_event), 
    )
    hopper_thread_nigga.start()

    try:
        input("Capturing... press Enter to stop\n")
    except KeyboardInterrupt:
        print()
    stop_event.set()
    _lib.stop_capture()
    capture_thread.join()
    hopper_thread_nigga.join(timeout = 2)

    print(f"{color_akhthar}[+] Captured {total_packets.value} packets{normal}")
if __name__ == "__main__":
     main()
