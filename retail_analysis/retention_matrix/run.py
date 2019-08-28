# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import pandas as pd
from utils import stack_data
from base import MapReduce
import time

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--filename', type=str, default=None)
    parser.add_argument('--periods', type=str, default=None)
    parser.add_argument('--nature-periods', type=str, default=None)
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    filename = args.filename
    periods = list(map(int, args.periods.split(','))) if args.periods != None else []
    nature = list(map(int, args.nature_periods.split(','))) if args.nature_periods != None else []
    df = pd.read_csv(filename + '.csv')
    orders, dimensions, last_date = stack_data(df)
    mp = MapReduce(df=orders, periods=periods, dimensions=dimensions, last_date=last_date, nature_periods=nature)
    df_reducer = mp.get_map_reduce_result()
    df_reducer.to_csv('df_reducer_'+str(int(time.time()))+'.csv', index=False, encoding='utf_8_sig')