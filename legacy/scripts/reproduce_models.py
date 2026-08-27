# SPDX-License-Identifier: MIT
# Copyright (a) 2026 Alex Breton
#!/usr/bin/env python3
"""
Reproducibility Script for Cryptoeconomic Theft Asymmetry Research Report.
Python Version Target: 3.10+
Calculates direct loss rates, relative vulnerability ratios (RVR), clearance gaps,
and value partitioning variance reduction models.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def load_raw_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    loss_df = pd.read_csv(data_dir / "raw_monetary_loss_data.csv")
    clearance_df = pd.read_csv(data_dir / "raw_clearance_data.csv")
    return loss_df, clearance_df


def compute_monetary_loss_asymmetry(loss_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates Loss Rate (Lr) and Relative Vulnerability Ratio (RVR)."""
    df = loss_df.copy()

    # Calculate Annual Direct Loss Rate (Lr)
    df["annual_loss_rate"] = df["annual_losses_usd"] / df["supply_pool_usd"]
    df["annual_loss_rate_pct"] = df["annual_loss_rate"] * 100

    # Extract specific Loss Rates for RVR denominators
    lr_vault = df.loc[
        df["asset_class"] == "Physical Bank Vault Cash", "annual_loss_rate"
    ].values[0]
    lr_cash_agg = df.loc[
        df["asset_class"] == "Physical Cash Aggregate", "annual_loss_rate"
    ].values[0]

    # Calculate RVR relative to Vault Cash and Aggregate Physical Cash
    df["rvr_vs_vault"] = df["annual_loss_rate"] / lr_vault
    df["rvr_vs_cash_agg"] = df["annual_loss_rate"] / lr_cash_agg

    return df


def compute_clearance_enforcement_gap(
    clearance_df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculates Deterrence Deficit Ratios (DR) between physical and digital crime enforcement."""
    df = clearance_df.copy()

    # Calculate midpoints for reporting
    df["clearance_rate_midpoint"] = (
        df["clearance_rate_min"] + df["clearance_rate_max"]
    ) / 2
    df["conviction_prob_midpoint"] = (
        df["conviction_prob_min"] + df["conviction_prob_max"]
    ) / 2

    # Physical baseline conviction midpoints
    p_phys_min = df.loc[
        df["offense_category"] == "Physical Cash Larceny", "conviction_prob_min"
    ].values[0]
    p_phys_max = df.loc[
        df["offense_category"] == "Physical Cash Larceny", "conviction_prob_max"
    ].values[0]
    p_phys_mid = df.loc[
        df["offense_category"] == "Physical Cash Larceny",
        "conviction_prob_midpoint",
    ].values[0]

    # Digital conviction bounds
    p_dig_min = df.loc[
        df["offense_category"] == "Digital Asset Exploit", "conviction_prob_min"
    ].values[0]
    p_dig_max = df.loc[
        df["offense_category"] == "Digital Asset Exploit", "conviction_prob_max"
    ].values[0]
    p_dig_mid = df.loc[
        df["offense_category"] == "Digital Asset Exploit",
        "conviction_prob_midpoint",
    ].values[0]

    # Deterrence Deficit Ratios
    dr_min = p_phys_min / p_dig_max  # ~33.3x
    dr_max = p_phys_max / p_dig_min  # ~900x
    dr_mid = p_phys_mid / p_dig_mid  # ~157.1x

    print(
        f"[Clearance Model Output] Deterrence Deficit Range: {dr_min:.2f}x to {dr_max:.2f}x (Midpoint: {dr_mid:.2f}x)"
    )

    return df


def simulate_value_partitioning(
    wealth_usd: float = 1_000_000.0,
    p_compromise: float = 1e-4,
    partitions: list[int] = [1, 2, 5, 10, 50, 100],
) -> pd.DataFrame:
    """Executes Security Proof 3 variance reduction and tail-risk exponential decay simulations."""
    results = []
    for N in partitions:
        w_i = wealth_usd / N
        expected_loss = p_compromise * wealth_usd
        loss_variance = (
            p_compromise * (1.0 - p_compromise) * (wealth_usd**2)
        ) / N
        prob_total_loss = p_compromise**N

        results.append(
            {
                "partition_count_N": N,
                "unit_value_usd": w_i,
                "expected_loss_usd": expected_loss,
                "loss_variance": loss_variance,
                "loss_std_dev_usd": np.sqrt(loss_variance),
                "prob_catastrophic_total_loss": prob_total_loss,
            }
        )

    return pd.DataFrame(results)


def main():
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / "data"
    output_dir = root_dir / "outputs"
    output_dir.mkdir(exist_ok=True)

    print("=== Cryptoeconomic Theft Asymmetry Reproduction Suite ===")
    loss_raw, clearance_raw = load_raw_data(data_dir)

    # 1. Compute Loss Asymmetry
    loss_summary = compute_monetary_loss_asymmetry(loss_raw)
    loss_summary.to_csv(
        output_dir / "table1_monetary_loss_asymmetry.csv", index=False
    )
    print("\nTable 1 Exported Successfully.")
    print(
        loss_summary[
            [
                "asset_class",
                "annual_loss_rate_pct",
                "rvr_vs_cash_agg",
                "rvr_vs_vault",
            ]
        ]
    )

    # 2. Compute Clearance Gap
    clearance_summary = compute_clearance_enforcement_gap(clearance_raw)
    clearance_summary.to_csv(
        output_dir / "table2_clearance_enforcement_gap.csv", index=False
    )
    print("\nTable 2 Exported Successfully.")

    # 3. Simulate Value Partitioning
    partition_df = simulate_value_partitioning()
    partition_df.to_csv(output_dir / "value_partitioning_model.csv", index=False)
    print("\nValue Partitioning Simulation Exported Successfully.")
    print(
        partition_df[
            [
                "partition_count_N",
                "unit_value_usd",
                "loss_std_dev_usd",
                "prob_catastrophic_total_loss",
            ]
        ]
    )


if __name__ == "__main__":
    main()
