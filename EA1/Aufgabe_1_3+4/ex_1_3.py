import pandas as pd

from lib import ATC, read_data_file, calculate_twt


def exercise_1_3():
    print(f"*========== |EX 1.3 | ==========*\n")
    schedule = read_data_file()
    atc = ATC(kappa=0.5)
    results = atc.evaluate_schedule(schedule, 3)
    twt = calculate_twt(results)
    print(f"EXECUTION RESULTS:\n{pd.DataFrame(results)}")
    print(f"\nTWT: {twt}\n")
    return twt
