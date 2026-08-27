# Repository update notes

## Structural changes

- Added an installable `src/theft_asymmetry` package containing side-effect-free
  reference implementations.
- Added 21 individually executable scripts and one unified runner.
- Replaced aggregate ad hoc inputs with equation-specific CSV schemas and a
  machine-readable equation registry.
- Added deterministic output CSVs, algebraic and numerical tests, a unified
  notebook, figures, a pinned reference environment, and GitHub Actions.
- Moved superseded scripts and outputs to `legacy/` with explicit non-use warnings.

## Scientific controls

- RVR calculation now requires nine matching metadata fields.
- Unmatched cash-versus-crypto and public enforcement comparisons return
  `not_estimated`.
- Loss rates are named exposure-normalized intensities, not per-unit theft
  probabilities.
- Enforcement transitions preserve event cohorts and distinguish stages.
- The cash calibration uses the reported 2019 FBI numerator and Federal Reserve
  stock denominator with its limitations retained.
- Shamir conformance uses a declared prime-field profile instead of an unverified
  binary polynomial.
- Partition outputs include correlation, common-mode compromise, and exact
  discrete upper-tail CVaR.

