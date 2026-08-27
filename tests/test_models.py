import pandas as pd
import pytest

from theft_asymmetry import models as m


def test_equation_1_reduces_to_equation_2_under_linear_utility():
    args = dict(q=.35, p=.08, g=25000, c=3000, f=50000, r=10000)
    eu = m.expected_utility(y=100000, family="linear", gamma=0, **args)
    assert eu - 100000 == pytest.approx(m.risk_neutral_payoff(**args))


def test_equations_4_and_5_telescope():
    product, ratio = m.enforcement_cohort_probability([1000, 720, 180, 72, 50, 40])
    assert product == pytest.approx(.04)
    assert product == pytest.approx(ratio)


def test_equations_7_to_9():
    events = pd.DataFrame({"gross_loss": [80., 20.], "recovered_at_horizon": [10., 5.]})
    assert m.loss_totals(events) == (100., 85.)
    exposure = pd.DataFrame({"timestamp": ["2025-01-01", "2026-01-01"], "exposed_value": [1000., 1000.]})
    assert m.time_weighted_exposure(exposure) == pytest.approx(1000.)
    assert m.loss_intensities(100., 85., 1000.) == pytest.approx((.1, .085))


def test_equation_10_rejects_unmatched_metadata():
    a = {field: "same" for field in m.COMPARABILITY_FIELDS}
    b = dict(a)
    a["gross_loss_intensity"] = .2
    b["gross_loss_intensity"] = .1
    assert m.relative_vulnerability_ratio(a, b) == pytest.approx(2)
    b["period"] = "different"
    with pytest.raises(ValueError, match="period"):
        m.relative_vulnerability_ratio(a, b)


def test_cash_calibration_equations_11_to_13():
    gross, recovered, stock = 1423559757, 36980933, 1759800000000
    assert m.cash_gross_intensity(gross, stock) == pytest.approx(0.0008089326951926355, abs=1e-15)
    assert m.cash_recovery_share(recovered, gross) == pytest.approx(0.025977787597714453, abs=1e-15)
    assert m.cash_net_intensity(gross, recovered, stock) == pytest.approx(0.0007879184134560746, abs=1e-15)


def test_xor_equations_14_and_15():
    secret = bytes(range(32)); share = bytes(reversed(range(32)))
    s1, s2 = m.xor_split(secret, share)
    assert m.xor_reconstruct(s1, s2) == secret


def test_shamir_equations_16_and_17():
    secret = int.from_bytes(bytes(range(32)), "big")
    coefficients = [123456789, 987654321]
    shares = [(x, m.shamir_evaluate(secret, coefficients, x)) for x in range(1, 6)]
    assert m.shamir_reconstruct(shares[:3]) == secret
    assert m.shamir_reconstruct([shares[0], shares[2], shares[4]]) == secret


def test_partition_equations_18_to_20_boundaries():
    _, expected = m.partition_expected_loss(1_000_000, 10, .01)
    assert expected == pytest.approx(10_000)
    independent = m.equicorrelated_variance(1_000_000, 10, .01, 0)
    common = m.equicorrelated_variance(1_000_000, 10, .01, 1)
    assert common == pytest.approx(10 * independent)
    assert m.catastrophic_loss_probability(5, .01, .002) == pytest.approx(.002 + .998e-10)


def test_equation_21_distribution_and_cvar():
    losses, probabilities = m.loss_distribution(1_000_000, 10, .01, .002)
    assert probabilities.sum() == pytest.approx(1)
    result = m.partition_objective(1_000_000, 10, .01, .002, .5, .99, 500, 250)
    assert result["expected_loss"] == pytest.approx(11_980)
    assert result["cvar"] >= result["expected_loss"]
