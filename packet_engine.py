import socket
import time
import sys
import os
import subprocess
from collections import defaultdict
from geo_engine import OfflineGeoIP
from ml_detector import NetworkAnomalyAI
from dpi_engine import DeepPacketInspector

print("==================================================")
print(" NATIONAL CYBER SHIELD - MILITARY DEFENSE ENGINE  ")
print("==================================================")

# Initialize All Core Defense Engines
geo_resolver = OfflineGeoIP()
ai_engine = NetworkAnomalyAI()
dpi_inspector = DeepPacketInspector()

blocked_ips = set()
packet_tracker = defaultdict(list)

MAX_PACKETS = 2
TIME_WINDOW = 3

def block_ip_firewall(ip_address):
    if ip_address in ("127.0.0.1", "localhost") or ip_address.startswith("10."):
        print(f"[🛡️ SHIELD ACTION] Internal Loopback IP noted. Skipping Firewall Rule.")
        return

    if ip_address in blocked_ips:
        print(f"[🛡️ SHIELD ACTION] IP {ip_address} is already neutralized.")
        return

    blocked_ips.add(ip_address)
    rule_name = f"CYBER_SHIELD_BLOCK_{ip_address.replace('.', '_')}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip_address}'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[🔥 FIREWALL ENFORCED] Successfully blocked IP {ip_address} on OS Firewall!")
        else:
            print(f"[⚠️ FIREWALL NOTE] Run CMD as Administrator to enforce OS-level rules.")
    except Exception as e:
        print(f"[-] Firewall execution error: {e}")

def check_rate_limit(ip_address):
    current_time = time.time()
    packet_tracker[ip_address].append(current_time)
    packet_tracker[ip_address] = [t for t in packet_tracker[ip_address] if current_time - t <= TIME_WINDOW]
    
    if len(packet_tracker[ip_address]) >= MAX_PACKETS:
        return True
    return False

def start_engine():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 9999))
    server.listen(5)
    
    print(f"[+] Military Engine Active: DPI + AI + Offline GeoIP on Port 9999...\n")
    
    last_packet_time = time.time()
    
    try:
        while True:
            client_sock, client_addr = server.accept()
            recv_time = time.time()
            data = client_sock.recv(1024).decode(errors='ignore')
            
            packet_size = len(data)
            time_delta = max((recv_time - last_packet_time) * 1000, 0.1)
            req_rate = 1000 / time_delta if time_delta > 0 else 1000
            last_packet_time = recv_time
            
            threat_ip = client_addr[0]
            if "THREAT_IP:" in data:
                threat_ip = data.split("THREAT_IP:")[1]

            # 1. Deep Packet Inspection (DPI)
            dpi_status, threat_type = dpi_inspector.inspect_payload(data)

            # 2. AI Machine Learning Inspection
            ai_decision = ai_engine.predict_packet(packet_size, time_delta, req_rate)
            
            # 3. Rate Limiting Check
            is_dos = check_rate_limit(threat_ip)

            print(f"\n[📡 TRAFFIC INTERCEPTED] Source: {threat_ip} | Size: {packet_size} Bytes")
            print(f"[🤖 AI DECISION] {ai_decision} | [🔍 DPI SCAN] {dpi_status}")
            
            if dpi_status == "CRITICAL_PAYLOAD_THREAT" or ai_decision == "THREAT_ANOMALY" or is_dos:
                geo_info = geo_resolver.resolve_ip(threat_ip)
                
                print("\n" + "="*55)
                print(f"[🚨 THREAT NEUTRALIZED!] IP: {threat_ip}")
                print(f" TRIGGER   : DPI Threat [{threat_type}] / ML Anomaly")
                print(f" LOCATION  : {geo_info['city']}, {geo_info['country']}")
                print(f" NETWORK   : {geo_info['isp']}")
                print("="*55)
                
                block_ip_firewall(threat_ip)
                
                with open("defence_attack_log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] IP: {threat_ip} | Location: {geo_info['city']}, {geo_info['country']} | DPI Threat: {threat_type} | Action: BLOCKED\n")
            
            client_sock.close()
    except KeyboardInterrupt:
        print("\n[-] Shield Engine Stopped Safely.")
        sys.exit()

if __name__ == "__main__":
    start_engine()