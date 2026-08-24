# Cryptoeconomic Theft Asymmetry & Cold Storage Reproduction Suite
This repository contains the official open-science reproduction suite, empirical datasets, mathematical models, and cryptographic verification scripts accompanying the academic research manuscript:
"The Asymmetric Attack Surface of Fiat Substitutes: Modeling Theft Probabilities and Air-Gapped Physical Mitigations for Digital Asset Cold Storage"<br>

Target Journal: Journal of FinTech and Digital Assets (JFDA)

The repository allows automated validation, and computational reproducibility of all econometric and cryptoeconomic models in the above research report.

---

## Environment & Prerequisites

* **Python Version:** Python **3.10** or higher (tested on Python 3.10, 3.11, 3.12, and 3.14).
* **Package Dependencies:** `numpy`, `pandas`, `jupyterlab`, `tabulate`.

---

# Quick-Start Reproduction Guide

## Option A: macOS / Linux (Terminal / Bash)

### 1. Clone the repository
git clone [https://github.com/printdreams/cryptoeconomic-theft-asymmetry.git](https://github.com/printdreams/cryptoeconomic-theft-asymmetry.git)
cd cryptoeconomic-theft-asymmetry

### 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Upgrade package installer and install requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

### 4. Run Econometric Models (Generates CSVs in /outputs)
python scripts/reproduce_models.py

### 5. Run Cryptographic Self-Test (Verifies Galois Field Shamir Scheme)
python scripts/shamir_gf256.py

### 6. Launch Interactive Jupyter Notebook
jupyter lab notebooks/reproduce_report_figures.ipynb<br><br>
Alternatively you can run it directly using Jupyter's nbviewer:<br>
https://nbviewer.org/github/printdreams/cryptoeconomic-theft-asymmetry/blob/main/notebooks/reproduce_report_figures.ipynb
<br><br><br>
## Option B: Windows (PowerShell)
On Windows PowerShell, execution policies or shell environment aliases can occasionally restrict script activation. Follow these tested instructions:

### 1. Clone the repository
git clone [https://github.com/printdreams/cryptoeconomic-theft-asymmetry.git](https://github.com/printdreams/cryptoeconomic-theft-asymmetry.git)
cd cryptoeconomic-theft-asymmetry

### 2. Create virtual environment
py -3 -m venv venv

### 3. Option B1 (Standard Activation): Allow script execution for current session
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

### 4. Install dependencies into virtual environment
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

### 5. Run Econometric Models and Cryptographic Self-Test
python scripts/reproduce_models.py
python scripts/shamir_gf256.py

### 6. Launch Jupyter Lab
jupyter lab notebooks/reproduce_report_figures.ipynb<br><br>
Alternatively you can run it directly using Jupyter's nbviewer:<br> 
https://nbviewer.org/github/printdreams/cryptoeconomic-theft-asymmetry/blob/main/notebooks/reproduce_report_figures.ipynb
<br><br>
## Note for Windows Users (Direct Execution Fallback): 
If PowerShell prevents environment activation, you can execute all commands directly via the virtual environment's binary without modifying system execution policies:

.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts/reproduce_models.py
.\venv\Scripts\python.exe scripts/shamir_gf256.py
.\venv\Scripts\python.exe -m jupyter lab notebooks/reproduce_report_figures.ipynb
<br><br><br>
# Output Verification
Upon executing scripts/reproduce_models.py, 
the following output tables are automatically created in the outputs/ folder:

### 1. table1_monetary_loss_asymmetry.csv: 
Contains exact loss rates ($L_r$) and vulnerability ratios ($\text{RVR}_{agg} = 12.84\times$, $\text{RVR}_{vault} = 560.48\times$).

### 2. table2_clearance_enforcement_gap.csv: 
Summarizes conviction probabilities ($p$) and deterrence gaps ($\mathcal{D}_R$).

### 3. value_partitioning_model.csv: 
Displays loss variance reduction ($\text{Var}/N$) and tail-risk decay ($p^N$) across $N \in \{1, 2, 5, 10, 50, 100\}$.

Running scripts/shamir_gf256.py performs a cryptographic self-test over $GF(2^{256})$ using the primitive polynomial $P(x) = x^{256} + x^{10} + x^5 + x^2 + 1$ (POLYNOMIAL = (1 << 256) | 0x425), confirming:

### - 256-bit key secret splitting into 2 shares.
### - Lagrange polynomial interpolation key reconstruction at $x = 0$.
### - Single-share corruption rejection.
<br><br><br>
# License
This project uses a dual-license model to distinguish between open-source code and open-access research data:

Source Code & Software: Distributed under the MIT License. Free for reuse, modification, and integration. See LICENSE-MIT.

Data, Reports & Visualizations: Distributed under Creative Commons Attribution 4.0 International (CC BY 4.0). Free to share and adapt with appropriate attribution. See LICENSE-CC-BY-4.0.
<br><br><br>
# Citation & Metadata
If you use this codebase, empirical data, or cryptographic implementations in your research, please cite it using the following metadata (BibTeX):
<br><br>
@article{printdreams_crypto_theft_2026,
  author    = {Alex Breton},
  title     = {The Asymmetric Attack Surface of Fiat Substitutes: Modeling Theft Probabilities and Air-Gapped Physical Mitigations for Digital Asset Cold Storage},
  journal   = {Journal of FinTech and Digital Assets (JFDA)},
  year      = {2026},
  doi       = {10.5281/zenodo.22057611},
  publisher = {Zenodo},
  url       = {[https://github.com/printdreams/cryptoeconomic-theft-asymmetry](https://github.com/printdreams/cryptoeconomic-theft-asymmetry)}
}
