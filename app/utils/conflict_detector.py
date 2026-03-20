def detect_conflicts(sources):
    conflicts = []
    drug_map = {}

    # Build drug map
    for source in sources:
        for med in source["medications"]:
            name = med["name"].lower()

            if name not in drug_map:
                drug_map[name] = []

            drug_map[name].append({
                "source": source["type"],
                "dosage": med["dosage"],
                "status": med["status"]
            })

    # Dosage + status conflicts
    for drug, entries in drug_map.items():
        dosages = set([e["dosage"] for e in entries])
        if len(dosages) > 1:
            conflicts.append({
                "drug": drug,
                "type": "dosage_mismatch",
                "details": entries,
                "resolved": False
            })

        statuses = set([e["status"] for e in entries])
        if "active" in statuses and "stopped" in statuses:
            conflicts.append({
                "drug": drug,
                "type": "status_conflict",
                "details": entries,
                "resolved": False
            })

    # Simple interaction rule
    bad_combinations = [
        ("aspirin", "ibuprofen")
    ]

    drugs = list(drug_map.keys())

    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            d1, d2 = drugs[i], drugs[j]
            if (d1, d2) in bad_combinations or (d2, d1) in bad_combinations:
                conflicts.append({
                    "type": "drug_interaction",
                    "drugs": [d1, d2],
                    "resolved": False
                })

    return conflicts