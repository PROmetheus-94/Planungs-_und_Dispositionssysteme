FILEPATH_DATA = "./data/Daten_EA1_3_4.txt"
KEY_JOB_ID = "j"
KEY_JOB_WEIGHT = "wj"
KEY_JOB_EFT = "dj"
KEY_JOB_DURATION = "pj"
KEY_PRIORITY_INDEX = "it"
KEY_MACHINE_ID = "m_id"
KEY_START_TIME = "start"
KEY_END_TIME = "end"
INPUT_KEYS = (KEY_JOB_ID, KEY_JOB_WEIGHT, KEY_JOB_EFT, KEY_JOB_DURATION)


# read data file and convert into param_list for other methods
def read_data_file() -> list[dict]:
    param_list = list()
    with open(FILEPATH_DATA, "r") as f:
        f.readline()
        for i in range(12):
            param_values = (f.readline().strip("\n").split("\t"))
            param_list.append(
                {k: v if k == KEY_JOB_ID else int(v) for k, v in zip(INPUT_KEYS, param_values)}
            )
    return param_list


# calculate TWT
def calculate_twt(results: list[dict]) -> float:
    return sum(
        result[KEY_JOB_WEIGHT] * max(result[KEY_END_TIME] - result[KEY_JOB_EFT], 0) for result in results
    )