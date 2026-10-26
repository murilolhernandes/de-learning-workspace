from pathlib import Path

from conftest import load_exercise

ex = load_exercise("05_terraform_ci", "ex01_terraform_concepts")
TF_DIR = Path(__file__).resolve().parents[1] / "weeks" / "05_terraform_ci" / "infra" / "terraform"


def test_facts():
    assert ex.FACTS == {
        "plan_changes_real_infrastructure": False,
        "apply_changes_real_infrastructure": True,
        "state_should_be_committed_to_git": False,
        "variables_let_one_config_serve_dev_and_prod": True,
        "credentials_belong_in_tf_files": False,
    }


def test_ci_commands():
    assert ex.CI_LINT_COMMAND == "ruff check ."
    assert ex.CI_TEST_COMMAND == "pytest"


def test_terraform_files_present_and_never_hold_secrets():
    for name in ("main.tf", "variables.tf", "outputs.tf"):
        text = (TF_DIR / name).read_text().lower()
        assert "token" not in text and "password" not in text
