import streamlit as st
import pandas as pd

# ---------- Page config ----------
st.set_page_config(
    page_title="Pakistani University Aggregate Calculator",
    page_icon="🎓",
    layout="centered",
)

st.markdown("""
    <style>
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

st.title("🎓 Pakistani University Aggregate Calculator")

# ---------- University presets ----------
UNIVERSITIES = {
    "NUST": {
        "weights": {"test": 75, "hssc": 15, "ssc": 10},
        "test_label": "NET Marks (out of 200)",
        "test_max": 200,
        "hssc_max": 100,
        "ssc_max": 100,
        "note": "NUST uses NET 75% + HSSC 15% + SSC 10%.",
    },
    "UET Taxila": {
        "weights": {"hssc": 50, "test": 33, "ssc": 17},
        "test_label": "ECAT Marks (out of 400)",
        "test_max": 400,
        "hssc_max": 100,
        "ssc_max": 100,
        "note": "UET Taxila uses HSSC-I 50% + ECAT 33% + SSC 17%.",
    },
    "FAST": {
        "weights": {"test": 50, "hssc": 40, "ssc": 10},
        "test_label": "FAST Entry Test Marks (out of 100)",
        "test_max": 100,
        "hssc_max": 100,
        "ssc_max": 100,
        "note": "FAST uses Test 50% + HSSC 40% + SSC 10%.",
    },
    "Custom": {
        "weights": {"ssc": 10, "hssc": 40, "test": 50},
        "test_label": "Entry Test Marks",
        "test_max": 400,
        "hssc_max": 1100,
        "ssc_max": 1100,
        "note": "Manually set your own weightages in the sidebar.",
    },
}

# ---------- Mode selector ----------
mode = st.radio(
    "Select mode",
    ["University Preset", "Custom Weightage"],
    horizontal=True,
)

if mode == "University Preset":
    university = st.selectbox("Select University", ["NUST", "UET Taxila", "FAST"])
    config = UNIVERSITIES[university]
    st.info(config["note"])
    ssc_weight = config["weights"]["ssc"]
    hssc_weight = config["weights"]["hssc"]
    test_weight = config["weights"]["test"]
    ssc_max = config["ssc_max"]
    hssc_max = config["hssc_max"]
    test_max = config["test_max"]
    test_label = config["test_label"]
else:
    st.sidebar.header("⚙️ Custom Weightage")
    ssc_weight = st.sidebar.number_input("SSC/Matric Weightage (%)", 0, 100, 10, 5)
    hssc_weight = st.sidebar.number_input("HSSC/FSc Weightage (%)", 0, 100, 40, 5)
    test_weight = st.sidebar.number_input("Entry Test Weightage (%)", 0, 100, 50, 5)
    total = ssc_weight + hssc_weight + test_weight
    if total != 100:
        st.sidebar.warning(f"⚠️ Total weightage is {total}%. Should sum to 100%.")
    else:
        st.sidebar.success("✅ Total weightage: 100%")
    ssc_max, hssc_max, test_max = 1100, 1100, 400
    test_label = "Entry Test Marks"

# ---------- Inputs ----------
st.header("📝 Enter Your Marks")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("SSC / Matric")
    ssc_obtained = st.number_input("Obtained", 0.0, float(ssc_max), float(ssc_max) * 0.85, 1.0, key="ssc_obt")
    ssc_total = st.number_input("Total", 1.0, float(ssc_max), float(ssc_max), 1.0, key="ssc_tot")

with col2:
    st.subheader("HSSC / FSc Part-I")
    hssc_obtained = st.number_input("Obtained", 0.0, float(hssc_max), float(hssc_max) * 0.80, 1.0, key="hssc_obt")
    hssc_total = st.number_input("Total", 1.0, float(hssc_max), float(hssc_max), 1.0, key="hssc_tot")

with col3:
    st.subheader("Entry Test")
    test_obtained = st.number_input(test_label, 0.0, float(test_max), float(test_max) * 0.70, 1.0, key="test_obt")
    test_total = st.number_input("Test Total", 1.0, float(test_max), float(test_max), 1.0, key="test_tot")

# ---------- Validate ----------
errors = []
if ssc_obtained > ssc_total: errors.append("SSC obtained marks cannot exceed total.")
if hssc_obtained > hssc_total: errors.append("HSSC obtained marks cannot exceed total.")
if test_obtained > test_total: errors.append("Entry Test obtained marks cannot exceed total.")
if mode == "Custom Weightage" and (ssc_weight + hssc_weight + test_weight) != 100:
    errors.append("Custom weightage must sum to 100%.")

if errors:
    for e in errors:
        st.error(e)
    st.stop()

# ---------- Compute ----------
ssc_pct  = (ssc_obtained  / ssc_total)  * 100
hssc_pct = (hssc_obtained / hssc_total) * 100
test_pct = (test_obtained / test_total) * 100

ssc_contrib  = (ssc_pct  * ssc_weight)  / 100
hssc_contrib = (hssc_pct * hssc_weight) / 100
test_contrib = (test_pct * test_weight) / 100
aggregate = ssc_contrib + hssc_contrib + test_contrib

# ---------- Result ----------
st.markdown("---")
st.markdown("### 🎯 Your Aggregate")

c1, c2, c3, c4 = st.columns(4)
c1.metric("SSC %",  f"{ssc_pct:.2f}%")
c2.metric("HSSC %", f"{hssc_pct:.2f}%")
c3.metric("Test %", f"{test_pct:.2f}%")
c4.metric("Final Aggregate", f"{aggregate:.2f}%")

# ---------- Breakdown ----------
st.markdown("### 📊 Transparent Breakdown")

df = pd.DataFrame({
    "Component":   ["SSC/Matric", "HSSC/FSc-I", "Entry Test", "Total"],
    "Obtained":    [f"{ssc_obtained:.0f}/{ssc_total:.0f}",
                    f"{hssc_obtained:.0f}/{hssc_total:.0f}",
                    f"{test_obtained:.0f}/{test_total:.0f}", "—"],
    "Percentage":  [f"{ssc_pct:.2f}%", f"{hssc_pct:.2f}%", f"{test_pct:.2f}%", "—"],
    "Weightage":   [f"{ssc_weight}%", f"{hssc_weight}%", f"{test_weight}%",
                    f"{ssc_weight + hssc_weight + test_weight}%"],
    "Contribution":[f"{ssc_contrib:.4f}%", f"{hssc_contrib:.4f}%",
                    f"{test_contrib:.4f}%", f"{aggregate:.4f}%"],
})
st.dataframe(df, hide_index=True, width="stretch")

with st.expander("See step-by-step calculation"):
    st.write(f"**SSC:** ({ssc_obtained:.0f} ÷ {ssc_total:.0f}) × 100 × {ssc_weight}% = **{ssc_contrib:.2f}%**")
    st.write(f"**HSSC:** ({hssc_obtained:.0f} ÷ {hssc_total:.0f}) × 100 × {hssc_weight}% = **{hssc_contrib:.2f}%**")
    st.write(f"**Test:** ({test_obtained:.0f} ÷ {test_total:.0f}) × 100 × {test_weight}% = **{test_contrib:.2f}%**")
    st.write(f"**Final Aggregate** = **{aggregate:.2f}%**")

st.progress(min(int(aggregate), 100))
st.caption("⚠️ Verify weightages with the official prospectus before relying on this result.")