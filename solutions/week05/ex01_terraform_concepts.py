"""Solution: Terraform and CI concepts."""

FACTS = {
    "plan_changes_real_infrastructure": False,
    "apply_changes_real_infrastructure": True,
    "state_should_be_committed_to_git": False,
    "variables_let_one_config_serve_dev_and_prod": True,
    "credentials_belong_in_tf_files": False,
}

CI_LINT_COMMAND = "ruff check ."
CI_TEST_COMMAND = "pytest"
