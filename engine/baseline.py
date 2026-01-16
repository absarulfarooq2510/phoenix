"""
Baseline Learning Engine for Phoenix

This module is responsible for learning what 'normal' behavior
looks like for each (component, metric) pair based on live telemetry.

It does NOT:
- detect anomalies
- raise incidents
- apply thresholds

Its only responsibility is to observe and summarize behavior.
"""

from collections import defaultdict
import math


class BaselineLearner:
    def __init__(self, min_samples=30):
        """
        Initialize the baseline learner.

        min_samples:
            Number of observations required before a baseline
            is considered stable and usable.
        """
        self.min_samples = min_samples

        # Data structure to store running statistics per signal.
        #
        # Structure:
        # {
        #   (component, metric): {
        #       "count": int,
        #       "mean": float,
        #       "m2": float   # helper value for variance calculation
        #   }
        # }
        self.stats = defaultdict(lambda: {
            "count": 0,
            "mean": 0.0,
            "m2": 0.0
        })

    def update(self, component, metric, value):
        """
        Update baseline statistics for a given telemetry signal.

        Uses Welford's algorithm for numerically stable
        incremental mean and variance calculation.
        """

        key = (component, metric)
        record = self.stats[key]

        record["count"] += 1
        count = record["count"]

        # Incremental mean update
        delta = value - record["mean"]
        record["mean"] += delta / count

        # Incremental variance helper update
        delta2 = value - record["mean"]
        record["m2"] += delta * delta2

    def is_baseline_ready(self, component, metric):
        """
        Check if enough data has been collected to trust the baseline.
        """
        return self.stats[(component, metric)]["count"] >= self.min_samples

    def get_baseline(self, component, metric):
        """
        Retrieve baseline statistics for a signal.

        Returns:
            mean, standard_deviation

        Raises:
            ValueError if baseline is not yet ready.
        """
        record = self.stats[(component, metric)]

        if record["count"] < self.min_samples:
            raise ValueError("Baseline not ready yet")

        variance = record["m2"] / (record["count"] - 1)
        std_dev = math.sqrt(variance)

        return record["mean"], std_dev
