import streamlit as st
import matplotlib.pyplot as plt
import time

# Streamlit Page Config
st.set_page_config(page_title="8-Cell Battery Dashboard", layout="wide")

# Battery cell profiles
BATTERY_PROFILES = {
    "Li-ion": {"capacity": 3000, "voltage": 3.7},
    "NiMH": {"capacity": 2000, "voltage": 1.2},
    "Lead-Acid": {"capacity": 5000, "voltage": 2.0}
}

NUM_CELLS = 8

# Initialize session state for each cell
for i in range(NUM_CELLS):
    if f"cell_{i}_level" not in st.session_state:
        st.session_state[f"cell_{i}_level"] = 50
    if f"cell_{i}_x" not in st.session_state:
        st.session_state[f"cell_{i}_x"] = []
    if f"cell_{i}_y" not in st.session_state:
        st.session_state[f"cell_{i}_y"] = []

# Sidebar controls
st.sidebar.title("🔧 Global Simulation Controls")
simulation_speed = st.sidebar.slider("⏱️ Speed (lower = faster)", 0.01, 0.5, 0.1)
run_sim = st.sidebar.checkbox("▶️ Run Simulation")

# Page Title
st.title("🔋 8-Cell Battery Charging/Discharging Dashboard")
st.caption("Each cell can be individually configured. The dashboard updates in real-time as cells charge or discharge.")

# Layout: 4 columns for 8 cells
cell_columns = st.columns(4)

for i in range(NUM_CELLS):
    col = cell_columns[i % 4]

    with col:
        st.markdown(f"### 🔌 Cell {i + 1}")

        battery_type = st.selectbox(
            f"Battery Type - Cell {i+1}",
            list(BATTERY_PROFILES.keys()),
            key=f"type_{i}"
        )

        mode = st.radio(
            f"Mode - Cell {i+1}",
            ["Charging", "Discharging"],
            key=f"mode_{i}",
            horizontal=True
        )

        # Get battery profile
        profile = BATTERY_PROFILES[battery_type]
        level_key = f"cell_{i}_level"
        level = st.session_state[level_key]

        # Run simulation logic
        if run_sim:
            if mode == "Charging" and level < 100:
                st.session_state[level_key] += 1
            elif mode == "Discharging" and level > 0:
                st.session_state[level_key] -= 1
            level = st.session_state[level_key]

            # Update plot data
            st.session_state[f"cell_{i}_x"].append(len(st.session_state[f"cell_{i}_x"]))
            st.session_state[f"cell_{i}_y"].append(level)

        # Battery level color
        if level > 75:
            color = "🟢"
        elif level > 35:
            color = "🟡"
        else:
            color = "🔴"

        st.markdown(f"**{color} Charge Level: {level}%**")
        st.progress(level / 100)

        # Plot battery charge
        fig, ax = plt.subplots(figsize=(3, 1.2))
        ax.plot(st.session_state[f"cell_{i}_x"], st.session_state[f"cell_{i}_y"],
                color='green' if mode == "Charging" else 'red')
        ax.set_ylim(0, 100)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#f9f9f9")
        fig.patch.set_alpha(0)
        st.pyplot(fig)

        st.markdown(f"**Voltage**: `{profile['voltage']} V`  |  **Capacity**: `{profile['capacity']} mAh`")
        import pandas as pd
import io

# Button in the sidebar to download CSV
st.sidebar.markdown("---")
st.sidebar.title("📤 Export Data")
if st.sidebar.button("Download CSV"):
    # Gather data from session_state
    rows = []
    for i in range(NUM_CELLS):
        times = st.session_state[f"cell_{i}_x"]
        levels = st.session_state[f"cell_{i}_y"]
        battery_type = st.session_state.get(f"type_{i}", "Unknown")
        mode = st.session_state.get(f"mode_{i}", "Unknown")
        profile = BATTERY_PROFILES.get(battery_type, {"voltage": None, "capacity": None})
        for t, level in zip(times, levels):
            rows.append({
                "Cell": i + 1,
                "Time Step": t,
                "Charge Level (%)": level,
                "Battery Type": battery_type,
                "Mode": mode,
                "Voltage (V)": profile["voltage"],
                "Capacity (mAh)": profile["capacity"]
            })

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Convert to CSV buffer
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Download button
    st.download_button(
        label="📥 Download Simulation CSV",
        data=csv_buffer.getvalue_
    )



