#!/usr/bin/python

from datetime import datetime as dt
from datetime import timedelta
import json
from pytz import  timezone as tz
import random as rnd
from time import sleep
from urllib.request import urlopen


def read_url_in_json():
    with urlopen('https://yandex.com/time/sync.json?geo=213') as response:
        html = response.read()
        body_json = (html.decode())
        body_dict = json.loads(body_json)
    return body_dict

def read_time():
    data_dict = read_url_in_json()
    current_time = data_dict['time']
    return current_time

def convert_time(time_msec:int):
    time_zone_name = 'Europe/Moscow'
    url_timezone = tz(time_zone_name)
    time_url = dt.fromtimestamp(time_msec / 1000.0, tz=url_timezone).strftime("%Y-%m-%d %H:%M:%S")
    convert_time_url = dt.strptime(time_url, '%Y-%m-%d %H:%M:%S')
    return convert_time_url


def output_time_timezone():
    data_dict = read_url_in_json()
    current_time = read_time()
    time_zone = data_dict['clocks']['213']['name']
    result_time = convert_time(current_time)
    print("Time - ", result_time)
    print("Time zone - ", time_zone)


def delta_time(time_milisec:int):
    my_timezone =  tz('Europe/Saratov')
    random_sec_num = rnd.randint(1, 10)
    sleep(random_sec_num)

    my_time_now = (dt.now(tz=my_timezone).strftime("%Y-%m-%d %H:%M:%S"))
    time_url = convert_time(time_milisec)
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


print("\nTask 1 - part 'a'.")
print("Аnswer in raw form - \n", read_url_in_json())

print("\nTask 1 - part 'b'.")
output_time_timezone()


print("\nTask 1 - part 'c' and 'd'.")
input_time = read_time()
delta_time(input_time)
