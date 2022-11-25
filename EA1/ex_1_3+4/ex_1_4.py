import pandas as pd

from lib import ATC, read_data_file, calculate_twt, \
    KEY_JOB_EFT, KEY_JOB_DURATION, KEY_MACHINE_ID, KEY_START_TIME, KEY_END_TIME


def exercise_1_4a():
    print(f"*========== |EX 1.4a| ==========*\n")
    schedule = read_data_file()
    kappa_twt_list = list()
    for s in range(1, 101):
        kappa = 0.1 * s
        atc = ATC(kappa=kappa)
        results = atc.evaluate_schedule(schedule, 3)
        twt = calculate_twt(results)
        kappa_twt_list.append({"kappa": kappa, "twt": twt})
    kappa_twt_list = sorted(kappa_twt_list, key=lambda x: x["twt"])
    print(f"TOP 10 KAPPA-TWT VALUES:\n{pd.DataFrame(kappa_twt_list).head(10)}\n")
    print(f"BEST KAPPA-TWT: {kappa_twt_list[0]}\n")
    best_atc_results = ATC(kappa=kappa_twt_list[0]["kappa"]).evaluate_schedule(schedule, 3)
    print(f"BEST KAPPA-TWT EXECUTION RESULTS:\n")
    print(f"{pd.DataFrame(best_atc_results)[[KEY_MACHINE_ID, KEY_START_TIME, KEY_END_TIME]]}\n")
    return kappa_twt_list[0]["twt"]


def exercise_1_4b():
    print(f"*========== |EX 1.4b| ==========*\n")
    schedule = read_data_file()
    d_list = [entry[KEY_JOB_EFT] for entry in schedule]
    pj_list = [entry[KEY_JOB_DURATION] for entry in schedule]
    R = (max(d_list) - min(d_list)) / max(pj_list)
    kappa = 4.5 + R if R <= 0.5 else 6 - 2 * R
    results = ATC(kappa=kappa).evaluate_schedule(schedule, 3)
    kappa_twt = {"kappa": kappa, "twt": calculate_twt(results)}
    print(f"KAPPA-TWT: {kappa_twt}\n")
    return kappa_twt["twt"]


def exercise_1_4c():
    print(f"*========== |EX 1.4c| ==========*\n")
    print(
        "LPT (Longest Processing Time) stellt eine sinnvolle Wahl für die Abschätzung der Durchlaufzeit "
        "bei List-Scheduling dar,\nweil eine Maschine nach dem Ablaufen von LPT auf jeden Fall wieder frei ist. "
        "Man kann so eine Durchlaufzeit abschätzen ohne\ndie parallelen Verarbeitungsstränge auf diversen Maschinen"
        "berücksichtigen zu müssen.\n"
    )
