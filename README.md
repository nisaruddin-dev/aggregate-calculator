# 🎓 Pakistani University Aggregate Calculator

A simple, transparent Streamlit web app that calculates your admission aggregate for Pakistani universities (NUST, FAST, UET, and others). It shows a full breakdown of how the final percentage is derived, so you can verify every step.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aggregate-calculator.streamlit.app/)

## ✨ Features

- Adjustable weightage for SSC/Matric, HSSC/FSc Part-I, and Entry Test
- Pre-configured presets for common universities (NUST, FAST, UET)
- Transparent breakdown table showing contribution of each component
- Step-by-step formula display so you can verify the math yourself
- Live validation — warns if weightages don't sum to 100% or marks exceed totals
- Clean, minimal UI

## 🖥️ Live Demo

👉 **[Try the app here](https://aggregate-calculator.streamlit.app/)**

> **Note:** To run this app locally, follow the instructions below. Local access is only available on your own machine at `http://localhost:8501`.

## 🚀 Getting Started (Local Development)

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

```bash
git clone https://github.com/nisaruddin-dev/aggregate-calculator.git
cd aggregate-calculator
python -m venv venv
Activate the virtual environment:

Windows (PowerShell):

powershell
.\venv\Scripts\Activate.ps1
macOS / Linux:

bash
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Run the app
bash
streamlit run app.py
If streamlit is not recognized on your PATH, use:

bash
python -m streamlit run app.py
Then open http://localhost:8501 in your browser.

📐 How the Aggregate Is Calculated
The final aggregate is a weighted sum of three components:

text
Aggregate = (SSC% × SSC weightage)
          + (HSSC% × HSSC weightage)
          + (Test% × Test weightage)
Where each component's percentage is:

text
Component % = (Obtained Marks ÷ Total Marks) × 100
Common weightages
University	SSC	HSSC	Entry Test
NUST	10%	40%	50% (NET)
FAST	10%	40%	50%
UET	10%	40%	50% (ECAT)
Always verify weightage against the current official prospectus, as criteria can change year to year.

🗂️ Project Structure
text
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
└── README.md           # This file
🛠️ Built With
Streamlit — web app framework

pandas — data display

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first.

📄 License
This project is open source and available under the MIT License.

⚠️ Disclaimer
This calculator is for informational purposes only. Different universities may apply different weightages or rounding rules. Always confirm with the official admission office or prospectus before relying on any result.
