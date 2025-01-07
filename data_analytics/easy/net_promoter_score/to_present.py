from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime


class NPS:
    """
    A class used to collect and analyze customer feedback,
    including calculating the Net Promoter Score (NPS) and plotting it over time.

    Attributes:
        feedbacks (dict): A dictionary to store feedback scores by period formatted as YYYYMM.
    """

    def __init__(self):
        """
        Initializes the NPS class with an empty dictionary for storing feedbacks.
        """
        self.feedbacks = {}

    def add_feedback(self, score: int, score_date: datetime = None):
        """
        Adds a feedback score for a specific datetime.

        Parameters:
            score (int): The customer's feedback score, must be between 0 and 10 inclusive.
            score_date (datetime, optional): The datetime of the feedback. Defaults to the current datetime if not provided.

        Raises:
            ValueError: If the score is not an integer or not within the range of 0 to 10.
        """
        if not isinstance(score, int) or not (0 <= score <= 10):
            raise ValueError("Invalid score")

        if score_date is None:
            score_date = datetime.now()

        score_date = int(score_date.strftime('%Y%m'))

        if score_date not in self.feedbacks:
            self.feedbacks[score_date] = []

        self.feedbacks[score_date].append(score)

    def calculate_nps(self, period: int) -> float:
        """
        Calculates and returns the Net Promoter Score (NPS) for a given period.

        Parameters:
            period (int): The period for which to calculate the NPS, formatted as YYYYMM.

        Returns:
            float: The calculated NPS, rounded to two decimal places.
            NPS ranges from -100 (all detractors) to 100 (all promoters).

        Explanation:
            NPS is calculated using the formula: ((Promoters - Detractors) / Total Responses) * 100
            - Promoters are rated 9 or 10.
            - Detractors are rated 6 or below.
            - Passives (scores of 7 and 8) do not directly affect the NPS.

        If no feedbacks are available for the specified period, returns 0
        """
        if period not in self.feedbacks:
            return 0.0

        promoters = sum(1 for score in self.feedbacks[period] if score >= 9)
        detractors = sum(1 for score in self.feedbacks[period] if score <= 6)
        return round((promoters - detractors) / len(self.feedbacks[period]) * 100, 2)

    def plot_trend(self, show_plot: bool = True) -> pd.DataFrame:
        """
        Plots NPS for each period stored in the feedbacks dictionary.

        Parameters:
            show_plot (bool): If True, displays the plot of NPS dynamics over time (default is True).

        Returns:
            pd.DataFrame: This DataFrame includes the following columns:
                - 'period' (int32): The period of feedback in YYYYMM format.
                - 'nps' (float32): The Net Promoter Score for that period.
            If the feedbacks dictionary is empty, returns an empty DataFrame.
        """
        if not self.feedbacks:
            return pd.DataFrame()

        data = {
            'period': [],
            'nps': []
        }
        for period, scores in self.feedbacks.items():
            nps = self.calculate_nps(int(period))
            data['period'].append(int(period))
            data['nps'].append(nps)

        df = pd.DataFrame(data)

        df['period'] = df['period'].astype('int32')
        df['nps'] = df['nps'].astype('float32')

        df = df.sort_values(by='period').reset_index(drop=True)

        if show_plot:
            plt.figure(figsize=(10, 6))
            plt.plot(df['period'], df['nps'], marker='o', label='NPS')
            plt.title('NPS OVER TIME')
            plt.xlabel('Period (YYYYMM)')
            plt.ylabel('NPS')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        return df
