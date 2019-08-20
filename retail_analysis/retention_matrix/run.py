# -*- coding: utf-8 -*-
from argparse import ArgumentParser

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--periods', type=str, default=[])
    parser.add_argument('--nature-periods', type=list, default=[])
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    print(args.periods)
    print(args.nature_periods)