from calendar import monthrange
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import List


class ValidationManager:

    @staticmethod
    def process_2019_raw_into_monthly() -> List[float]:
        """
        Takes the raw offset monthly electricity usage resource file and re-fits it into standard monthly bins.
        This will add a very minor amount of error.

        :return: A list of 12 floating point values that represent calendar-monthly electricity kWh usage.
        """
        this_file_path = Path(os.path.realpath(__file__))
        this_file_dir = this_file_path.parent
        usage_2019_file = this_file_dir / 'resources' / 'electricity2019.json'
        with usage_2019_file.open() as f:
            usage_2019_data = json.loads(f.read())
        flat_kwh_per_day = []
        for raw_month in usage_2019_data:
            start_date = datetime.strptime(raw_month['StartDate'], '%m/%d/%Y')
            end_date = datetime.strptime(raw_month['EndDate'], '%m/%d/%Y')
            days_in_range = (end_date - start_date).days
            for i in range(days_in_range + 1):
                this_date = start_date + timedelta(i)
                if this_date.year == 2019:
                    flat_kwh_per_day.append(raw_month['kWh'])
        day_index = -1
        month_usages = []
        for month in range(1, 13):
            num_days = monthrange(2019, month)[1]
            month_sum = 0
            for day in range(num_days):
                day_index += 1
                month_sum += flat_kwh_per_day[day_index]
            month_usages.append(round(month_sum / num_days, 2))
        return month_usages
