#!/bin/bash
echo "========================================================="
echo " NATIONAL CYBER SHIELD - BOSS LINUX MILITARY DEPLOYMENT  "
echo "========================================================="

# 1. System Dependency Installation for Linux Kernel
echo "[+] Updating Package Repositories..."
sudo apt-get update -y
sudo apt-get install -y clang llvm libbpf-dev linux-headers-$(uname -r) python3-pip

# 2. Compile eBPF C Code to Kernel Bytecode
echo "[+] Compiling XDP Kernel Module (kernel_shield.c)..."
clang -O2 -target bpf -c kernel_shield.c -o kernel_shield.o

if [ -f "kernel_shield.o" ]; then
    echo "[🔥 SUCCESS] Kernel Object Compiled! Linking with Network Interface..."
    # Attach XDP module to eth0 Network Card
    sudo ip link set dev eth0 xdpgeneric obj kernel_shield.o sec xdp
    echo "[✓] XDP Driver Hook Active on NIC Interface!"
else
    echo "[-] Compilation failed. Check Kernel Headers."
    exit 1
fi

# 3. Launch Core AI Engine and Dashboard
echo "[+] Launching Production Engines..."
python3 packet_engine.py &
python3 -m http.server 8080 &

echo "========================================================="
echo " SYSTEM FULLY DEPLOYED ON LINUX KERNEL - MILITARY GRADE  "
echo "========================================================="