from datetime import datetime as dt
from datetime import timedelta
import json
from pytz import  timezone as tz
import random as rnd
from time import sleep
from urllib.request import urlopen


def read_url_in_json(url:str):
    with urlopen(url) as response:
        html = response.read()
        body_json = (html.decode())
        body_dict = json.loads(body_json)
    return body_dict


def read_time(url:str):
    data_dict = read_url_in_json(url)
    current_time = data_dict['time']
    return current_time


def convert_time(time_msec:int, time_zone:str):
    url_timezone = tz(time_zone)
    time_url = dt.fromtimestamp(time_msec / 1000.0, tz=url_timezone).strftime("%Y-%m-%d %H:%M:%S")
    convert_time_url = dt.strptime(time_url, '%Y-%m-%d %H:%M:%S')
    return convert_time_url


def output_time_timezone(url:str):
    data_dict = read_url_in_json(url)
    current_time = read_time(url)
    time_zone = data_dict['clocks']['213']['name']
    result_time = convert_time(current_time,'Europe/Moscow')
    print("Time - ", result_time)
    print("Time zone - ", time_zone)


def delta_time(time_milisec:int, time_zone:str):
    my_timezone =  tz(time_zone)
    random_sec_num = rnd.randint(1, 10)
    sleep(random_sec_num)

    my_time_now = (dt.now(tz=my_timezone).strftime("%Y-%m-%d %H:%M:%S"))
    time_url = convert_time(time_milisec,'Europe/Moscow')
    convert_time_now = dt.strptime(my_time_now, '%Y-%m-%d %H:%M:%S')

    time_diff = convert_time_now - time_url

    print("My time:       ", convert_time_now)
    print("Time from url: ", time_url)
    print("Different time:", time_diff)

    sum_sec = 0
    for _ in range(5):
        time_diff_req = convert_time_now - time_url
        time_diff_sec = time_diff_req.total_seconds()
        sum_sec += time_diff_sec
    aver_dif = sum_sec / 5
    aver_dif_res = timedelta(seconds = aver_dif )

    print("Average delta time for 5 requests: ", aver_dif_res)



url = 'https://yandex.com/time/sync.json?geo=213'
my_time_zone = 'Europe/Saratov'
input_dict = read_url_in_json(url)


print("\nTask 1 - part 'a'.")
print("Аnswer in raw form - \n", input_dict)

print("\nTask 1 - part 'b'.")
output_time_timezone(url)


print("\nTask 1 - part 'c' and 'd'.")
input_time = read_time(url)
delta_time(input_time, my_time_zone)
