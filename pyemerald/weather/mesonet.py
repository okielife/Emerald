import requests
import numpy as np
from os import walk
import os


def get_target_url(location, _year, _month, _day):
    target_url = "http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/"
    target_url += "%d%02d%02d%s" % (_year, _month, _day, location)
    target_url += "/mts/TEXT/"
    return target_url


def download_data_file(path, location, _year, _month, _day):
    try:
        target_url = get_target_url(location, _year, _month, _day)
        response = requests.get(target_url)
        out_file = open(os.path.join(path, "%d%02d%02d%s.txt") % (_year, _month, _day, location), 'wb')
        out_file.write(response.content)
        out_file.close()
    except Exception as e:
        print("Error downloading weather data: " + "%d%02d%02d%s.txt" % (_year, _month, _day, location) + str(e))


my_path = "/tmp/mesonet_data_files/"
# if os.path.exists(my_path):
#     shutil.rmtree(my_path)
# os.makedirs(my_path)
days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
lookups = dict()
for i, num_days in enumerate(days_in_months):
    month_num = i + 1
    lookups[month_num] = [x for x in range(1, num_days + 1)]
# for month, days in lookups.items():
#     for day in days:
#         download_data_file('/tmp/mesonet_data_files/', "kin2", 2019, month, day)
f = []
for _, _, filenames in walk(my_path):
    f.extend(filenames)
    break
lastDayOfMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
numHeaderLines = 3
weatherData_list = []
tokenInputList = [4, 3, 5, 13, 17]
year = 2018
month = 12
day = 31
hour = 17
for fileName in f:
    infile = open(os.path.join(my_path, fileName), 'r')
    print(infile)
    headerline = 0
    for line in infile:
        headerline += 1
        if headerline > numHeaderLines:
            tokens = line.split()
            tokenList = []
            # Set date and time
            minute = int(tokens[2]) % 60
            if minute == 0:
                hour += 1
                if hour == 24:
                    hour = 0
                    day += 1
                    if day > lastDayOfMonth[month - 1]:
                        day = 1
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
            tokenList.append(year)
            tokenList.append(month)
            tokenList.append(day)
            tokenList.append(hour)
            tokenList.append(minute)
            # Append listed items
            for token in tokenInputList:
                tokenList.append(float(tokens[token]))
            # Put list inside bigger list
            weatherData_list.append(tokenList)
            if int(tokens[2]) == 1435:
                break
# Convert to numpy array
weatherData = np.array(weatherData_list)
print(weatherData.shape)
dailyAverage_list = []
numerators = [0, 0, 0, 0, 0]
denominators = [0, 0, 0, 0, 0]
tempList = []
prevDay = 1
for line in range(weatherData.shape[0]):
    year = weatherData[line, 0]
    month = weatherData[line, 1]
    day = weatherData[line, 2]
    airTemp = weatherData[line, 3]
    relHum = weatherData[line, 4]
    wind = weatherData[line, 5]
    solar = weatherData[line, 6]
    soilTemp = weatherData[line, 7]
    if year == 2019:
        if day == prevDay:
            for entry in range(len(weatherData[line])):
                if entry > 4:
                    if weatherData[line, entry] > -200:
                        numerators[entry - 5] += weatherData[line, entry]
                        denominators[entry - 5] += 1
        else:
            tempList.append(year)
            tempList.append(month)
            tempList.append(day)
            for entry in range(len(numerators)):
                if float(denominators[entry]) == 0:
                    tempList.append(0)
                else:
                    tempList.append(numerators[entry] / float(denominators[entry]))
            dailyAverage_list.append(tempList)
            numerators = [0, 0, 0, 0, 0]
            denominators = [0, 0, 0, 0, 0]
            tempList = []
            for entry in range(len(weatherData[line])):
                if entry > 4:
                    if weatherData[line, entry] > -200:
                        numerators[entry - 5] += weatherData[line, entry]
                        denominators[entry - 5] += 1
        prevDay = day
