"""Exercise 2: assign each rule to a layer. Run:  pytest tests/test_w04_modeling.py"""

# Replace each "" with "bronze", "silver" or "gold".
RULE_LAYER = {
    "keeps rows exactly as received, including duplicates": "bronze",
    "removes duplicate transactions": "silver",
    "casts timestamp strings to timestamp type": "silver",
    "daily sales per store joined to weather": "gold",
    "adds _source_file lineage column": "bronze",
    "quarantines rows with unparseable timestamps": "silver",
}
