# -*- coding: utf-8 -*-
import json
import re
import math
import time
import pandas as pd


def mapper(df_list, periods, last_date=None, nature_periods=[]):
    users = {}

    for order in df_list:
        user_id = order['customer_id']
        user = {}
        diffday = order['diff_btw_first_this_order']

        # if this line is the first order of this customer
        if diffday == 0:
            for k,v in order.items():
                if re.compile('^first_+').findall(k):
                    user[k] = v

            user['first_order_date'] = order['format_order_date']
            user['orders'] = {}
            index = order['diff_btw_first_last_order']

            for period in periods:
                user['orders']['day_' + str(period)] = {}

                for i in range(math.ceil(index / period)):
                    user['orders']['day_' + str(period)][i] = 0
            
            if nature_periods != []:
                first_order_date = user['first_order_date']
                last_date_format = int(last_date.replace('-', ''))
                months = diff_month(first_order_date, last_date_format)
                for nature_period in nature_periods:
                    user['orders']['month_' + str(nature_period)] = {}

                    for i in range(math.floor(months / nature_period) + 1):
                        user['orders']['month_' + str(nature_period)][i] = 0

            users[user_id] = user

        if diffday > 0:
            user = users[user_id]
            for period in periods:
                user['orders']['day_' + str(period)][math.floor((diffday - 1) / period)] = 1  # map最关键的一步！记1的操作
            
            if nature_periods != []:
                first_order_date = user['first_order_date']
                format_order_date = order['format_order_date']
                months = diff_month(int(first_order_date), int(format_order_date))
                for nature_period in nature_periods:
                    user['orders']['month_' + str(nature_period)][math.floor(months / nature_period)] = 1

            users[user_id] = user

    df = []
    for k, v in users.items():
        v['customer_id'] = k
        month = int(v['first_order_date']/100)
        m = {'month': month}
        orders = v['orders']
        del v['first_order_date']
        del v['orders']
        del v['customer_id']
        all = dict(m, **v, **orders)
        df.append(all)
    
    return df


def diff_month(day1, day2):
    month1 = int(day1 / 100 % 100)
    year1 = int(day1 / 10000)
    month2 = int(day2 / 100 % 100)
    year2 = int(day2 / 10000)
    return (year2 - year1) * 12 + (month2 - month1)


def reducer(df_list, dimensions, periods, nature_periods=[]):
    df = pd.DataFrame(df_list)
    all_periods = ['day_' + str(i) for i in periods] + ['month_' + str(i) for i in nature_periods]
    first_dimensions = ['first_' + i for i in dimensions]

    if len(all_periods) == 1:
        df = df.groupby(first_dimensions + ['month']).agg({
            all_periods[0]: [list, len]
        }).reset_index()
    else:
        tmp_map_groupby = {}
        tmp_map_groupby[all_periods[0]] = [list, len]
        for period in all_periods[1:]:
            tmp_map_groupby[period] = list
        df = df.groupby(first_dimensions + ['month']).agg(tmp_map_groupby).reset_index()

    df.columns = [''.join(x) for x in df.columns.ravel()]
    tmp_map_rename = {}

    for i in df.columns.tolist():
        if 'list' in i:
            tmp_map_rename[i] = re.sub('(list|len)', '', i)
        elif 'len' in i:
            tmp_map_rename[i] = 'total'
        else:
            continue

    df.rename(columns=tmp_map_rename, inplace=True)

    def reduce(x):
        d = {}
        length = 0
        for i in range(len(x)):
            tmp_length = len(x[i])
            if tmp_length > length:
                length = tmp_length
        for i in range(length):
            d[str(i)] = 0
        for i in range(len(x)):
            for k, v in x[i].items():
                d[str(k)] += v
        return d

    for period in all_periods:
        df[period] = df[period].apply(lambda x: reduce(x))
    return df
