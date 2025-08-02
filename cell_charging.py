import streamlit as st
import pandas as pd
import random
import time
import psutil
import numpy as np

# ------------------- ⚙️ Page Configuration -------------------
st.set_page_config(
    page_title="Battery Dashboard",
    page_icon="🔋",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🔋 Battery Cell Monitoring Dashboard</h1>
    <p style='text-align: center;'>Real-time simulated data with interactive controls and insights.</p>
""", unsafe_allow_html=True)

# ------------------- 🧪 Sidebar Configuration -------------------
def configure_sidebar():
    st.sidebar.header("🧪 Configure Cells")
    available_types = ["LFP", "NMC", "NCA", "LMO", "LTO", "NiMH", "Lead-Acid"]
    selected_cells = []

    for i in range(8):
        selected = st.sidebar.selectbox(
            f"Select type for Cell {i+1}",
            options=[""] + available_types,
            key=f"cell_{i}"
        )
        if selected:
            selected_cells.append(selected.lower())

    selected_cells = list(dict.fromkeys([c for c in selected_cells if c.strip() != ""]))
    return selected_cells

# ------------------- 🔋 Simulate Cell Data -------------------
def generate_cell_data(cell_selection):
    statuses = ["Charging", "Discharging", "Idle"]
    data = []
    for idx, cell_type in enumerate(cell_selection, start=1):
        voltage = 3.2 if cell_type == "lfp" else 3.6
        current = round(random.uniform(0.5, 5.0), 2)
        temp = round(random.uniform(25, 40), 1)
        capacity = round(voltage * current, 2)
        status = random.choice(statuses)

        data.append({
            "Cell ID": f"Cell_{idx}",
            "Type": cell_type.upper(),
            "🔋 Voltage (V)": voltage,
            "⚡ Current (A)": current,
            "🌡️ Temp (°C)": temp,
            "⚙️ Capacity (Wh)": capacity,
            "📶 Status": status
        })
    return pd.DataFrame(data)

# ------------------- 📊 Key Metrics -------------------
def show_metrics(df):
    st.markdown("## 📊 Key Metrics Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔋 Avg Voltage", f"{df['🔋 Voltage (V)'].mean():.2f} V")
    col2.metric("⚡ Avg Current", f"{df['⚡ Current (A)'].mean():.2f} A")
    col3.metric("🌡️ Avg Temp", f"{df['🌡️ Temp (°C)'].mean():.1f} °C")
    col4.metric("⚙️ Total Capacity", f"{df['⚙️ Capacity (Wh)'].sum():.2f} Wh")

# ------------------- 📋 Show Data Table -------------------
def show_data_table(df):
    st.markdown("## 📋 Detailed Cell Data")
    st.dataframe(df, use_container_width=True)

# ------------------- 📈 Charts -------------------
def show_charts(df):
    st.markdown("## 📈 Visual Insights")
    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("🌡️ Temperature by Cell")
        st.bar_chart(df.set_index("Cell ID")["🌡️ Temp (°C)"])

    with chart2:
        st.subheader("⚙️ Capacity Distribution")
        st.bar_chart(df.set_index("Cell ID")["⚙️ Capacity (Wh)"])

    st.subheader("📶 Status Count")
    status_counts = df["📶 Status"].value_counts()
    st.bar_chart(status_counts)

# ------------------- ⏱️ Real-time System Monitor -------------------
def show_system_info():
    st.markdown("## 🖥️ System Resource Usage")
    cpu, ram = st.columns(2)
    with cpu:
        st.metric("🧠 CPU Usage", f"{psutil.cpu_percent()} %")
    with ram:
        mem = psutil.virtual_memory()
        st.metric("📦 RAM Usage", f"{mem.percent} %")

# ------------------- 📉 Line Chart Simulation -------------------
def show_live_trends(df):
    st.subheader("📊 Real-Time Current Trend Simulation")
    chart_data = pd.DataFrame(
        {
            cell: np.random.normal(loc=df.loc[idx, "⚡ Current (A)"], scale=0.2, size=20)
            for idx, cell in enumerate(df["Cell ID"])
        }
    )
    st.line_chart(chart_data)

# ------------------- 📥 CSV Export -------------------
def download_csv(df):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="battery_cell_data.csv",
        mime="text/csv"
    )

# ------------------- 🚀 Main App Logic -------------------
def main():
    cell_selection = configure_sidebar()

    if st.sidebar.button("🚀 Generate Dashboard"):
        if not cell_selection:
            st.warning("⚠️ Please select at least one valid cell type.")
            return

        df = generate_cell_data(cell_selection)
        show_metrics(df)
        show_data_table(df)
        show_charts(df)
        show_live_trends(df)
        show_system_info()
        download_csv(df)
        st.success("✅ Dashboard generated successfully!")
    else:
        st.info("ℹ️ Select cell types from the sidebar and click 'Generate Dashboard' to begin.")

# ------------------- 🔄 Run App -------------------
if __name__ == "__main__":
    main()
