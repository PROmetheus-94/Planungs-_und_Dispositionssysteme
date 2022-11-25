import pandas as pd

from ex_1_3 import exercise_1_3
from ex_1_4 import exercise_1_4a, exercise_1_4b, exercise_1_4c

if __name__ == '__main__':
    exercise_twts = (exercise_1_3(), exercise_1_4a(), exercise_1_4b())
    print("COMPARISON OF ALL METHODS:")
    comparison_df = pd.DataFrame([
        {"method": method_twt[0], "twt": method_twt[1]}
        for method_twt in zip(["kappa fixed at 0.5", "grid search", "emp. formula and lpt"], exercise_twts)
    ]).sort_values("twt")
    print(comparison_df, "\n")
    exercise_1_4c()
