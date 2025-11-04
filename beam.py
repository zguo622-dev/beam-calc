# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cantilever Beam Deflection", page_icon="👷‍♂️")

# ─────────────────────────────────────────────
# Header & intro
# ─────────────────────────────────────────────
st.title("👷‍♀️ Cantilever Beam Deflection Visualiser")
st.write(
    """
    Use the sliders in the **sidebar** to see how length **L**, tip load **P**,
    Young’s modulus **E** and second-moment of area **I** affect the deflection curve.
    """
)

# ─────────────────────────────────────────────
# Sidebar inputs
# ─────────────────────────────────────────────
st.sidebar.header("Input parameters")

L = st.sidebar.number_input("Beam length L  (m)",
                            min_value=0.5, max_value=20.0,
                            value=5.0, step=0.1, format="%.1f")

P = st.sidebar.number_input("Tip load P  (kN)",
                            min_value=1.0, max_value=2000.0,
                            value=50.0, step=1.0, format="%.1f")

E = st.sidebar.number_input("Young’s modulus E  (GPa)",
                            min_value=5.0, max_value=300.0,
                            value=210.0, step=1.0, format="%.1f")

I = st.sidebar.number_input("Moment of inertia I  (cm⁴)",
                            min_value=100.0, max_value=1_000_000.0,
                            value=50_000.0, step=100.0, format="%.0f")

# ─────────────────────────────────────────────
# Unit conversions
# ─────────────────────────────────────────────
P_N = P * 1e3       # kN → N
E_Pa = E * 1e9       # GPa → Pa
I_m4 = I * 1e-8      # cm⁴ → m⁴

# ─────────────────────────────────────────────
# Deflection analysis (closed-form formula)
# ─────────────────────────────────────────────
x = np.linspace(0, L, 400)                            # position along beam
y = (P_N * x**2) / (6 * E_Pa * I_m4) * (3*L - x)      # deflection (m)

δ_max = y[-1]               # tip deflection (m)
δ_allow = L / 250             # simple limit L/250 (m)

# ─────────────────────────────────────────────
# Metrics
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)
col1.metric("Max deflection δₘₐₓ", f"{δ_max*1000:.2f} mm")
col2.metric("Limit L/250", f"{δ_allow*1000:.2f} mm",
            delta=f"{(δ_max-δ_allow)*1000:+.2f} mm")

# ─────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────
fig, ax = plt.subplots()
ax.plot(x, y*1000)                 # y in mm
ax.set_xlabel("x  (m)")
ax.set_ylabel("Deflection  (mm)")
ax.set_title("Deflection curve")
ax.grid(True)
st.pyplot(fig)

# ─────────────────────────────────────────────
# Optional: download results
# ─────────────────────────────────────────────
df = pd.DataFrame({"x (m)": x, "deflection (mm)": y*1000})
csv = df.to_csv(index=False).encode()
st.download_button("Download CSV", csv, "deflection.csv", "text/csv")
