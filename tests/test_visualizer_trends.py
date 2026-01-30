import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import visualizer


def test_risk_trend_improving():
    current = pd.DataFrame({"risk_score": [1, 2, 3]})
    previous = pd.DataFrame({"risk_score": [10, 2]})

    trend, current_sum, previous_sum = visualizer._calculate_risk_trend(current, previous)

    assert trend == "Improving"
    assert current_sum == 6
    assert previous_sum == 12
