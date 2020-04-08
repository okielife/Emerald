from pathlib import Path
import sqlite3


class OutputProcessor:

    def sql(self, sql_command):
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def __init__(self, path_to_sql_file: Path):
        connection = sqlite3.connect(str(path_to_sql_file))
        self.cursor = connection.cursor()

        # get the index of the facility electricity report meter
        cmd = "SELECT t.ReportDataDictionaryIndex FROM ReportDataDictionary t WHERE IndexGroup = 'Facility:Electricity'"
        result = self.sql(cmd)
        if len(result) != 1:
            raise Exception('Invalid meter outputs in EnergyPlus -- could not find Facility:Electricity index in SQL')
        report_id = result[0][0]

        # now get the values of the meter during the simulation
        cmd = "SELECT t.TimeIndex, t.Value FROM ReportData t WHERE ReportDataDictionaryIndex == %s" % report_id
        result = self.sql(cmd)

        # now we need to line up the monthly values for each output
        self.monthly_electricity = [0.0] * 12
        for time_index, meter_value in result:
            # get the current month and day type so we can exclude design days
            cmd = "SELECT t.Month, t.DayType FROM Time t WHERE TimeIndex == %s" % time_index
            result = self.sql(cmd)
            result = result[0]
            if result[1] == 'WinterDesignDay' or result[1] == 'SummerDesignDay':
                print("Skipping design day values")
                continue
            else:
                self.monthly_electricity[result[0] - 1] = round(meter_value / 3600 / 1000, 2)
        connection.close()
