
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import (
    proportions_ztest,
    confint_proportions_2indep,
)


def validate_experiment(data, alpha=0.05):
    control = data[data["assigned_treatment"] == 0]["converted"]
    treatment = data[data["assigned_treatment"] == 1]["converted"]

    control_n = len(control)
    treatment_n = len(treatment)

    control_conversions = int(control.sum())
    treatment_conversions = int(treatment.sum())

    control_rate = control_conversions / control_n
    treatment_rate = treatment_conversions / treatment_n

    observed_effect = treatment_rate - control_rate

    count = np.array([
        treatment_conversions,
        control_conversions,
    ])

    nobs = np.array([treatment_n, control_n])

    z_stat, p_value = proportions_ztest(
        count,
        nobs,
        alternative="two-sided",
    )

    ci_low, ci_high = confint_proportions_2indep(
        treatment_conversions,
        treatment_n,
        control_conversions,
        control_n,
        method="newcomb",
        alpha=alpha,
    )

    return {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "observed_effect": observed_effect,
        "confidence_interval": (ci_low, ci_high),
        "z_statistic": z_stat,
        "p_value": p_value,
        "significant": p_value < alpha,
        "alpha": alpha,
    }
