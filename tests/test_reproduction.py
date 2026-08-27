import pandas as pd

from theft_asymmetry.runner import ROOT, run_all


def test_all_21_equations_generate_nonempty_csvs():
    paths = run_all()
    assert len(paths) == 21
    for path in paths:
        assert path.exists()
        assert not pd.read_csv(path).empty


def test_registry_covers_all_equations_and_scripts():
    registry = pd.read_csv(ROOT / "data" / "equation_registry.csv")
    assert registry.equation.tolist() == list(range(1, 22))
    assert all((ROOT / path).exists() for path in registry.script)


def test_invalid_cross_domain_comparisons_remain_nonestimates():
    run_all()
    rvr = pd.read_csv(ROOT / "data" / "output" / "eq10_results.csv")
    row = rvr.loc[rvr.scenario_id == "cash_crypto_unmatched"].iloc[0]
    assert row.status == "not_estimated"
    dr = pd.read_csv(ROOT / "data" / "output" / "eq06_results.csv")
    row = dr.loc[dr.scenario_id == "unmatched_public_sources"].iloc[0]
    assert row.status == "not_estimated"

