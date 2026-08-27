#!/usr/bin/env python3
"""Build the canonical, executable reproduction notebook."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parent.parent

FORMULAS = [
    r"EU_j=q_j\left[(1-p_j)U(Y+G_j-c_j)+p_jU(Y+G_j-c_j-F_j-R_j)\right]+(1-q_j)U(Y-c_j)",
    r"\pi_j=q_jG_j-c_j-q_jp_j(F_j+R_j)",
    r"\Pi(M)=-C_0+\sum_{m=1}^{M}\left[q_mG_m-c_m-q_mp_m(F_m+R_m)\right]",
    r"\widehat{\theta}_k=\frac{n_k}{n_{k-1}}",
    r"\widehat{p}_{0\rightarrow K}=\prod_{k=1}^{K}\widehat{\theta}_k=\frac{n_K}{n_0}",
    r"DR^{(p)}_{c,d}=\frac{p_c}{p_d}",
    r"G_{j,t}=\sum_{e\in\mathcal{E}_{j,t}}g_e,\qquad N_{j,t}(h)=\sum_{e\in\mathcal{E}_{j,t}}[g_e-r_e(h)]",
    r"E_{j,t}=\frac{1}{T}\int_t^{t+T}V_j(u)\,du",
    r"\widehat{L}^{G}_{j,t}=\frac{G_{j,t}}{E_{j,t}},\qquad \widehat{L}^{N}_{j,t}(h)=\frac{N_{j,t}(h)}{E_{j,t}}",
    r"RVR_{a,b}=\frac{\widehat{L}^{G}_{a,t}}{\widehat{L}^{G}_{b,t}}",
    r"\widehat{L}^{G}_{cash,2019}=\frac{1{,}423{,}559{,}757}{1{,}759{,}800{,}000{,}000}",
    r"\widehat{RR}_{cash,2019}=\frac{36{,}980{,}933}{1{,}423{,}559{,}757}",
    r"\widehat{L}^{N}_{cash,2019}=\frac{1{,}423{,}559{,}757-36{,}980{,}933}{1{,}759{,}800{,}000{,}000}",
    r"S_1\overset{\$}{\leftarrow}\{0,1\}^{256},\qquad S_2=K\oplus S_1",
    r"K=S_1\oplus S_2",
    r"f(x)=K+\sum_{j=1}^{t-1}a_jx^j,\qquad a_j\overset{\$}{\leftarrow}\mathbb{F}",
    r"K=f(0)=\sum_{i=1}^{t}y_i\prod_{\ell\ne i}\frac{x_\ell}{x_\ell-x_i}",
    r"L=\frac{W}{N}\sum_{i=1}^{N}X_i,\qquad \mathbb{E}[L]=pW",
    r"\operatorname{Var}(L)=W^2p(1-p)\left[\frac{1}{N}+\rho\frac{N-1}{N}\right]",
    r"\Pr(L=W)=q+(1-q)p^N",
    r"\min_N\ \mathbb{E}[L_N]+\lambda\,\operatorname{CVaR}_{\alpha}(L_N)+C(N)",
]

NAMES = [
    "Expected utility", "Risk-neutral payoff", "Automated attack portfolio",
    "Enforcement transition rates", "Enforcement cohort probability",
    "Probability-only deterrence ratio", "Gross and net loss totals",
    "Time-weighted exposure", "Exposure-normalized loss intensities",
    "Relative Vulnerability Ratio", "Cash gross intensity", "Cash recovery share",
    "Cash net intensity", "XOR share generation", "XOR reconstruction",
    "Shamir polynomial", "Lagrange reconstruction", "Partition expected loss",
    "Equicorrelated loss variance", "Common-mode catastrophic loss",
    "Partition CVaR objective",
]


def build() -> None:
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
    }
    cells = [nbf.v4.new_markdown_cell(
        "# Reproduction of report equations and figures\n\n"
        "This notebook executes all 21 numbered equations from the manuscript. "
        "Rows labelled `illustrative_scenario` or `deterministic_test_vector` are "
        "not empirical estimates. The cash-versus-crypto RVR and unmatched "
        "enforcement comparison are intentionally returned as `not_estimated`."
    )]
    cells.append(nbf.v4.new_code_cell(
        "from pathlib import Path\n"
        "import sys\n"
        "import matplotlib.pyplot as plt\n"
        "import pandas as pd\n\n"
        "ROOT = Path.cwd()\n"
        "if not (ROOT / 'pyproject.toml').exists():\n"
        "    raise RuntimeError('Run this notebook from the repository root')\n"
        "sys.path.insert(0, str(ROOT / 'src'))\n"
        "from theft_asymmetry.runner import run_all\n"
        "outputs = run_all()\n"
        "assert len(outputs) == 21\n"
        "print('Generated', len(outputs), 'equation outputs')"
    ))
    for number, (name, formula) in enumerate(zip(NAMES, FORMULAS), start=1):
        note = ""
        if number == 6:
            note = "\n\nOnly metadata-matched cohorts produce a ratio; the public-source row is a non-estimate."
        elif number == 10:
            note = "\n\nThe cash-versus-crypto row is rejected by the comparability gate."
        elif number in (14, 15, 16, 17):
            note = "\n\nThe committed values are deterministic conformance vectors, not production entropy."
        cells.append(nbf.v4.new_markdown_cell(f"## Equation {number}: {name}\n\n$${formula}$$" + note))
        cells.append(nbf.v4.new_code_cell(
            f"eq{number:02d} = pd.read_csv(ROOT / 'data/output/eq{number:02d}_results.csv')\n"
            f"eq{number:02d}"
        ))
    cells.append(nbf.v4.new_markdown_cell("## Figures\n\nFigures are generated from the same equation outputs."))
    cells.append(nbf.v4.new_code_cell(
        "figdir = ROOT / 'figures'\nfigdir.mkdir(exist_ok=True)\n"
        "cash = pd.concat([eq11, eq12, eq13], ignore_index=True)\n"
        "ax = cash.plot.bar(x='metric', y='percent', legend=False, color=['#355C7D', '#6C5B7B', '#C06C84'])\n"
        "ax.set_ylabel('Percent')\nax.set_title('2019 U.S. reported-currency calibration')\n"
        "plt.tight_layout(); plt.savefig(figdir / 'cash_calibration.png', dpi=160); plt.show()"
    ))
    cells.append(nbf.v4.new_code_cell(
        "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\n"
        "for label, group in eq19.groupby('scenario_id'):\n"
        "    axes[0].plot(group.n, group.loss_variance, marker='o', label=label)\n"
        "axes[0].set(xlabel='Partitions N', ylabel='Loss variance', title='Equation 19')\naxes[0].legend()\n"
        "for label, group in eq20.groupby('scenario_id'):\n"
        "    axes[1].plot(group.n, group.catastrophic_loss_probability, marker='o', label=label)\n"
        "axes[1].set(xlabel='Partitions N', ylabel='Probability', title='Equation 20')\naxes[1].legend()\n"
        "plt.tight_layout(); plt.savefig(figdir / 'partition_risk.png', dpi=160); plt.show()"
    ))
    cells.append(nbf.v4.new_code_cell(
        "ax = eq21.plot(x='n', y='objective', marker='o', legend=False)\n"
        "best = eq21.loc[eq21.is_minimum].iloc[0]\n"
        "ax.scatter([best.n], [best.objective], color='red', zorder=3, label='conditional minimum')\n"
        "ax.set(xlabel='Partitions N', ylabel='Objective value', title='Equation 21 sensitivity scenario')\n"
        "ax.legend(); plt.tight_layout(); plt.savefig(figdir / 'partition_objective.png', dpi=160); plt.show()"
    ))
    cells.append(nbf.v4.new_markdown_cell(
        "## Interpretation boundary\n\nThe numerical minimizer in Equation 21 is conditional on the supplied "
        "illustrative probabilities, risk weight, feasible values of $N$, and cost function. "
        "It is not an empirical recommendation."
    ))
    nb["cells"] = cells
    nbf.write(nb, ROOT / "reproduce_report_figures.ipynb")


if __name__ == "__main__":
    build()

