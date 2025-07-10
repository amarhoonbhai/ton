
def detect_upgrade_changes(old_gift, new_gift):
    old_levels = {lvl["level"]: lvl["upgradeCost"] for lvl in old_gift.get("levels", [])}
    new_levels = {lvl["level"]: lvl["upgradeCost"] for lvl in new_gift.get("levels", [])}

    changes = []
    for level, new_cost in new_levels.items():
        old_cost = old_levels.get(level)
        if old_cost is not None and old_cost != new_cost:
            is_final = level == max(new_levels.keys())
            label = "Final" if is_final else f"Level {level}"
            changes.append(f"• {label} — upgrade: {old_cost} → {new_cost}")
    return changes
