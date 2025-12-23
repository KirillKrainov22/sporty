LEVELS = [
    0,
    50,
    250,
    1000,
    2500,
    5000,
    15000,
    30000,
]


def calc_level(total_points: int) -> int:
    lvl = 1
    for i, threshold in enumerate(LEVELS):
        if total_points >= threshold:
            lvl = i + 1
    return lvl