dailyAverage = np.array(dailyAverage_list)
xRange = range(len(dailyAverage))
airTemp = dailyAverage[:, 3]
relHum = dailyAverage[:, 4]
wind = dailyAverage[:, 5]
solar = dailyAverage[:, 6]
soilTemp = dailyAverage[:, 7]
soilTemp_model = [1.93295, 0.257731, 1.37396, 3.59343, -2.52588, -7.0102, -1.90898, -0.876014, -0.583155, 3.0935,
                  4.19801, 7.76437, 6.68844, 5.31517, 4.78704, 5.66021, 4.18835, 5.28714, 6.00217, 6.25431, 2.02675,
                  2.30165, -3.27056, -1.75863, 3.20301, 5.21059, -1.32193, -1.18127, 0.266161, 2.29082, 1.22153,
                  0.025698, -1.52415, -1.42586, -1.26145, -5.2694, -6.66286, -5.82804, -4.42545, -3.13357, -3.70975,
                  -2.04049, -0.273109, 2.80822, 5.03094, 5.90262, 7.03155, 8.78147, 8.34427, 9.04438, 9.34654, 7.83057,
                  8.56385, 6.98125, 4.86557, 3.08321, 1.95702, 4.4839, 6.60439, 3.49049, -5.25561, -7.42959, -1.5388,
                  1.4823, 3.71712, 5.78636, 2.62787, 6.9284, 10.2276, 12.5134, 9.71391, 10.3079, 11.5179, 10.6452,
                  6.64496, 8.12105, 10.5277, 10.276, 11.5579, 12.4282, 9.63076, 7.69676, 8.8946, 9.90095, 7.18836,
                  13.1136, 10.4092, 13.3355, 14.2144, 15.6849, 11.5661, 16.5563, 17.0215, 13.8881, 13.7749, 11.666,
                  13.533, 13.3558, 15.3505, 17.4147, 18.6296, 20.404, 17.9828, 11.292, 13.4225, 14.0054, 11.64, 16.0887,
                  17.455, 16.6286, 17.636, 19.5558, 19.9306, 18.8877, 19.234, 20.4556, 20.666, 17.7825, 13.4425,
                  13.4067, 14.9837, 18.8064, 19.9031, 21.497, 22.8085, 24.0076, 24.3168, 23.4779, 22.9263, 24.2322,
                  24.8121, 19.6618, 17.5636, 17.8161, 18.0354, 19.1239, 18.2785, 19.6141, 22.0998, 23.7983, 24.2891,
                  25.7456, 24.3544, 24.8313, 24.1907, 22.9951, 21.1692, 24.7311, 25.9899, 25.1939, 25.7311, 25.6457,
                  26.7387, 27.8214, 28.3767, 27.3973, 27.0009, 27.3902, 24.5224, 23.8173, 23.9383, 27.2244, 26.4395,
                  27.8781, 27.2038, 27.5435, 28.2722, 28.41, 28.8179, 27.2499, 28.8727, 29.9831, 29.663, 28.496, 29.721,
                  30.5194, 29.3371, 27.4204, 25.9, 28.5958, 29.8231, 28.327, 27.7661, 28.4456, 29.9294, 30.191, 30.6561,
                  31.1908, 30.406, 30.7032, 27.3761, 29.661, 29.9178, 31.0702, 31.3332, 27.62, 23.2422, 20.8006,
                  21.4501, 24.2724, 27.3366, 29.7033, 32.4947, 31.7352, 32.9167, 31.9069, 31.6249, 30.3916, 29.7811,
                  31.6925, 26.4638, 25.0832, 29.3449, 31.8887, 34.9719, 34.617, 33.2433, 30.7811, 31.7629, 30.9409,
                  31.2675, 32.5184, 31.3692, 31.6114, 32.0314, 30.7598, 30.5628, 31.1741, 34.3999, 31.2078, 31.5628,
                  30.7368, 30.9571, 31.0923, 30.4464, 30.6076, 31.6566, 32.396, 32.3037, 31.0159, 29.8026, 31.9858,
                  30.6328, 29.6, 27.8429, 29.5347, 29.5595, 28.8938, 23.9408, 27.8959, 28.6408, 28.9165, 26.29, 23.0141,
                  18.2403, 18.899, 21.5659, 23.187, 23.5321, 26.1361, 26.4655, 26.9862, 27.6765, 24.9608, 25.2733,
                  23.7801, 23.3703, 24.212, 25.1956, 25.4021, 26.7282, 26.5381, 25.4899, 26.068, 24.2109, 20.3867,
                  20.4797, 21.9224, 23.58, 25.5521, 25.3991, 25.3496, 20.2827, 16.4349, 18.2623, 16.0467, 16.7655,
                  20.4369, 20.6748, 19.9301, 18.5123, 19.0214, 21.1564, 22.2159, 21.8488, 20.4346, 21.68, 23.6084,
                  22.7317, 21.2294, 18.0578, 19.5497, 18.0386, 14.2694, 11.5752, 12.1586, 13.5409, 11.5622, 12.4619,
                  13.107, 13.1646, 12.7981, 13.2864, 14.5297, 7.36255, 3.00066, 2.69711, 3.9689, 3.98178, 1.29608,
                  1.60643, 3.62576, 5.80472, 6.50121, 7.14409, 9.70897, 10.1014, 8.227, 7.62932, 6.71522, 6.3815,
                  8.79002, 11.9941, 9.38028, 2.32971, 3.03384, 4.73276, 5.0522, 6.92792, 5.2714, 5.12984, 7.41359,
                  6.8013, 6.83548, 7.79574, 7.26686, 9.1057, 11.1315, 8.36704, 6.02786, 3.62994, 3.42313, 3.19276,
                  4.30322, 5.10336, 6.50808, 4.91851, 4.34579, 6.4299, 6.78602, 3.16962, 3.35083, 2.83298, -0.241818]
print(dailyAverage[-1])
outfile = open("2014-DailyAverage-STIL.csv", 'w')
for line in range(dailyAverage.shape[0]):
    for entry in range(len(dailyAverage[0]) - 1):
        outfile.write(str(dailyAverage[line, entry]) + ",")
    outfile.write(str(dailyAverage[line, -1]) + "\n")
outfile.close()
outfile = open("AirTemp.csv", 'w')
for line in range(dailyAverage.shape[0]):
    outfile.write(str(dailyAverage[line, 3]) + ",")
outfile.close()
outfile = open("RelHum.csv", 'w')
for line in range(dailyAverage.shape[0]):
    outfile.write(str(dailyAverage[line, 4] / 100.0) + ",")
outfile.close()
outfile = open("Wind.csv", 'w')
for line in range(dailyAverage.shape[0]):
    outfile.write(str(dailyAverage[line, 5]) + ",")
outfile.close()
outfile = open("Solar.csv", 'w')
for line in range(dailyAverage.shape[0]):
    outfile.write(str(dailyAverage[line, 6]) + ",")
outfile.close()
