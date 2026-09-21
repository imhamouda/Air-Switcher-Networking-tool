* AirSwitcher

AirSwitcher is a Linux command-line tool for 802.11 (Wi-Fi) frame capture and analysis. It puts a wireless interface into monitor mode and decodes management, control, and data frames in real time 
its on  v0.1-alpha — actively in development.

---

* ATTENTION:

- Air Switcher needs to kill some processes like NetworkManager, wpa_supplicant... in order to make a clear path for the monitor mode changing 
- AirSwitcher is built for **educational purposes and authorized security research only**.
- Capturing wireless traffic on networks you do not own or do not have **explicit permission** to test is illegal in most countries. I dont take any  responsibility for misuse of this tool. Only use it on your own network, in a lab environment, or with the written consent of the network owner.

---

* LIMITATIONS:

- 2.4 GHz only for now — no 5 GHz/6 GHz channel support yet
- Channel 13–14 legality varies by country; verify local regulations before use
- Tested primarily on interfaces using `ath9k`/`rtl` family drivers; other chipsets may behave differently
- No packet injection support 
- You cant write the sniffed packets in a .cap file (ill add that soon)

  * GOOD THINGS:
    
  - It has a user friendly 802.11 packet visualisation so even when you're a beginner you can understand it
  - All the management frames and control frames are defined by name , the data frames are not all defined but the DHCP , 4 ways handshake and some data types are absolutely defined 
  - it visualize the source BSSID and the distination BSSID
  - The sniffer program is made with c++ so fast sniffing with no delay
  - You can return your interface to managed mode with one click
    
    ## Installation
## 0. Install dependencies

### Debian / Ubunt (slopbuntu) / Linux Mint

```bash
sudo apt update
sudo apt install -y git cmake build-essential libpcap-dev libssl-dev python3 iw rfkill
```

### Arch Linux , i use arch btw 

```bash
sudo pacman -Syu
sudo pacman -S --needed git cmake base-devel libpcap openssl python iw rfkill
```

Wait dont panic haha these packages are important for my tool to work , well I think some of them are built in the kernel but we need to add them 

---

## 1. Clone libtins

### 1. Install libtins , if you have it skip to step 2

AirSwitcher relies on libtins for 802.11 frame parsing. Most distros don't package it, so build it from source:

```bash
git clone https://github.com/mfontanini/libtins.git
cd libtins
mkdir build && cd build
cmake ../ -DLIBTINS_ENABLE_CXX11=1
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 2. Clone AirSwitcher

```bash
git clone https://github.com/imhamouda/Air-Switcher-Networking-tool.git
cd Air-Switcher-Networking-tool
```

### 3. Build the ultra fast sniffer 

```bash
chmod +x build.sh
./build.sh
```

This compiles `src/sniffer.cpp` into `build/libsniffer-test.so`.

### 4. Run it by name

```bash
chmod +x src/main.py
sudo ln -s "$(pwd)/src/main.py" /usr/local/bin/airswitcher
```
