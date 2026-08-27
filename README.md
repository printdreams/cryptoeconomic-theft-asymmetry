# Cryptoeconomic Theft Asymmetry: Reproduction Suite

This repository is the computational companion to **“The Asymmetric Attack
Surface of Fiat Substitutes: A Measurement Framework and Owner-Bound Offline
Custody Architecture.”** It provides executable specifications for all 21 numbered
display equations, machine-readable inputs and outputs, deterministic cryptographic
test vectors, an integrated notebook, and continuous-integration checks.

The repository separates empirical calibrations from illustrative scenarios. It
does **not** publish a global “per-dollar theft probability,” an empirical
cash-versus-crypto Relative Vulnerability Ratio (RVR), or a cross-domain deterrence
ratio: the available public data do not meet the manuscript’s matching conditions.

## What is reproducible

- Equations 1–3: offender utility, risk-neutral payoff, and reusable-attack scale
- Equations 4–6: stage-specific enforcement transitions and conditional deterrence ratio
- Equations 7–10: gross/net losses, time-weighted exposure, loss intensity, and metadata-gated RVR
- Equations 11–13: 2019 U.S. reported-currency calibration
- Equations 14–17: XOR and Shamir algebra with deterministic known-answer tests
- Equations 18–21: partition expectation, correlated variance, common-mode tail loss, and exact discrete CVaR optimization

The canonical map from equation to script, input, output, and evidence class is
[`data/equation_registry.csv`](data/equation_registry.csv).

## Repository structure

```text
.
├── src/theft_asymmetry/       # Tested model and runner library
├── scripts/                   # One executable script per equation + unified runner
├── data/
│   ├── input/                 # Empirical calibration, scenarios, and test vectors
│   ├── output/                # Deterministically regenerated CSV results
│   └── equation_registry.csv  # Equation-to-code audit trail
├── tests/                     # Algebra, numerical invariants, and non-estimate gates
├── docs/                      # Methodology, data dictionary, and limitations
├── figures/                   # Notebook-generated figures
├── reproduce_report_figures.ipynb
└── .github/workflows/reproducibility.yml
```

Legacy files are retained under `legacy/` only to preserve provenance. They are not
part of the current reproduction path because they used unmatched denominators and
unsupported enforcement quantities.

## Quick start

Python 3.10 or later is required although in our tests we noticed that Python 3.14 currently segfaults with the pinned numpy/pandas. Python 3.10 and 3.12 worked fine during our testing.

```bash
git clone https://github.com/printdreams/cryptoeconomic-theft-asymmetry.git
cd cryptoeconomic-theft-asymmetry
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
python -m pip install -e . --no-deps
make verify
```

Without `make`, run:

```bash
python scripts/reproduce_all.py
python -m pytest
python -m nbconvert --to notebook --execute \
  reproduce_report_figures.ipynb \
  --output reproduce_report_figures.ipynb \
  --ExecutePreprocessor.timeout=180
```

Run one equation independently:

```bash
python scripts/eq11_cash_gross_intensity.py
# or
python scripts/run_equation.py 11 --output /tmp/eq11.csv
```

## Empirical calibration and non-estimates

The committed U.S. cash calibration uses:

- reported stolen currency: USD 1,423,559,757;
- reported recovered currency: USD 36,980,933; and
- year-end currency in circulation: USD 1,759,800,000,000.

The scripts reproduce a gross reported loss intensity of approximately 0.080893%,
a recovery share of approximately 2.5978%, and a net reported loss intensity of
approximately 0.078792%. These are lower-bound reported-value calibrations. The
stock denominator includes currency abroad and is not average value exposed to
theft.

The 2024 Chainalysis and TRM Labs estimates of roughly USD 2.2 billion stolen are
not divided by stablecoin supply or total crypto market capitalization. Their
incident perimeters do not supply a matched reachable-exposure denominator. The
RVR runner therefore rejects the included cash-versus-crypto example and records
`not_estimated` with the mismatched fields.

Likewise, clearance, identification, arrest, prosecution, and conviction are
distinct stages. Equation 6 produces a number only for a metadata-matched scenario;
the unmatched public-source row is retained as a machine-checkable non-estimate.

## Cryptographic scope

XOR and Shamir files are conformance tests, not production custody software.
Deterministic values are never suitable as production entropy.

Shamir examples use the versioned `prime521-v1` profile over the prime field
$p=2^{521}-1$. This admits every 256-bit secret without modular truncation and makes
the field and encoding assumptions explicit. The suite intentionally makes no
`GF(2^{256})` claim. A binary-field profile must first specify a vetted irreducible
polynomial, polynomial-basis encoding, byte order, share-index rules, known-answer
vectors, malformed-input behavior, and independent review.

Secret sharing is not threshold signing and does not authenticate shares. Real
deployments must address entropy, independent control, authenticated envelopes,
pre-funding verification, parser and firmware risk, zeroization limits,
supply-chain compromise, side channels, coercion, recovery, and common-mode failure.

## Inputs, outputs, and auditability

CSV fields and provenance are described in [`docs/data_dictionary.md`](docs/data_dictionary.md).
Model assumptions and numerical conventions are described in
[`docs/methodology.md`](docs/methodology.md). Each generated CSV contains an
`equation` column and retains an evidence classification.

The GitHub Actions workflow runs the 21 equations, unit tests, and notebook on
Python 3.10 and 3.12. It then fails if regenerated CSV outputs differ from the
committed versions. `requirements-lock.txt` defines the reference environment;
`pyproject.toml` retains compatible ranges for library consumers.

## Primary empirical sources

- [FBI Crime in the United States 2019, Table 24](https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-24)
- [Federal Reserve Board, Currency in Circulation: Value](https://www.federalreserve.gov/paymentsystems/coin_currcircvalue.htm)
- [Chainalysis 2024 hacking update](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2025/)
- [TRM Labs 2024 hacks analysis](https://www.trmlabs.com/resources/blog/category-deep-dive-2-2-billion-was-stolen-in-crypto-related-hacks-in-2024)

## License and citation

Source code is available under the MIT License. Data, reports, and visualizations
are available under CC BY 4.0; see `LICENSE-MIT` and `LICENSE-CC-BY-4.0`.

Citation metadata are supplied in `CITATION-draft.cff` and `CITATION-draft.bib`.
Update the draft fields when the manuscript receives final bibliographic metadata.
