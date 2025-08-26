import statistics
from typing import Sequence


def zscore(series: Sequence[float]) -> float:
    if not series:
        return 0.0
    mean = statistics.mean(series)
    stdev = statistics.stdev(series) if len(series) > 1 else 1e-9
    return (series[-1] - mean) / stdev