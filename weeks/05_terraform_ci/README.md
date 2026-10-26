# Week 5: Terraform and CI

## Goal
Read, validate and explain Terraform files, and understand the CI workflow that lints and tests this repo. Read-and-explain level, not mastery.

## Concepts
- Terraform: declarative infrastructure. You describe the end state; `plan` shows the diff
- Provider, resource, variable, output, module
- State: Terraform's record of what it manages (never commit it, it can hold secrets)
- CI: every push runs lint (`ruff`) and tests (`pytest`)

## Steps
1. Read `infra/terraform/main.tf`, `variables.tf`, `outputs.tf` (generic bucket + Databricks workspace; nothing is ever applied).
2. `ex01_terraform_concepts.py`: answer the concept questions.
3. Read `.github/workflows/ci.yml` and the `Makefile`; note which command CI runs for lint and for tests.
4. Terraform is not installed here. If you install it, you may run only `terraform init -backend=false`, `terraform validate` and `terraform plan`. Never `apply`.

## How to check your work
```
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w05_terraform.py
```

## Self-test questions
1. What is Terraform state, and why must it not be committed?
2. What does `plan` do that `apply` does not?
3. Why does CI run on every push instead of before release?
