import streamlit as st
import pandas as pd
from optimizer import optimize_top_7, optimize_balanced

st.set_page_config(page_title="HR Derby Optimizer", layout="wide")

# ---------- Password Protection ----------
def check_password():
    if "authenticated" not in st.session_state:
        st.header("🔒 Login")
        password = st.text_input("Enter password", type="password")
        if password == st.secrets["password"]:
            st.session_state.authenticated = True
            st.rerun()
        elif password:
            st.error("Access denied.")
            st.stop()
        else:
            st.stop()
    else:
        st.success("✅ Access granted. Welcome!")

check_password()

# ---------- Settings ----------
DEFAULT_DATA_PATH = "final_2025_combined_dataset.csv"
TEAM_SIZE = 8
TOP_K = 7
BUDGET_CAP = 163

# ---------- App Title and Rules ----------
# st.set_page_config(page_title="HR Derby Optimizer", layout="wide")
st.title("2025 Home Run Derby Optimizer")
st.markdown("""
### Competition Rules:
- Draft **8 MLB players** under a **163-point budget** (based on 2024 HR totals)
- Each month, **only the top 7 HR hitters** from your team count
- You can customize 2025 HR projections and run one of two optimizers:
    - **Balanced Optimizer**: Maximizes projected HRs across all 8 players (safe, well-rounded)
    - **Top-Heavy Optimizer**: Maximizes the top 7 of 8 scorers (focuses on ceiling, allows one weak backup)

📊 *P2025 HR Projection data is based on 'The Bat' & 'The Bat X' by Derek Carty.*
""")

# ---------- Load and Display Editable Table ----------
st.subheader("Edit 2025 HR Projections")

@st.cache_data
def load_default_data():
    df = pd.read_csv(DEFAULT_DATA_PATH)
    df = df.rename(columns={
        "2024_rank": "2024 Rank",
        "player_name": "Name",
        "team": "Team",
        "cost_to_draft": "Cost to Draft (2024 HR Total)",
        "hr_projection": "2025 HR Projections"
    })
    return df

df_default = load_default_data()
df_user = st.data_editor(df_default, use_container_width=True, num_rows="fixed", hide_index=True)

# ---------- Buttons ----------
col1, col2 = st.columns(2)
run_balanced = col1.button("📊 Run Balanced Optimizer")
run_top_heavy = col2.button("⚡ Run Top-Heavy Optimizer")

st.markdown("🔄 **To restore default projections, please refresh the webpage**")

# ---------- Optimizer Execution ----------
if run_balanced:
    with st.spinner("Running balanced optimizer..."):
        df_input = df_user.copy()
        df_input.columns = df_input.columns.str.strip()
        df_input = df_input.rename(columns={
            "2024 Rank": "2024_rank",
            "Name": "player_name",
            "Team": "team",
            "Cost to Draft (2024 HR Total)": "cost_to_draft",
            "2025 HR Projections": "hr_projection"
        })

        df_team, total_cost, total_hr_projection, status = optimize_balanced(
            df_input,
            budget_cap=BUDGET_CAP,
            team_size=TEAM_SIZE
        )

        if status != "Optimal":
            st.error("❌ Optimization failed. Please check your input data.")
        else:
            st.success("✅ Optimization complete!")
            st.subheader("Balanced Optimized Team (Highest HR total for all 8 Players.)")
            st.dataframe(df_team.rename(columns={
                "player_name": "Name",
                "team": "Team",
                "cost_to_draft": "Cost to Draft (2024 HR Total)",
                "hr_projection": "2025 HR Projections"
            }), use_container_width=True, hide_index=True)
            st.markdown(f"**Total Budget Used:** {total_cost}")
            st.markdown(f"**Projected Total HRs (All 8):** {total_hr_projection}")

if run_top_heavy:
    with st.spinner("Running top-heavy optimizer..."):
        df_input = df_user.copy()
        df_input.columns = df_input.columns.str.strip()
        df_input = df_input.rename(columns={
            "2024 Rank": "2024_rank",
            "Name": "player_name",
            "Team": "team",
            "Cost to Draft (2024 HR Total)": "cost_to_draft",
            "2025 HR Projections": "hr_projection"
        })

        df_team, total_cost, total_hr_projection, status = optimize_top_7(
            df_input,
            budget_cap=BUDGET_CAP,
            team_size=TEAM_SIZE,
            top_k=TOP_K
        )

        if status != "Optimal":
            st.error("❌ Optimization failed. Please check your input data.")
        else:
            st.success("✅ Optimization complete!")
            st.subheader("Top-Heavy Optimized Team (Top 7 of 8 Players Count)")
            st.dataframe(df_team.rename(columns={
                "player_name": "Name",
                "team": "Team",
                "cost_to_draft": "Cost to Draft (2024 HR Total)",
                "hr_projection": "2025 HR Projections"
            }), use_container_width=True, hide_index=True)
            st.markdown(f"**Total Budget Used:** {total_cost}")
            st.markdown(f"**Projected Total HRs (Top 7 of 8):** {total_hr_projection}")

st.divider()
st.markdown("Built with 🍺 using [Streamlit](https://streamlit.io/) and [PuLP.](https://pypi.org/project/PuLP/)")
