class VectorClock:
    def __init__(self, initial_clock=None):
        self.clock = initial_clock if initial_clock is not None else {}

    def increment(self, service_id):
        self.clock[service_id] = self.clock.get(service_id, 0) + 1

    def merge(self, other_clock):
        for key, value in other_clock.items():
            self.clock[key] = max(self.clock.get(key, 0), value)

    def get_clock(self):
        return self.clock

    @staticmethod
    def from_proto(proto_clock):
        return VectorClock({k: v for k, v in proto_clock.entries.items()})

    def to_proto(self, proto_class):
        return proto_class(entries={k: v for k, v in self.clock.items()})

    def is_after(self, other_vc):
        """
        Check if this vector clock is after another vector clock.
        A vector clock A is after B if A has all elements greater than or equal to B,
        and at least one element is strictly greater.
        """
        at_least_one_greater = False
        for key, value in self.clock.items():
            other_value = other_vc.clock.get(key, 0)
            if value < other_value:
                return False
            if value > other_value:
                at_least_one_greater = True
        return at_least_one_greater
