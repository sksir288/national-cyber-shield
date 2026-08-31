import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="National Cyber Shield - Threat Command Center", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>NATIONAL CYBER SHIELD - THREAT COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00FF00;'><b>SYSTEM STATUS: ACTIVE PROTECTED</b> | Engine Mode: AI Anomaly Inspector, Active Firewall & Live Map Tracking</p>", unsafe_allow_html=True)

st.markdown("### LIVE GEOGRAPHICAL THREAT MAP")

# Sample coordinates mapping for demo/live attack representation based on logs
map_data = pd.DataFrame({
    'lat': [52.4126, 37.4220], # Brandenburg, Germany & Mountain View, US
    'lon': [12.5316, -122.0840],
    'threat': ['Brandenburg, Germany (Blocked)', 'Mountain View, US (Blocked)']
})

st.map(map_data, zoom=2)

st.markdown("### INTERCEPTED & BLOCKED THREAT LOGS")

log_file = "defence_attack_log.txt"
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        logs = f.readlines()
    for log in reversed(logs[-15:]): # Show last 15 logs
        st.markdown(f"<p style='color: #00FF00; font-family: monospace;'>{log.strip()}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #FFFF00;'>Waiting for live traffic injection logs...</p>", unsafe_allow_html=True)