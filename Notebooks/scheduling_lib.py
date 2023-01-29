# Definition of a job
from typing import List, Dict


class __Metricable:
    
    _metrics: Dict[str, float] = None
    
    def get_metrics(self) -> Dict[str, float]:
        return self._metrics
    
    def set_metrics(self, metrics: Dict[str, float]) -> None:
        self._metrics = metrics


class Job(__Metricable):
    
    f: int # family
    w: int # weight
    d: int # due date
    
    C: int = None # completion time
    
    def __init__(self, family: int, weight: int, due_date: int):
        super().__init__()
        self.f = family
        self.w = weight
        self.d = due_date
        
    def __str__(self) -> str:
        return f"Job(f={self.f}, w={self.w}, d={self.d}, metrics={self._metrics})"
    
    def __repr__(self) -> str:
        return str(self)


class Batch(__Metricable):
    
    family: int = None
    jobs: List[Job] = None
    
    C: int = None # completion time
    
    def __str__(self) -> str:
        return f"Batch(f={self.family}, jobs={self.jobs}, C={self.C}, metrics={self._metrics})"
        
    def __repr__(self) -> str:
        return str(self)

    
class BatchMachine:
    
    batch: Batch = None
    
    def __str__(self) -> str:
        return f"BatchMachine(batch={self.batch})"
    
    def __repr__(self) -> str:
        return str(self)
    
    def is_idle(self) -> bool:
        return self.batch is None
    
    def update(self, t: int) -> None:
        if not self.is_idle() and self.batch.C == t:
            self.batch = None
