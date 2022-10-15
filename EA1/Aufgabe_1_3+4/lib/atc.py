import math
from operator import itemgetter

import numpy as np

from .header import INPUT_KEYS, KEY_JOB_DURATION, KEY_MACHINE_ID, KEY_PRIORITY_INDEX, KEY_START_TIME, KEY_END_TIME


# Apparent-Tardiness-Cost (ATC)
class ATC:

    __kappa: float

    def __init__(self, kappa: float = 0.5):
        self.kappa = kappa

    # calculate priority index for single dict of params
    def get_job_priority(self, params: dict, p_arr: np.ndarray, t: int) -> float:
        assert all(key in params.keys() for key in INPUT_KEYS)
        j, wj, dj, pj = itemgetter(*INPUT_KEYS)(params)
        return (wj/pj) * math.exp(-max(dj - pj - t, 0)/(self.kappa * p_arr.mean()))

    # append a list of dicts of params with index priority
    def get_job_list_priority(self, param_list: list[dict], t: int) -> list[dict]:
        param_list_copy = param_list.copy()
        for params in param_list_copy:
            p_arr = np.array([p[KEY_JOB_DURATION] for p in param_list_copy])
            params[KEY_PRIORITY_INDEX] = self.get_job_priority(params, p_arr, t)
        return param_list_copy

    def evaluate_schedule(self, param_list: list[dict], parallel_executions: int) -> list[dict]:
        # discrete time variable
        tick = 0
        # simulate machine states: 0 for readiness, 1 for working
        machine_states = [0 for i in range(parallel_executions)]
        schedule = param_list.copy()
        results = list()
        while len(schedule) > 0:
            # calculate ATC-Priority and sort by it
            schedule = sorted(
                self.get_job_list_priority(schedule, tick),
                key=lambda x: x[KEY_PRIORITY_INDEX],
                reverse=True
            )
            # reset state of machines if done with job at current tick
            for result in results:
                if result[KEY_END_TIME] == tick:
                    machine_states[result[KEY_MACHINE_ID]] = 0
            # calculate results for top-1 priority if machine available
            for index, state in enumerate(machine_states):
                if state == 0:
                    machine_states[index] = 1
                    result = schedule.pop(0)
                    result[KEY_MACHINE_ID] = index
                    result[KEY_START_TIME] = tick
                    result[KEY_END_TIME] = tick + result[KEY_JOB_DURATION]
                    results.append(result)
            tick += 1
        return results