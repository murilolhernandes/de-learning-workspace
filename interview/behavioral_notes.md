# Behavioral notes

Fill in the blanks with your own real examples. Honest, specific stories beat polished ones.

## My background in one breath

New BS graduate in Software Development. Before that: client success, then construction superintendent. I coordinate people, schedules and problems under pressure, and I now build software and data pipelines.

## What the two careers give a data engineer

| Experience | Data engineering link |
|---|---|
| Construction superintendent: sequencing trades, dependencies, inspections | Pipeline orchestration: tasks, dependencies, retries, quality gates before the next step |
| Superintendent: daily logs, safety and quality checks | Data quality checks, audit trails, lineage |
| Client success: translating what a customer says into what they need | Gathering requirements from analysts and stores, asking about the business grain |
| Client success: owning an issue until it is resolved | On-call mindset, root-cause fixes, clear incident updates |
| Both: working with non-technical people | Explaining data issues in plain language |

## Stories to prepare (STAR: situation, task, action, result)

Write 4 to 6 bullets for each. Use real numbers where you can.

1. **A schedule or plan fell apart.** What did you re-sequence, and what was the result?
2. **A conflict with a client or crew.** How did you listen first, then resolve it?
3. **A mistake you owned.** What did you change so it would not repeat?
4. **Learning something fast.** (Good fit: this crash course.) What did you build and what did you learn?
5. **Explaining something complex simply.**
6. **Working under a deadline with incomplete information.**

## One page: how I would explain my learning plan

Use this out loud as an answer to "You have no data engineering experience. How will you get up to speed?"

**Opening.** "I am upfront that I am new to data engineering. What I bring is a software background and a habit of learning by building, so I made a plan instead of just reading."

**What I am doing.**
- I run a local Spark and Delta Lake workspace with synthetic retail data, shaped like your world: stores, fuel and merchandise transactions, loyalty and weather.
- Week 1 covered PySpark basics, Delta read and write, window functions, and the bronze, silver and gold idea.
- The next weeks go deeper on joins, MERGE upserts, schema evolution, partitioning and testing. After that: data modeling and quality checks, Terraform and CI at a read-and-explain level, and orchestration.
- The finish is a capstone: raw files to a daily sales and weather feature table, with tests, CI and a write-up of the tradeoffs.

**Why this order.** "PySpark and Delta are the core of the daily work, so I started there. I treat infrastructure and orchestration as things I can read, run and explain before I own them."

**What I will not claim.** "I have not run production pipelines or tuned large jobs. I can show you what I built, explain why I made each choice, and I know where I would ask for help."

**Closing.** "I expect to be useful on small, well-scoped tasks early, and to grow quickly with code review and mentoring."

Rewrite this in your own words. If it sounds like a script, shorten it.

## Mock interview checklist (20 minutes)

- [ ] 6 questions from `pyspark_questions.md`, answered aloud
- [ ] 2 questions from `sql_questions.md`, written on paper or in a SQL view
- [ ] 1 behavioral story (STAR) from above
- [ ] Your learning-plan answer, under 90 seconds
- [ ] 2 questions from `questions_to_ask.md`
