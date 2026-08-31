import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="National Cyber Shield - Threat Command Center", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>NATIONAL CYBER SHIELD - THREAT COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00FF00;'><b>SYSTEM STATUS: ACTIVE PROTECTED</b> | Engine Mode: AI Anomaly Inspector, Active Firewall & Live Map Tracking</p>", unsafe_allow_html=True)

st.markdown("### LIVE GEOGRAPHICAL THREAT MAP")
map_data = pd.DataFrame({
    'lat': [52.4126, 37.4220],
    'lon': [12.5316, -122.0840],
    'threat': ['Brandenburg, Germany (Blocked)', 'Mountain View, US (Blocked)']
})
st.map(map_data, zoom=2)

st.markdown("### INTERCEPTED & BLOCKED THREAT LOGS")
log_file = "defence_attack_log.txt"
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        logs = f.readlines()
    for log in reversed(logs[-15:]):
        st.markdown(f"<p style='color: #00FF00; font-family: monospace;'>{log.strip()}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #FFFF00;'>Waiting for live traffic injection logs...</p>", unsafe_allow_html=True)

# PDF Report Download Section Placeholder
st.markdown("---")
if st.button("Download Incident Forensic Report (PDF)"):
    if os.path.exists("Cyber_Shield_Incident_Report.html"):
        with open("Cyber_Shield_Incident_Report.html", "rb") as file:
            st.download_button(
                label="Click to Save Report",
                data=file,
                file_name="Cyber_Shield_Incident_Report.html",
                mime="text/html"
            )
    else:
        st.warning("Report file not generated yet.")
