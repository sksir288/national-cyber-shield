import numpy as np
from sklearn.ensemble import IsolationForest

class NetworkAnomalyAI:
    def __init__(self):
        # Features: [Packet Size (Bytes), Time Delta (ms), Request Rate (req/sec)]
        # Training baseline with standard network traffic vs threat vectors
        X_train = np.array([
            [64, 100, 10],   # Normal HTTP traffic
            [128, 200, 5],   # Normal HTTPS payload
            [1024, 1000, 1], # Normal File transfer
            [1500, 2, 500],  # DDoS Syn Flood / Burst anomaly
            [45, 1, 800],    # Port scanning signature
            [2048, 0.5, 900] # High-rate Malicious Payload Injection
        ])
        
        self.model = IsolationForest(contamination=0.3, random_state=42)
        self.model.fit(X_train)

    def predict_packet(self, packet_size, time_delta, req_rate):
        features = np.array([[packet_size, time_delta, req_rate]])
        prediction = self.model.predict(features)
        # -1 = Anomaly / Threat, 1 = Normal Traffic
        return "THREAT_ANOMALY" if prediction[0] == -1 else "CLEAN_TRAFFIC"

if __name__ == "__main__":
    ai = NetworkAnomalyAI()
    test_result = ai.predict_packet(1500, 1, 600)
    print(f"[✓] AI Anomaly Engine Decision: {test_result}")