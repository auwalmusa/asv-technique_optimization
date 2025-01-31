import streamlit as st
import pandas as pd

# Streamlit app title and description
st.title("Electrochemical Technique Optimization for Heavy Metal Sensing")
st.write("Upload experimental results and optimize parameters for voltammetric detection.")

# Upload file section
uploaded_file = st.file_uploader("Upload a CSV or Excel file with experimental results", type=["csv", "xlsx"])

# Display sample data if uploaded
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(data.head())
    except Exception as e:
        st.error("Error loading file. Please check the format.")
        st.write(e)

# Analysis settings section
st.header("Technique Optimization Settings")

# Select heavy metal target
metal_target = st.selectbox("Select Heavy Metal Ion", ["Lead (Pb²⁺)", "Cadmium (Cd²⁺)", "Mercury (Hg²⁺)", "Arsenic (As³⁺)"])

# Select electrochemical technique
st.subheader("Electrochemical Technique")
technique = st.selectbox(
    "Choose Detection Technique",
    ["Cyclic Voltammetry (CV)", "Anodic Stripping Voltammetry (ASV)", "Differential Pulse Voltammetry (DPV)", "Square Wave Voltammetry (SWV)", "Linear Sweep Voltammetry (LSV)"]
)

# Optimize technique parameters
st.subheader("Optimization Parameters")

# Deposition potential and time (for ASV)
if technique in ["ASV", "DPV", "SWV"]:
    deposition_potential = st.number_input("Deposition Potential (V)", min_value=-2.0, max_value=0.0, value=-1.2, step=0.1)
    deposition_time = st.number_input("Deposition Time (seconds)", min_value=10, max_value=300, value=60, step=10)

# Scan rate (for CV and LSV)
if technique in ["CV", "LSV"]:
    scan_rate = st.number_input("Scan Rate (mV/s)", min_value=5, max_value=200, value=50, step=5)

# Frequency and amplitude (for SWV and DPV)
if technique in ["SWV", "DPV"]:
    pulse_amplitude = st.number_input("Pulse Amplitude (mV)", min_value=10, max_value=200, value=50, step=5)
    pulse_width = st.number_input("Pulse Width (ms)", min_value=1, max_value=50, value=10, step=1)

# Initialize session state for technique optimization results
if "technique_optimization" not in st.session_state:
    st.session_state.technique_optimization = []

# Add technique conditions to session state
with st.form("technique_form"):
    add_technique = st.form_submit_button("Add Optimized Technique Parameters")
    
    if add_technique:
        optimization_entry = {
            "Metal Ion": metal_target,
            "Technique": technique,
            "Deposition Potential (V)": deposition_potential if technique in ["ASV", "DPV", "SWV"] else "N/A",
            "Deposition Time (s)": deposition_time if technique in ["ASV", "DPV", "SWV"] else "N/A",
            "Scan Rate (mV/s)": scan_rate if technique in ["CV", "LSV"] else "N/A",
            "Pulse Amplitude (mV)": pulse_amplitude if technique in ["SWV", "DPV"] else "N/A",
            "Pulse Width (ms)": pulse_width if technique in ["SWV", "DPV"] else "N/A"
        }
        st.session_state.technique_optimization.append(optimization_entry)
        st.success("Technique parameters added successfully!")

# Display optimized technique results
st.write("Optimized Technique Parameters:")
technique_df = pd.DataFrame(st.session_state.technique_optimization)
st.dataframe(technique_df)

# Download results
if not technique_df.empty:
    csv = technique_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Optimized Technique Data", data=csv, file_name="technique_optimization.csv", mime="text/csv")

# Submit button for final query
if st.button("Submit Optimization Query"):
    st.success("Optimization query submitted with the following settings:")
    st.write("Selected Metal Ion:", metal_target)
    st.write("Technique:", technique)
    if technique in ["ASV", "DPV", "SWV"]:
        st.write("Deposition Potential (V):", deposition_potential)
        st.write("Deposition Time (s):", deposition_time)
    if technique in ["CV", "LSV"]:
        st.write("Scan Rate (mV/s):", scan_rate)
    if technique in ["SWV", "DPV"]:
        st.write("Pulse Amplitude (mV):", pulse_amplitude)
        st.write("Pulse Width (ms):", pulse_width)

