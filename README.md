# cryptoeconomic-theft-asymmetry
Allows automated validation, and computational reproducibility of all econometric and cryptoeconomic models in my research report called "The Asymmetric Attack Surface of Fiat Substitutes: Modeling Theft Probabilities and Air-Gapped Physical Mitigations for Digital Asset Cold Storage"

# <b>Reproducibility Commands (Linux / macOS / Windows)</b><br><br>
# 1. Clone the repository<br>
git clone https://github.com/your-username/cryptoeconomic-theft-asymmetry.git<br>
cd cryptoeconomic-theft-asymmetry<br>

# 2. Set up Python 3.10 virtual environment<br>
python3.10 -m venv venv<br>
source venv/bin/activate  # On Windows: venv\Scripts\activate<br>

# 3. Upgrade pip and install pinned dependencies<br>
pip install --upgrade pip<br>
pip install -r requirements.txt<br>

# 4. Execute automated calculation script to generate outputs<br>
python scripts/reproduce_models.py<br>

# 5. Launch Jupyter Lab for interactive peer review<br>
jupyter lab notebooks/reproduce_report_figures.ipynb<br>
