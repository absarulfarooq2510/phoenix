"""
Deviation Detection Engine for Phoenix

This module evaluates incoming telemetry values against
learned baselines to determine how unusual a signal is.

It does NOT:
- raise incidents
- correlate across components
- take autonomous actions

Its sole responsibility is to quantify deviation.
"""

class DeviationDetector:
    def __init__(self, baseline_learner, z_threshold=3.0):
        """
        Initialize the deviation detector.

        baseline_learner:
            Instance of BaselineLearner used to retrieve
            learned mean and standard deviation.

        z_threshold:
            Deviation score above which a signal is considered
            strongly unusual.
        """
        self.baseline_learner = baseline_learner
        self.z_threshold = z_threshold

    def evaluate(self, component, metric, value):
        """
        Evaluate a telemetry signal against its baseline.

        Returns:
            A dictionary containing deviation information,
            or None if baseline is not ready.
        """

        # Do not evaluate deviation until baseline is stable
        if not self.baseline_learner.is_baseline_ready(component, metric):
            return None

        mean, std_dev = self.baseline_learner.get_baseline(component, metric)

        # Guard against zero variance (flat signals)
        if std_dev == 0:
            return None

        # Calculate deviation score (z-score style)
        deviation_score = abs(value - mean) / std_dev

        # Classify deviation strength
        if deviation_score >= self.z_threshold:
            level = "strong"
        elif deviation_score >= 2.0:
            level = "mild"
        else:
            level = "normal"

        return {
            "component": component,
            "metric": metric,
            "value": value,
            "mean": round(mean, 3),
            "std_dev": round(std_dev, 3),
            "deviation_score": round(deviation_score, 3),
            "level": level
        }
