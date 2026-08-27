"""Reference implementations of the manuscript's 21 numbered equations.

The functions are deliberately small and side-effect free.  Empirical estimates
and illustrative scenarios remain distinguishable in every output table.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from math import log
from typing import Iterable

import numpy as np
import pandas as pd


PRIME_521 = (1 << 521) - 1


def utility(x: float, family: str = "linear", gamma: float = 1.0) -> float:
    """Utility used by Equation 1; CRRA/log utilities require positive wealth."""
    if family == "linear":
        return x
    if x <= 0:
        raise ValueError("log and CRRA utility require strictly positive wealth")
    if family == "log" or (family == "crra" and gamma == 1.0):
        return log(x)
    if family == "crra":
        return (x ** (1.0 - gamma)) / (1.0 - gamma)
    raise ValueError(f"unsupported utility family: {family}")


def expected_utility(q: float, p: float, y: float, g: float, c: float,
                     f: float, r: float, family: str = "linear",
                     gamma: float = 1.0) -> float:
    """Equation 1."""
    _probabilities(q=q, p=p)
    return q * ((1 - p) * utility(y + g - c, family, gamma)
                + p * utility(y + g - c - f - r, family, gamma)) \
        + (1 - q) * utility(y - c, family, gamma)


def risk_neutral_payoff(q: float, p: float, g: float, c: float,
                        f: float, r: float) -> float:
    """Equation 2."""
    _probabilities(q=q, p=p)
    return q * g - c - q * p * (f + r)


def attack_portfolio(fixed_cost: float, targets: Iterable[dict]) -> float:
    """Equation 3."""
    return -fixed_cost + sum(risk_neutral_payoff(
        float(x["q"]), float(x["p"]), float(x["gain"]),
        float(x["marginal_cost"]), float(x["penalty"]), float(x["recovery"])
    ) for x in targets)


def enforcement_transition(n_previous: int, n_current: int) -> float:
    """Equation 4."""
    if n_previous <= 0 or n_current < 0 or n_current > n_previous:
        raise ValueError("stage counts must satisfy 0 <= n_current <= n_previous")
    return n_current / n_previous


def enforcement_cohort_probability(counts: Iterable[int]) -> tuple[float, float]:
    """Equation 5; returns the product of transitions and telescoping ratio."""
    values = list(counts)
    if len(values) < 2:
        raise ValueError("at least two stage counts are required")
    transitions = [enforcement_transition(a, b) for a, b in zip(values, values[1:])]
    return float(np.prod(transitions)), values[-1] / values[0]


def deterrence_ratio(p_cash: float, p_digital: float) -> float:
    """Equation 6; valid only for metadata-matched cohorts."""
    _probabilities(p_cash=p_cash, p_digital=p_digital)
    if p_digital <= 0:
        raise ValueError("p_digital must be greater than zero")
    return p_cash / p_digital


def loss_totals(events: pd.DataFrame) -> tuple[float, float]:
    """Equation 7."""
    gross = float(events["gross_loss"].sum())
    net = float((events["gross_loss"] - events["recovered_at_horizon"]).sum())
    if gross < 0 or net < 0 or (events["recovered_at_horizon"] < 0).any():
        raise ValueError("loss and recovery values must be non-negative")
    if (events["recovered_at_horizon"] > events["gross_loss"]).any():
        raise ValueError("event recovery cannot exceed event gross loss")
    return gross, net


def time_weighted_exposure(observations: pd.DataFrame) -> float:
    """Equation 8, evaluated by trapezoidal integration over dated observations."""
    frame = observations.sort_values("timestamp").copy()
    times = pd.to_datetime(frame["timestamp"], utc=True)
    if len(frame) < 2:
        raise ValueError("at least two exposure observations are required")
    seconds = (times - times.iloc[0]).dt.total_seconds().to_numpy(dtype=float)
    if seconds[-1] <= 0 or np.any(np.diff(seconds) <= 0):
        raise ValueError("timestamps must be unique and strictly increasing")
    values = frame["exposed_value"].to_numpy(dtype=float)
    if np.any(values < 0):
        raise ValueError("exposure cannot be negative")
    return float(np.trapezoid(values, seconds) / seconds[-1])


def loss_intensities(gross: float, net: float, exposure: float) -> tuple[float, float]:
    """Equation 9."""
    if exposure <= 0 or gross < 0 or net < 0 or net > gross:
        raise ValueError("require exposure > 0 and 0 <= net <= gross")
    return gross / exposure, net / exposure


COMPARABILITY_FIELDS = (
    "period", "geography", "asset_perimeter", "custody_perimeter",
    "event_definition", "loss_convention", "valuation_rule",
    "exposure_concept", "reporting_coverage",
)


def relative_vulnerability_ratio(a: dict, b: dict) -> float:
    """Equation 10, with mandatory metadata comparability gate."""
    mismatches = [field for field in COMPARABILITY_FIELDS if a.get(field) != b.get(field)]
    if mismatches:
        raise ValueError("unmatched RVR metadata: " + ", ".join(mismatches))
    denominator = float(b["gross_loss_intensity"])
    if denominator <= 0:
        raise ValueError("RVR denominator must be positive")
    return float(a["gross_loss_intensity"]) / denominator


def cash_gross_intensity(gross_stolen: float, currency_stock: float) -> float:
    """Equation 11."""
    return gross_stolen / currency_stock


def cash_recovery_share(recovered: float, gross_stolen: float) -> float:
    """Equation 12."""
    return recovered / gross_stolen


def cash_net_intensity(gross_stolen: float, recovered: float,
                       currency_stock: float) -> float:
    """Equation 13."""
    return (gross_stolen - recovered) / currency_stock


def xor_split(secret: bytes, share1: bytes) -> tuple[bytes, bytes]:
    """Equation 14. The supplied share must be independent, uniform, and one-time."""
    if len(secret) != 32 or len(share1) != 32:
        raise ValueError("XOR profile requires two 32-byte values")
    return share1, bytes(a ^ b for a, b in zip(secret, share1))


def xor_reconstruct(share1: bytes, share2: bytes) -> bytes:
    """Equation 15."""
    if len(share1) != len(share2) or len(share1) != 32:
        raise ValueError("XOR shares must both be 32 bytes")
    return bytes(a ^ b for a, b in zip(share1, share2))


def shamir_evaluate(secret: int, coefficients: list[int], x: int,
                    prime: int = PRIME_521) -> int:
    """Equation 16 over the versioned prime521-v1 field profile."""
    if not 0 <= secret < prime or not 0 < x < prime:
        raise ValueError("secret and non-zero share index must be field elements")
    y = secret
    power = x
    for coefficient in coefficients:
        if not 0 <= coefficient < prime:
            raise ValueError("coefficient is outside the field")
        y = (y + coefficient * power) % prime
        power = (power * x) % prime
    return y


def shamir_reconstruct(shares: list[tuple[int, int]], prime: int = PRIME_521) -> int:
    """Equation 17: Lagrange interpolation at zero in the selected field."""
    if not shares:
        raise ValueError("at least one share is required")
    xs = [x for x, _ in shares]
    if len(xs) != len(set(xs)) or any(x <= 0 or x >= prime for x in xs):
        raise ValueError("share indices must be distinct, non-zero field elements")
    secret = 0
    for i, (x_i, y_i) in enumerate(shares):
        numerator = 1
        denominator = 1
        for ell, (x_l, _) in enumerate(shares):
            if ell != i:
                numerator = numerator * x_l % prime
                denominator = denominator * (x_l - x_i) % prime
        basis = numerator * pow(denominator, -1, prime) % prime
        secret = (secret + y_i * basis) % prime
    return secret


def partition_expected_loss(wealth: float, n: int, p: float) -> tuple[float, float]:
    """Equation 18; returns unit value and expected total loss."""
    _partition_inputs(wealth, n, p)
    return wealth / n, p * wealth


def equicorrelated_variance(wealth: float, n: int, p: float, rho: float) -> float:
    """Equation 19."""
    _partition_inputs(wealth, n, p)
    lower = -1 / (n - 1) if n > 1 else 0.0
    if not lower <= rho <= 1:
        raise ValueError(f"rho must be in [{lower}, 1] for an equicorrelation matrix")
    return wealth**2 * p * (1 - p) * (1 / n + rho * (n - 1) / n)


def catastrophic_loss_probability(n: int, p: float, q: float) -> float:
    """Equation 20."""
    _partition_inputs(1.0, n, p)
    _probabilities(q=q)
    return q + (1 - q) * p**n


def loss_distribution(wealth: float, n: int, p: float, q: float) -> tuple[np.ndarray, np.ndarray]:
    """Exact common-mode/binomial loss distribution used for Equation 21."""
    _partition_inputs(wealth, n, p)
    _probabilities(q=q)
    losses = wealth * np.arange(n + 1) / n
    from math import comb
    probabilities = np.array([(1 - q) * comb(n, k) * p**k * (1 - p)**(n-k)
                              for k in range(n + 1)], dtype=float)
    probabilities[-1] += q
    return losses, probabilities


def discrete_cvar(losses: np.ndarray, probabilities: np.ndarray, alpha: float) -> float:
    """Upper-tail CVaR with fractional probability mass at the discrete boundary."""
    if not 0 <= alpha < 1:
        raise ValueError("alpha must satisfy 0 <= alpha < 1")
    tail_mass = 1 - alpha
    remaining = tail_mass
    total = 0.0
    for loss, probability in zip(losses[::-1], probabilities[::-1]):
        take = min(remaining, probability)
        total += take * loss
        remaining -= take
        if remaining <= 1e-15:
            break
    if remaining > 1e-10:
        raise ValueError("probabilities do not sum to one")
    return total / tail_mass


def partition_objective(wealth: float, n: int, p: float, q: float,
                        risk_weight: float, alpha: float,
                        fixed_cost: float, cost_per_partition: float) -> dict:
    """Equation 21 for a specified feasible N."""
    losses, probabilities = loss_distribution(wealth, n, p, q)
    expected = float(np.dot(losses, probabilities))
    cvar = discrete_cvar(losses, probabilities, alpha)
    cost = fixed_cost + cost_per_partition * n
    return {"expected_loss": expected, "cvar": cvar, "cost": cost,
            "objective": expected + risk_weight * cvar + cost}


def _probabilities(**values: float) -> None:
    for name, value in values.items():
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must lie in [0, 1]")


def _partition_inputs(wealth: float, n: int, p: float) -> None:
    if wealth < 0 or int(n) != n or n < 1:
        raise ValueError("wealth must be non-negative and N a positive integer")
    _probabilities(p=p)

