# Questions to ask Murphy USA

Pick 4 or 5 per interview. Listen for answers that tell you what week 1 on the job looks like.

## Cloud and platform
- Which cloud provider does the data platform run on, and is Databricks managed centrally or by each team?
- How is the data lake organized (medallion layers, Unity Catalog, workspace per environment)?
- How are environments split (dev, test, prod), and how does code get promoted?

## Orchestration and DevOps
- Do pipelines run as Databricks Jobs/Workflows or in another orchestrator? How are retries and alerting handled?
- How is infrastructure managed (Terraform repos, who reviews changes)?
- What does CI look like for pipeline code: linting, unit tests, integration tests on sample data?

## Data
- What are the main sources (point of sale, fuel, loyalty, supplier files)? Are they batch, near real time, or both?
- How do you currently measure data quality, and who owns fixing issues upstream?
- Which downstream consumers matter most (BI, forecasting, pricing, store operations)?

## Team and growth
- How is the data team structured, and who would I work with day to day?
- What does a good first 90 days look like for a new data engineer with a software background?
- How do you support learning (mentoring, certifications, code review culture)?
- What is the hardest data problem the team is working on right now?
