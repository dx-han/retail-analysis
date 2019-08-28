# -*- coding: utf-8 -*-
import json
import time
import numpy as np
import pandas as pd
import re
import datetime


def stack_data(df):
    """Add first-txn-based and selectively multidimensional info to each txn record.

    Arguments:
        df: order table with .csv format
        last_date: the last date of the whole order table

    Returns:
        A map where key is customer_id, value is 
    """

    _columns = df.columns.tolist()
    _must_columns = ['customer_id', 'txn_date']
    dimensions = [i for i in _columns if i not in _must_columns]
    last_date = df['txn_date'].max()
    # last_date = datetime.datetime.strftime(
    #     datetime.datetime.strptime(df['txn_date'].max(), '%Y-%m-%d') + datetime.timedelta(32), '%Y-%m-%d')
    df.sort_values(by=['txn_date'], ascending=True, inplace=True)
    df_list = df.to_dict(orient = 'records')
    first_orders = {}
    orders = []

    for order in df_list:
        order_txn_time = order['txn_date']
        if order['txn_date'] is np.nan:
            continue
        else:
            order_timestamp = time.mktime(time.strptime(order_txn_time, '%Y-%m-%d'))
            order['txn_date'] = order_timestamp

        user_id = order['customer_id']
        format_date = list(time.localtime(order_timestamp))
        order['format_order_date'] = format_date[0] * 10000 + format_date[1] * 100 + format_date[2]

        if user_id not in first_orders:
            first_orders[user_id] = order

        first_order = first_orders[user_id]
        last_time = time.mktime(time.strptime(last_date, '%Y-%m-%d'))
        order['diff_btw_first_last_order'] = int((last_time - first_order['txn_date']) / 86400)
        order['diff_btw_first_this_order'] = int((order_timestamp - first_order['txn_date']) / 86400)

        for dim in dimensions:
            order['first_' + str(dim)] = first_order[str(dim)]

        orders.append(order)
    return orders, dimensions, last_date
