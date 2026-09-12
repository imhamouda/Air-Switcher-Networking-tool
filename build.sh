#!/bin/bash
mkdir -p build
g++ -std=c++14 -shared -fPIC -o build/libsniffer-test.so src/sniffer.cpp \
    -I/usr/local/include -L/usr/local/lib -ltins -lpcap
echo "[+] Build complete: build/libsniffer-test.so"
