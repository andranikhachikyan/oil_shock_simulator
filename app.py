import streamlit as st
import matplotlib.pyplot as plt

from oil_shock_model import simulate_shock

st.title("Oil Shock Simulator")

st.markdown("""
### Key Variable Definitions:
- **Gas**: Change in gasoline prices  
- **Energy**: Energy-related inflation (fuel, electricity)  
- **CPI**: Overall inflation (headline inflation)  
- **GDP**: Economic growth rate  
""")

shock = st.slider("Oil Shock (%)", -50, 50, 20) / 100

baseline = simulate_shock(0)
shock_result = simulate_shock(shock)

st.subheader("Results (%)")

for k in baseline:
    st.write(f"{k}: {baseline[k]*100:.2f}% → {shock_result[k]*100:.2f}%")

# plot
labels = list(baseline.keys())

fig, ax = plt.subplots()
ax.bar(labels, baseline.values(), alpha=0.5, label="Baseline")
ax.bar(labels, shock_result.values(), alpha=0.5, label="Shock")
ax.legend()

st.subheader("Summary Insight")

gas_change = (shock_result["Gas"] - baseline["Gas"]) * 100
cpi_change = (shock_result["CPI"] - baseline["CPI"]) * 100

st.write(f"""
A {shock*100:.0f}% oil shock increases gasoline prices by approximately {gas_change:.2f}% 
and raises overall inflation by about {cpi_change:.2f}%.
""")

st.pyplot(fig)