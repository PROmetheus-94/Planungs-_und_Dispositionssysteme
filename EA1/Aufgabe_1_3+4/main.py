import math
import pandas as pd
from operator import itemgetter

import numpy as np

FILEPATH_DATA = "./Daten_EA1_3_4.txt"
KEY_JOB_ID = "j"
KEY_JOB_WEIGHT = "wj"
KEY_JOB_EFT = "dj"
KEY_JOB_DURATION = "pj"
KEY_PRIORITY_INDEX = "it"
KEY_MACHINE_ID = "m_id"
KEY_START_TIME = "start"
KEY_END_TIME = "end"
INPUT_KEYS = (KEY_JOB_ID, KEY_JOB_WEIGHT, KEY_JOB_EFT, KEY_JOB_DURATION)


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

    # append a list of params with index priority
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


# read data file and convert into param_list for other methods
def read_data_file() -> list[dict]:
    param_list = list()
    with open(FILEPATH_DATA, "r") as f:
        f.readline()
        for i in range(12):
            param_values = (f.readline().strip("\n").split("\t"))
            param_list.append({k: v if k == KEY_JOB_ID else int(v)
                               for k, v in zip(INPUT_KEYS, param_values)})
    return param_list


# TWT
def calculate_twt(results: list[dict]) -> float:
    return sum(
        result[KEY_JOB_WEIGHT] * max(result[KEY_END_TIME] - result[KEY_JOB_EFT], 0)
        for result in results
    )


def exercise_1_3():
    print(f"*========== |EX 1.3 | ==========*\n")
    schedule = read_data_file()
    atc = ATC(kappa=0.5)
    results = atc.evaluate_schedule(schedule, 3)
    twt = calculate_twt(results)
    print(f"RESULTS:\n{pd.DataFrame(results)}")
    print(f"\nTWT: {twt}\n")
    return twt


def exercise_1_4a():
    print(f"*========== |EX 1.4a| ==========*\n")
    schedule = read_data_file()
    kappa_twt_list = list()
    for s in range(1, 101, 1):
        kappa = 0.1 * s
        atc = ATC(kappa=kappa)
        results = atc.evaluate_schedule(schedule, 3)
        twt = calculate_twt(results)
        kappa_twt_list.append({"kappa": kappa, "twt": twt})
    kappa_twt_list = sorted(kappa_twt_list, key=lambda x: x["twt"])
    print(f"TOP 10 KAPPA-TWT VALUES:\n{pd.DataFrame(kappa_twt_list).head(10)}")
    print(f"\nBEST KAPPA-TWT: {kappa_twt_list[0]}\n")


def exercise_1_4b():
    print(f"*========== |EX 1.4b| ==========*\n")
    schedule = read_data_file()
    d_list = [entry[KEY_JOB_EFT] for entry in schedule]
    pj_list = [entry[KEY_JOB_DURATION] for entry in schedule]
    R = (max(d_list) - min(d_list)) / max(pj_list)
    kappa = 4.5 + R if R <= 0.5 else 6 - 2 * R
    results = ATC(kappa=kappa).evaluate_schedule(schedule, 3)
    kappa_twt = {"kappa": kappa, "twt": calculate_twt(results)}
    print(f"KAPPA-TWT: {kappa_twt}")


if __name__ == '__main__':
    exercise_1_3()
    exercise_1_4a()
    exercise_1_4b()

