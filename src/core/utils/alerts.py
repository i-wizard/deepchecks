import statistics

class AlertChecker:
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.values = []

    def check_threshold(self, value: float) -> bool:
        return value > self.threshold

    def has_outlier(self, value: float) -> bool:
        self.values.append(value)
        mean = statistics.mean(self.values)
        stdev = statistics.stdev(self.values) if len(self.values) > 1 else 0
        return abs(value - mean) > 2 * stdev