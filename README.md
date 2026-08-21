# cryptoeconomic-theft-asymmetry
Allows automated validation, and computational reproducibility of all econometric and cryptoeconomic models in my research report called "The Asymmetric Attack Surface of Fiat Substitutes: Modeling Theft Probabilities and Air-Gapped Physical Mitigations for Digital Asset Cold Storage"

<H><b>Reproducibility Commands (Linux / macOS / Windows)</H></b><br>
# 1. Clone the repository
git clone https://github.com/your-username/cryptoeconomic-theft-asymmetry.git
cd cryptoeconomic-theft-asymmetry

# 2. Set up Python 3.10 virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Upgrade pip and install pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Execute automated calculation script to generate outputs
python scripts/reproduce_models.py

# 5. Launch Jupyter Lab for interactive peer review
jupyter lab notebooks/reproduce_report_figures.ipynb
