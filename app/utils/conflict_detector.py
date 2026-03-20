def detect_conflicts(sources):
    med_map = {}

    for source in sources:
        for med in source["medications"]:
            name = med["name"].lower()

            if name not in med_map:
                med_map[name] = []

            med_map[name].append({
                "dosage": med["dosage"],
                "frequency": med["frequency"],
                "status": med["status"],
                "source": source["type"]
            })

    conflicts = []

    for med_name, entries in med_map.items():
        
        dosages = set(e["dosage"] for e in entries)
        statuses = set(e["status"] for e in entries)

        # 1. Dosage mismatch
        if len(dosages) > 1:
            conflicts.append({
                "medication": med_name,
                "type": "DOSAGE_MISMATCH",
                "details": list(dosages)
            })

        # 2. Active vs Stopped
        if "active" in statuses and "stopped" in statuses:
            conflicts.append({
                "medication": med_name,
                "type": "STATUS_CONFLICT",
                "details": list(statuses)
            })

    return conflicts