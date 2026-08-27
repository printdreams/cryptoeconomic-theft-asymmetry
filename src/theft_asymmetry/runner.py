"""CSV-driven equation runners and output contract."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from . import models as m


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "input"
OUTPUT = ROOT / "data" / "output"


def _rows(name: str) -> pd.DataFrame:
    return pd.read_csv(INPUT / name, keep_default_na=False)


def _write(number: int, frame: pd.DataFrame, output_path: Path | None) -> Path:
    path = output_path or OUTPUT / f"eq{number:02d}_results.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.insert(0, "equation", number)
    frame.to_csv(path, index=False)
    return path


def run_equation(number: int, output_path: Path | None = None) -> Path:
    """Evaluate one numbered display equation from committed CSV inputs."""
    if number == 1:
        x = _rows("offender_scenarios.csv")
        x["expected_utility"] = x.apply(lambda r: m.expected_utility(
            r.q, r.p, r.baseline_wealth, r.gain, r.execution_cost, r.penalty,
            r.recovery, r.utility_family, r.risk_aversion), axis=1)
        out = x[["scenario_id", "classification", "utility_family", "expected_utility"]]
    elif number == 2:
        x = _rows("offender_scenarios.csv")
        x["expected_payoff"] = x.apply(lambda r: m.risk_neutral_payoff(
            r.q, r.p, r.gain, r.execution_cost, r.penalty, r.recovery), axis=1)
        out = x[["scenario_id", "classification", "expected_payoff"]]
    elif number == 3:
        x = _rows("attack_portfolio.csv")
        records = []
        for sid, group in x.groupby("scenario_id", sort=False):
            targets = group.rename(columns={"fixed_development_cost": "fixed"}).to_dict("records")
            records.append({"scenario_id": sid, "classification": group.classification.iloc[0],
                            "target_count": len(group), "portfolio_payoff":
                            m.attack_portfolio(group.fixed_development_cost.iloc[0], targets)})
        out = pd.DataFrame(records)
    elif number in (4, 5):
        x = _rows("enforcement_pipeline.csv")
        records = []
        for cohort, group in x.groupby("cohort_id", sort=False):
            g = group.sort_values("stage_order")
            counts = g.event_count.astype(int).tolist()
            if number == 4:
                for (_, prev), (_, cur) in zip(g.iloc[:-1].iterrows(), g.iloc[1:].iterrows()):
                    records.append({"cohort_id": cohort, "classification": cur.classification,
                                    "from_stage": prev.stage, "to_stage": cur.stage,
                                    "n_previous": prev.event_count, "n_current": cur.event_count,
                                    "transition_rate": m.enforcement_transition(prev.event_count, cur.event_count)})
            else:
                product, ratio = m.enforcement_cohort_probability(counts)
                records.append({"cohort_id": cohort, "classification": g.classification.iloc[0],
                                "initial_count": counts[0], "final_count": counts[-1],
                                "transition_product": product, "telescoping_ratio": ratio,
                                "identity_error": abs(product-ratio)})
        out = pd.DataFrame(records)
    elif number == 6:
        x = _rows("deterrence_scenarios.csv")
        records = []
        for r in x.itertuples():
            if not r.metadata_matched:
                records.append({"scenario_id": r.scenario_id, "classification": r.classification,
                                "status": "not_estimated", "deterrence_ratio": "",
                                "reason": "cohort metadata are not matched"})
            else:
                records.append({"scenario_id": r.scenario_id, "classification": r.classification,
                                "status": "estimated", "deterrence_ratio": m.deterrence_ratio(r.p_cash, r.p_digital),
                                "reason": ""})
        out = pd.DataFrame(records)
    elif number == 7:
        x = _rows("theft_events.csv")
        records = []
        for keys, group in x.groupby(["domain", "period", "recovery_horizon_days"], sort=False):
            gross, net = m.loss_totals(group)
            records.append({"domain": keys[0], "period": keys[1], "recovery_horizon_days": keys[2],
                            "classification": group.classification.iloc[0], "gross_loss": gross, "net_loss": net})
        out = pd.DataFrame(records)
    elif number == 8:
        x = _rows("exposure_observations.csv")
        records = []
        for keys, group in x.groupby(["domain", "period"], sort=False):
            records.append({"domain": keys[0], "period": keys[1],
                            "classification": group.classification.iloc[0],
                            "time_weighted_exposure": m.time_weighted_exposure(group)})
        out = pd.DataFrame(records)
    elif number == 9:
        events = pd.read_csv(OUTPUT / "eq07_results.csv")
        exposure = pd.read_csv(OUTPUT / "eq08_results.csv")
        x = events.merge(exposure, on=["domain", "period", "classification"])
        vals = x.apply(lambda r: m.loss_intensities(r.gross_loss, r.net_loss, r.time_weighted_exposure), axis=1)
        x[["gross_loss_intensity", "net_loss_intensity"]] = pd.DataFrame(vals.tolist(), index=x.index)
        out = x.drop(columns=["equation_x", "equation_y"])
    elif number == 10:
        x = _rows("rvr_scenarios.csv")
        records = []
        for scenario, group in x.groupby("scenario_id", sort=False):
            a = group.loc[group.side == "a"].iloc[0].to_dict()
            b = group.loc[group.side == "b"].iloc[0].to_dict()
            try:
                value = m.relative_vulnerability_ratio(a, b)
                status, reason = "estimated", ""
            except ValueError as exc:
                value, status, reason = "", "not_estimated", str(exc)
            records.append({"scenario_id": scenario, "classification": a["classification"],
                            "status": status, "rvr": value, "reason": reason})
        out = pd.DataFrame(records)
    elif number in (11, 12, 13):
        r = _rows("us_cash_2019.csv").iloc[0]
        if number == 11:
            value, metric = m.cash_gross_intensity(r.gross_stolen_usd, r.currency_stock_usd), "gross_loss_intensity"
        elif number == 12:
            value, metric = m.cash_recovery_share(r.recovered_usd, r.gross_stolen_usd), "recovery_share"
        else:
            value, metric = m.cash_net_intensity(r.gross_stolen_usd, r.recovered_usd, r.currency_stock_usd), "net_loss_intensity"
        out = pd.DataFrame([{"domain": "U.S. reported currency", "period": 2019,
                             "classification": "empirical_calibration", "metric": metric,
                             "value": value, "percent": 100*value}])
    elif number in (14, 15):
        x = _rows("xor_test_vectors.csv")
        records = []
        for r in x.itertuples():
            secret = bytes.fromhex(r.secret_hex); supplied = bytes.fromhex(r.share1_hex)
            s1, s2 = m.xor_split(secret, supplied)
            recovered = m.xor_reconstruct(s1, s2)
            records.append({"vector_id": r.vector_id, "classification": "deterministic_test_vector",
                            "share1_hex": s1.hex(), "share2_hex": s2.hex(),
                            "reconstructed_secret_hex": recovered.hex(), "valid": recovered == secret})
        out = pd.DataFrame(records)
    elif number in (16, 17):
        x = _rows("shamir_prime521_test_vectors.csv")
        records = []
        for vector, group in x.groupby("vector_id", sort=False):
            secret = int(group.secret_hex.iloc[0], 16)
            coefficients = [int(v, 16) for v in json.loads(group.coefficients_hex_json.iloc[0])]
            shares = [(int(r.x), m.shamir_evaluate(secret, coefficients, int(r.x))) for r in group.itertuples()]
            recovered = m.shamir_reconstruct(shares[:len(coefficients)+1])
            records.append({"vector_id": vector, "classification": "deterministic_test_vector",
                            "field_profile": "prime521-v1", "threshold": len(coefficients)+1,
                            "shares_json": json.dumps([[x, hex(y)] for x, y in shares]),
                            "reconstructed_secret_hex": f"{recovered:064x}", "valid": recovered == secret})
        out = pd.DataFrame(records)
    elif number in (18, 19, 20):
        x = _rows("partition_scenarios.csv")
        records = []
        for r in x.itertuples():
            unit, expected = m.partition_expected_loss(r.wealth, int(r.n), r.p)
            record = {"scenario_id": r.scenario_id, "classification": r.classification,
                      "n": int(r.n), "unit_value": unit, "expected_loss": expected}
            if number == 19:
                record["loss_variance"] = m.equicorrelated_variance(r.wealth, int(r.n), r.p, r.rho)
            if number == 20:
                record["catastrophic_loss_probability"] = m.catastrophic_loss_probability(int(r.n), r.p, r.q)
            records.append(record)
        out = pd.DataFrame(records)
    elif number == 21:
        x = _rows("optimization_scenarios.csv")
        records = []
        for r in x.itertuples():
            values = m.partition_objective(r.wealth, int(r.n), r.p, r.q, r.risk_weight,
                                           r.alpha, r.fixed_cost, r.cost_per_partition)
            records.append({"scenario_id": r.scenario_id, "classification": r.classification,
                            "n": int(r.n), **values})
        out = pd.DataFrame(records)
        out["is_minimum"] = out.groupby("scenario_id")["objective"].transform("min").eq(out["objective"])
    else:
        raise ValueError("equation number must lie in 1..21")
    return _write(number, out.copy(), output_path)


def run_all() -> list[Path]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    return [run_equation(number) for number in range(1, 22)]

