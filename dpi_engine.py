import re

class DeepPacketInspector:
    def __init__(self):
        # Military Grade Signature Definitions (Zero-Day & Advanced Vectors)
        self.signatures = {
            "SQL_INJECTION": re.compile(r"('|\"|--|UNION|SELECT|DROP|INSERT)", re.IGNORECASE),
            "COMMAND_INJECTION": re.compile(r"(;|\|\||&&|/bin/sh|/bin/bash|cmd\.exe|powershell)", re.IGNORECASE),
            "BUFFER_OVERFLOW": re.compile(r"(\x90{10,}|A{50,})"), # NOP Sleds / Shellcode padding
            "XSS_EXPLOIT": re.compile(r"(<script>|javascript:|onerror=)", re.IGNORECASE)
        }

    def inspect_payload(self, raw_payload):
        if not raw_payload:
            return "CLEAN", None
            
        for threat_type, pattern in self.signatures.items():
            if pattern.search(raw_payload):
                return "CRITICAL_PAYLOAD_THREAT", threat_type
                
        return "CLEAN", None

if __name__ == "__main__":
    dpi = DeepPacketInspector()
    test_payload = "GET /index.php?id=1' UNION SELECT NULL, username, password FROM users--"
    status, threat = dpi.inspect_payload(test_payload)
    print(f"[✓] DPI Inspection Result: Status = {status} | Threat Identified = {threat}")