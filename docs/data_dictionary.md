# Data dictionary and provenance

All monetary values are nominal U.S. dollars unless a CSV states otherwise.
Input files are UTF-8 CSV with a header row; generated outputs use the same format.

| File | Purpose | Status |
|---|---|---|
| `us_cash_2019.csv` | Equations 11–13 | Empirical calibration from FBI Table 24 and Federal Reserve currency stock |
| `theft_events.csv` | Equation 7 | One empirical aggregate split plus synthetic test events |
| `exposure_observations.csv` | Equation 8 | Transparent cash-stock approximation plus synthetic series |
| `rvr_scenarios.csv` | Equation 10 | One valid synthetic comparison and one intentionally rejected empirical comparison |
| `enforcement_pipeline.csv` | Equations 4–5 | Mature synthetic event cohort; not public enforcement evidence |
| `deterrence_scenarios.csv` | Equation 6 | Synthetic sensitivity and an intentionally rejected unmatched comparison |
| `xor_test_vectors.csv` | Equations 14–15 | Deterministic known-answer vectors; never production entropy |
| `shamir_prime521_test_vectors.csv` | Equations 16–17 | Deterministic algebraic conformance vectors |
| `partition_scenarios.csv` | Equations 18–20 | Illustrative risk scenarios |
| `optimization_scenarios.csv` | Equation 21 | Illustrative decision parameters |

Primary empirical sources:

- FBI, *Crime in the United States 2019*, Table 24: <https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-24>
- Federal Reserve Board, *Currency in Circulation: Value*: <https://www.federalreserve.gov/paymentsystems/coin_currcircvalue.htm>

Commercial 2024 crypto-loss reports are documented in the manuscript but are not
used to calculate an exposure-normalized intensity because neither supplies a
matched stablecoin or all-crypto reachable-exposure denominator.

