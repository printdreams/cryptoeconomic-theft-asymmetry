import pandas as pd

from theft_asymmetry.runner import EQUATIONS, ROOT, run_all, run_equation


def test_all_equations_generate_nonempty_csvs():
    paths = run_all()
    assert len(paths) == 23
    for path in paths:
        assert path.exists()
        assert not pd.read_csv(path).empty


def test_registry_covers_all_equations_and_scripts():
    registry = pd.read_csv(ROOT / "data" / "equation_registry.csv")
    assert registry.equation.tolist() == [str(number) for number in EQUATIONS]
    assert all((ROOT / path).exists() for path in registry.script)


def test_invalid_cross_domain_comparisons_remain_nonestimates():
    run_all()
    rvr = pd.read_csv(ROOT / "data" / "output" / "eq10_results.csv")
    row = rvr.loc[rvr.scenario_id == "cash_crypto_unmatched"].iloc[0]
    assert row.status == "not_estimated"
    dr = pd.read_csv(ROOT / "data" / "output" / "eq06_results.csv")
    row = dr.loc[dr.scenario_id == "unmatched_public_sources"].iloc[0]
    assert row.status == "not_estimated"


def test_equation_extensions_have_reproducible_known_answers(tmp_path):
    for number, column, expected in [('21a', 'expected_net_loss', 62.5),
                                     ('21b', 'net_loss_variance', 6718.75)]:
        path = run_equation(number, tmp_path / f'{number}.csv')
        frame = pd.read_csv(path)
        assert set(frame.equation) == {number}
        assert frame.loc[frame.scenario_id == 'unequal_dependent_recovery', column].iloc[0] == expected
