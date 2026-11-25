
from src.data.generate_experiments import generate_experiment


def test_experiment_has_expected_rows():
    data, metadata = generate_experiment(n_users=1000)

    assert len(data) == 1000
    assert metadata["n_users"] == 1000


def test_assignment_contains_two_groups():
    data, _ = generate_experiment(n_users=1000)

    assert set(data["assigned_treatment"].unique()) == {0, 1}


def test_outcome_is_binary():
    data, _ = generate_experiment(n_users=1000)

    assert set(data["converted"].unique()).issubset({0, 1})


def test_random_seed_is_reproducible():
    data1, _ = generate_experiment(seed=123)
    data2, _ = generate_experiment(seed=123)

    assert data1.equals(data2)


def test_true_effect_is_recorded():
    _, metadata = generate_experiment(treatment_effect=0.03)

    assert metadata["true_ate"] == 0.03


def test_invalid_conversion_rate_is_rejected():
    try:
        generate_experiment(baseline_conversion_rate=1.5)
    except ValueError:
        return

    raise AssertionError("Expected ValueError")
