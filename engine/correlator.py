"""
Topology-Aware Correlation Engine for Phoenix

This module groups and evaluates deviations across components
to identify system-level degradation patterns.

It does NOT:
- raise incidents
- decide severity
- auto-remediate

Its only job is to connect related deviations.
"""

from collections import defaultdict
from datetime import datetime, timedelta


class Correlator:
    def __init__(self, topology, time_window_seconds=30):
        """
        Initialize the correlator.

        topology:
            Parsed topology containing nodes and edges.

        time_window_seconds:
            Maximum time difference between deviations
            to consider them related.
        """
        self.topology = topology
        self.time_window = timedelta(seconds=time_window_seconds)

        # Store recent deviations grouped by component
        self.recent_deviations = defaultdict(list)

        # Build adjacency list for fast topology traversal
        self.graph = self._build_graph(topology)

    def _build_graph(self, topology):
        """
        Build adjacency list from topology edges.
        """
        graph = defaultdict(list)
        for edge in topology["edges"]:
            graph[edge["from"]].append(edge["to"])
        return graph

    def record_deviation(self, deviation):
        """
        Record a deviation for later correlation.
        """
        deviation["timestamp"] = datetime.utcnow()
        self.recent_deviations[deviation["component"]].append(deviation)

    def correlate(self):
        """
        Identify correlated deviations across topology.

        Returns:
            List of correlation groups.
        """
        now = datetime.utcnow()
        correlation_groups = []

        # Flatten recent deviations within the time window
        active_deviations = []
        for component, deviations in self.recent_deviations.items():
            for d in deviations:
                if now - d["timestamp"] <= self.time_window:
                    active_deviations.append(d)

        # Group deviations by connected topology paths
        visited = set()

        for deviation in active_deviations:
            component = deviation["component"]
            if component in visited:
                continue

            group = self._collect_connected_deviations(
                component,
                active_deviations,
                visited
            )

            # Only consider meaningful correlation groups
            if len(group) >= 2:
                correlation_groups.append(group)

        return correlation_groups

    def _collect_connected_deviations(self, start_component, deviations, visited):
        """
        Collect deviations connected through topology starting from a component.
        """
        stack = [start_component]
        group = []

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)

            # Add deviations for this component
            for d in deviations:
                if d["component"] == current:
                    group.append(d)

            # Traverse downstream topology
            for neighbor in self.graph.get(current, []):
                stack.append(neighbor)

        return group
