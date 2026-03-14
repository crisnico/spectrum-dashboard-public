import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Spectrum | Structural AI Resilience",
    page_icon="🛡️",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🛡️ Spectrum: Structural AI Resilience Dashboard")
st.write("Quantitative analysis of **Laminar (Safe)** vs. **Plastic (Yielding)** states in LLM Architectures.")

st.divider()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Adversarial Control")
    
    load = st.slider(
        "Adversarial Load (A)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.945, 
        step=0.001,
        help="Simulated stress applied to the model's safety baffles."
    )
    
    st.write("---")
    st.caption("Technical Diagnostic Tool")

# --- CORE LOGIC (Simulated Engine) ---
def calculate_resilience(A):
    # Constants for current simulation
    L = 154.5  
    sigma = 1.05 
    R_crit = 194.7 
    val = L / (max(A, 0.001) * sigma)
    return max(val, 147.1), R_crit

r_value, r_crit = calculate_resilience(load)

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("Real-Time Diagnostics")
    
    if r_value > r_crit:
        status = "🟢 LAMINAR (ELASTIC)"
        color = "normal"
        st.success(status)
    else:
        status = "🔴 PLASTIC DEFORMATION"
        color = "inverse"
        st.error(status)
        st.warning("⚠️ WARNING: Yield point exceeded. Structural integrity compromised.")

    st.metric(
        label="Resistance (R)", 
        value=f"{r_value:.2f}", 
        delta=f"{r_value - r_crit:.2f} vs Yield",
        delta_color=color
    )
    
    st.write(f"**Current Load:** {load*100:.1f}% Stress")
    st.write(f"**Yield Point (R_crit):** {r_crit}")

with col2:
    st.subheader("Stress-Strain Visualization")
    
    load_range = [i/100 for i in range(80, 101)]
    res_range = [calculate_resilience(l)[0] for l in load_range]
    
    df = pd.DataFrame({'Load': load_range, 'Resistance': res_range})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Load'], y=df['Resistance'], 
        mode='lines+markers', 
        name='Decay Curve',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.add_hline(y=r_crit, line_dash="dash", line_color="red", annotation_text="Yield Point")
    
    fig.update_layout(
        xaxis_title="Adversarial Load (A)",
        yaxis_title="Resistance (R)",
        margin=dict(l=0, r=0, t=30, b=0),
        height=400,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.caption("© 2026 Spectrum Infosec | Proprietary Technical Analysis. Confidential Logic Protected.")
