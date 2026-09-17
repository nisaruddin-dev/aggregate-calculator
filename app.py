import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="University Aggregate Calculator",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for clean UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .result-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-top: 20px;
    }
    .breakdown-box {
        background-color: #fafafa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎓 Pakistani University Aggregate Calculator")
st.markdown("Calculate your aggregate for admission to Pakistani universities (NUST, FAST, UET, etc.)")

# Sidebar for weightage configuration
st.sidebar.header("⚙️ Weightage Settings")
st.sidebar.markdown("Adjust the weightage as per your university's criteria.")

default_ssc_w = 10
default_hssc_w = 40
default_test_w = 50

ssc_weight = st.sidebar.number_input("SSC/Matric Weightage (%)", min_value=0, max_value=100, value=default_ssc_w, step=5)
hssc_weight = st.sidebar.number_input("HSSC/FSc Weightage (%)", min_value=0, max_value=100, value=default_hssc_w, step=5)
test_weight = st.sidebar.number_input("Entry Test Weightage (%)", min_value=0, max_value=100, value=default_test_w, step=5)

total_weight = ssc_weight + hssc_weight + test_weight

if total_weight != 100:
    st.sidebar.warning(f"⚠️ Total weightage is {total_weight}%. It should sum to 100%.")
else:
    st.sidebar.success("✅ Total weightage: 100%")

st.sidebar.markdown("---")
st.sidebar.markdown("**Common Weightages:**")
st.sidebar.markdown("- NUST: 10% SSC, 40% HSSC, 50% NET")
st.sidebar.markdown("- FAST: 10% SSC, 40% HSSC, 50% Test")
st.sidebar.markdown("- UET: 10% SSC, 40% HSSC, 50% ECAT")

# Input fields
st.header("📝 Enter Your Marks")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("SSC / Matric")
    ssc_obtained = st.number_input("Obtained Marks", min_value=0.0, max_value=1100.0, value=900.0, step=1.0, key="ssc_obt")
    ssc_total = st.number_input("Total Marks", min_value=1.0, max_value=1100.0, value=1100.0, step=1.0, key="ssc_tot")

with col2:
    st.subheader("HSSC / FSc Part-I")
    hssc_obtained = st.number_input("Obtained Marks", min_value=0.0, max_value=600.0, value=450.0, step=1.0, key="hssc_obt")
    hssc_total = st.number_input("Total Marks", min_value=1.0, max_value=600.0, value=520.0, step=1.0, key="hssc_tot")

with col3:
    st.subheader("Entry Test")
    test_obtained = st.number_input("Obtained Marks", min_value=0.0, max_value=400.0, value=140.0, step=1.0, key="test_obt")
    test_total = st.number_input("Total Marks", min_value=1.0, max_value=400.0, value=200.0, step=1.0, key="test_tot")

# Calculate button
st.markdown("---")
calculate = st.button("🧮 Calculate Aggregate", use_container_width=True)

if calculate:
    # Validation
    errors = []
    if ssc_obtained > ssc_total:
        errors.append("SSC obtained marks cannot exceed total marks.")
    if hssc_obtained > hssc_total:
        errors.append("HSSC obtained marks cannot exceed total marks.")
    if test_obtained > test_total:
        errors.append("Entry Test obtained marks cannot exceed total marks.")
    if total_weight != 100:
        errors.append(f"Total weightage must be 100% (currently {total_weight}%).")

    if errors:
        for err in errors:
            st.error(err)
    else:
        # Calculate percentages
        ssc_pct = (ssc_obtained / ssc_total) * 100
        hssc_pct = (hssc_obtained / hssc_total) * 100
        test_pct = (test_obtained / test_total) * 100

        # Calculate weighted contributions
        ssc_contrib = (ssc_pct * ssc_weight) / 100
        hssc_contrib = (hssc_pct * hssc_weight) / 100
        test_contrib = (test_pct * test_weight) / 100

        aggregate = ssc_contrib + hssc_contrib + test_contrib

        # Display result
        st.markdown(f"""
            <div class="result-box">
                <h2 style="margin:0; color:#1f77b4;">Your Aggregate: {aggregate:.4f}%</h2>
            </div>
        """, unsafe_allow_html=True)

        # Breakdown
        st.subheader("📊 Transparent Breakdown")

        breakdown_data = {
            "Component": ["SSC / Matric", "HSSC / FSc Part-I", "Entry Test", "Total"],
            "Obtained": [f"{ssc_obtained:.0f}/{ssc_total:.0f}", f"{hssc_obtained:.0f}/{hssc_total:.0f}", f"{test_obtained:.0f}/{test_total:.0f}", "—"],
            "Percentage": [f"{ssc_pct:.2f}%", f"{hssc_pct:.2f}%", f"{test_pct:.2f}%", "—"],
            "Weightage": [f"{ssc_weight}%", f"{hssc_weight}%", f"{test_weight}%", f"{total_weight}%"],
            "Contribution": [f"{ssc_contrib:.4f}%", f"{hssc_contrib:.4f}%", f"{test_contrib:.4f}%", f"{aggregate:.4f}%"]
        }

        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

        # Detailed formula breakdown
        st.markdown(f"""
            <div class="breakdown-box">
                <h4>🧾 Detailed Calculation</h4>
                <p><b>SSC Contribution:</b><br>
                ({ssc_obtained:.0f} ÷ {ssc_total:.0f}) × 100 × {ssc_weight}% = <b>{ssc_contrib:.4f}%</b></p>
                <p><b>HSSC Contribution:</b><br>
                ({hssc_obtained:.0f} ÷ {hssc_total:.0f}) × 100 × {hssc_weight}% = <b>{hssc_contrib:.4f}%</b></p>
                <p><b>Entry Test Contribution:</b><br>
                ({test_obtained:.0f} ÷ {test_total:.0f}) × 100 × {test_weight}% = <b>{test_contrib:.4f}%</b></p>
                <hr>
                <p><b>Final Aggregate:</b> {ssc_contrib:.4f} + {hssc_contrib:.4f} + {test_contrib:.4f} = 
                <b style="color:#1f77b4;">{aggregate:.4f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.markdown("### 📈 Aggregate Visualization")
        st.progress(min(int(aggregate), 100))

# Footer
st.markdown("---")
st.caption("💡 Note: Different universities may have different weightage criteria. Adjust the sidebar settings accordingly.")
st.caption("Common formulas: NUST (10-40-50), FAST (10-40-50), UET (10-40-50), but always verify with the official prospectus.")