import gnuplotlib as gp
import math
import numpy as np
from typing import List


class ResultsAnalyzer:

    def __init__(self, eplus_monthly_electricity: List[float], actual_monthly_electricity: List[float]):
        if len(eplus_monthly_electricity) != 12:
            raise Exception('EPlus Monthly Electricity size problem -- should be 12')
        if len(actual_monthly_electricity) != 12:
            raise Exception('Actual Monthly Electricity size problem -- should be 12')
        self.e_plus = eplus_monthly_electricity
        self.actual = actual_monthly_electricity

    def plot_electricity(self):
        x = np.array([x + 1 for x in range(12)])
        sum_square_error = 0
        for i in range(12):
            sum_square_error += (self.actual[i] - self.e_plus[i]) ** 2
        r_m_s_e = math.sqrt(sum_square_error)
        gp.plot(
            (x, np.array(self.actual), {'with': 'lines', 'legend': 'Actual'}),
            (x, np.array(self.e_plus), {'with': 'lines', 'legend': 'EnergyPlus'}),
            terminal='dumb 120,25', unset='grid', title='Comparing E+ to Actual (RMSE = %s)' % r_m_s_e
        )
