import streamlit as st
import matplotlib.pyplot as plt
from oil_shock_model import simulate_shock

# config 
st.set_page_config(page_title="Oil Shock Simulator", layout="wide")

# title and desc 
st.title("Oil Shock Simulator")

st.markdown("""
Simulate how changes in oil prices propagate through the economy.

This model captures the short-term chain:
**Oil → Gas → Energy Inflation → CPI → GDP**
""")

# Sidebar
st.sidebar.header("Simulation Controls")

shock = st.sidebar.slider(
    "Oil Shock (%)",
    -100, 100, 20,
    help="Percentage change in oil prices"
) / 100

st.sidebar.markdown("""
### What this does:
Adjust the oil shock to see how it impacts:
- Gas prices  
- Energy inflation  
- Overall inflation (CPI)  
- GDP growth  
""")

# runs model
baseline = simulate_shock(0)
shock_result = simulate_shock(shock)

# top display metrics
st.subheader("Key Results")

col1, col2, col3, col4 = st.columns(4)

labels = ["Gas", "Energy", "CPI", "GDP"]

for col, key in zip([col1, col2, col3, col4], labels):
    change = (shock_result[key] - baseline[key]) * 100
    col.metric(
        label=key,
        value=f"{shock_result[key]*100:.2f}%",
        delta=f"{change:.2f}%"
    )

# diff plot 
st.subheader("Baseline vs Shock Comparison")

fig, ax = plt.subplots()

ax.bar(labels, [v*100 for v in baseline.values()], alpha=0.5, label="Baseline")
ax.bar(labels, [v*100 for v in shock_result.values()], alpha=0.5, label="Shock")

ax.set_ylabel("Change (%)")
ax.set_title("Impact of Oil Shock on Economic Indicators")
ax.legend()

st.pyplot(fig)

# interpretation
st.subheader("Interpretation")

gas_change = (shock_result["Gas"] - baseline["Gas"]) * 100
energy_change = (shock_result["Energy"] - baseline["Energy"]) * 100
cpi_change = (shock_result["CPI"] - baseline["CPI"]) * 100
gdp_change = (shock_result["GDP"] - baseline["GDP"]) * 100

st.markdown(f"""
A **{shock*100:.0f}% oil shock** leads to:

- **Gasoline prices** increasing by ~{gas_change:.2f}%
- **Energy inflation** increasing by ~{energy_change:.2f}%
- **Headline inflation (CPI)** increasing by ~{cpi_change:.2f}%
- **GDP growth** changing by ~{gdp_change:.2f}% *(low reliability)*

### Key Insight:
Oil shocks strongly impact inflation through energy prices, but their effect on GDP is weak and uncertain in the short term.
""")

# -----------------------
# EXPLANATIONS
# -----------------------
st.subheader("What These Metrics Mean")

st.markdown("""
- **Gas**: Change in gasoline prices  
- **Energy**: Inflation in energy-related goods (fuel, electricity)  
- **CPI (Headline Inflation)**: Overall price level in the economy  
- **GDP Growth**: Economic output growth rate  

---

### Important Notes:
- This model captures **short-term effects (~1-3 months)**  
- GDP results are less reliable due to missing variables  
- Relationships are **correlational, not causal**  
""")

# -----------------------
# ADVANCED NOTE (OPTIONAL FLEX)
# -----------------------
with st.expander("Model Details"):
    st.markdown("""
- Built using linear regression (statsmodels)  
- Sequential transmission model  
- Includes lagged economic relationships  
- Designed for interpretability, not forecasting  

---

### Limitations:
- Does not include interest rates, employment, or policy effects  
- Assumes linear relationships  
- GDP model has low explanatory power  
""")
