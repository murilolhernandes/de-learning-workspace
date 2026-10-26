RULE_LAYER = {
    "keeps rows exactly as received, including duplicates": "bronze",
    "removes duplicate transactions": "silver",
    "casts timestamp strings to timestamp type": "silver",
    "daily sales per store joined to weather": "gold",
    "adds _source_file lineage column": "bronze",
    "quarantines rows with unparseable timestamps": "silver",
}
