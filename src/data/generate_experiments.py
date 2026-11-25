
import numpy as np
import pandas as pd


def generate_experiment(
    n_users: int = 10_000,
    baseline_conversion_rate: float = 0.10,
    treatment_effect: float = 0.02,
    allocation_ratio: float = 0.50,
    seed: int = 42,
):
    """
    Generate a clean, randomized A/B experiment.

    treatment_effect is an absolute change in conversion probability.
    Example: 0.02 means a 2-percentage-point increase.
    """

    if not isinstance(n_users, int) or isinstance(n_users, bool) or n_users < 2:
        raise ValueError("n_users must be an integer of at least 2.")

    if not 0 < baseline_conversion_rate < 1:
        raise ValueError("baseline_conversion_rate must be between 0 and 1.")

    if not 0 < allocation_ratio < 1:
        raise ValueError("allocation_ratio must be between 0 and 1.")

    treatment_conversion_rate = (
        baseline_conversion_rate + treatment_effect
    )

    if not 0 < treatment_conversion_rate < 1:
        raise ValueError(
            "The treatment conversion rate must be between 0 and 1."
        )

    rng = np.random.default_rng(seed)

    # Randomly assign users to control (0) or treatment (1).
    assigned_treatment = rng.binomial(
        n=1,
        p=allocation_ratio,
        size=n_users,
    )

    # Generate conversion outcomes using the assigned group.
    conversion_probabilities = np.where(
        assigned_treatment == 1,
        treatment_conversion_rate,
        baseline_conversion_rate,
    )

    converted = rng.binomial(
        n=1,
        p=conversion_probabilities,
        size=n_users,
    )

    data = pd.DataFrame(
        {
            "user_id": np.arange(1, n_users + 1),
            "assigned_treatment": assigned_treatment,
            "exposed_treatment": assigned_treatment.copy(),
            "converted": converted,
        }
    )

    metadata = {
        "scenario": "clean_experiment",
        "seed": seed,
        "n_users": n_users,
        "allocation_ratio": allocation_ratio,
        "true_control_rate": baseline_conversion_rate,
        "true_treatment_rate": treatment_conversion_rate,
        "true_ate": treatment_effect,
    }

    return data, metadata
