from agentsieve.models.trace_record import TraceRecord


class InMemoryTraceCollector:
    def __init__(self) -> None:
        self.records: list[TraceRecord] = []

    def collect(self, record: TraceRecord) -> None:
        self.records.append(record)
