from statsmodels.stats.multitest import multipletests
import pandas as pd
from statsmodels.stats.proportion import (
    proportions_ztest,
    confint_proportions_2indep,
)


def compare_groups(data, treatment, control="No E-Mail"):
    treatment_data = data[data["segment"] == treatment]
    control_data = data[data["segment"] == control]

    treatment_conversions = treatment_data["conversion"].sum()
    control_conversions = control_data["conversion"].sum()

    treatment_n = len(treatment_data)
    control_n = len(control_data)

    treatment_rate = treatment_conversions / treatment_n
    control_rate = control_conversions / control_n

    absolute_lift = treatment_rate - control_rate
    relative_lift = absolute_lift / control_rate

    count = [
        treatment_conversions,
        control_conversions,
    ]

    nobs = [
        treatment_n,
        control_n,
    ]

    z_stat, p_value = proportions_ztest(
        count,
        nobs,
    )

    ci_low, ci_high = confint_proportions_2indep(
        treatment_conversions,
        treatment_n,
        control_conversions,
        control_n,
        method="newcomb",
    )

    return {
        "treatment": treatment,
        "control": control,
        "treatment_n": treatment_n,
        "control_n": control_n,
        "treatment_rate": treatment_rate,
        "control_rate": control_rate,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "confidence_interval_low": ci_low,
        "confidence_interval_high": ci_high,
        "z_statistic": z_stat,
        "p_value": p_value,
    }


if __name__ == "__main__":
    df = pd.read_csv("data/raw/hillstrom.csv")

    results = []

    for group in ["Mens E-Mail", "Womens E-Mail"]:
        results.append(compare_groups(df, group))

    raw_p_values = [result["p_value"] for result in results]

    reject, adjusted_p_values, _, _ = multipletests(
        raw_p_values,
        alpha=0.05,
        method="holm",
    )

    for result, adjusted_p, is_significant in zip(
        results,
        adjusted_p_values,
        reject,
    ):
        print(f"\n========== {result['treatment']} vs No E-Mail ==========")

        for key, value in result.items():
            print(f"{key}: {value}")

        print("Holm-adjusted p-value:", adjusted_p)
        print("Significant after correction:", is_significant)