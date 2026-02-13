from config import MIN_GAP

def suppress_nearby(pattern_indices, min_gap=MIN_GAP):
    if not pattern_indices:
        return []

    pattern_indices = sorted(pattern_indices)
    filtered = [pattern_indices[0]]

    for idx in pattern_indices[1:]:
        if idx - filtered[-1] >= min_gap:
            filtered.append(idx)

    return filtered

