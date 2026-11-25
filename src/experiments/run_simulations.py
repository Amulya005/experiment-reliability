
import pandas as pd

from src.data.generate_experiments import generate_experiment
from src.statistics.validate_experiment import validate_experiment


def run_simulations(
    repetitions=1000,
    n_users=10000,
    baseline_conversion_rate=0.10,
    treatment_effect=0.02,
    alpha=0.05,
    starting_seed=1000,
):
    results = []

    for iteration in range(repetitions):
        seed = starting_seed + iteration

        data, metadata = generate_experiment(
            n_users=n_users,
            baseline_conversion_rate=baseline_conversion_rate,
            treatment_effect=treatment_effect,
            seed=seed,
        )

        analysis = validate_experiment(data, alpha=alpha)

        results.append({
            "iteration": iteration + 1,
            "seed": seed,
            "n_users": n_users,
            "true_effect": metadata["true_ate"],
            "observed_effect": analysis["observed_effect"],
            "p_value": analysis["p_value"],
            "significant": analysis["significant"],
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    results = run_simulations(repetitions=1000)

    print("\n========== SIMULATION SUMMARY ==========")
    print("Total simulations:", len(results))
    print("Significant results:", results["significant"].sum())
    print(
        "Empirical power:",
        round(results["significant"].mean(), 4),
    )
    print(
        "Average observed effect:",
        round(results["observed_effect"].mean(), 6),
    )

    results.to_csv(
        "reports/clean_baseline_simulations.csv",
        index=False,
    )

    print("Results saved to reports/clean_baseline_simulations.csv")
