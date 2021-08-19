#!/usr/bin/env python3
import argparse
import sys

import requests as requests
import requests_cache

from python_task.expression import DynamicExprFunction, DictNoDefault

URL_FORMAT = "https://static-api.prod.bonusway.com/api/16/campaigns_limit_{limit}_offset_" \
             "{offset}_order_popularity.json"


def get_single_data(limit, offset=0):
    return requests.get(URL_FORMAT.format(limit=limit, offset=offset)).json()


def get_data(limit, filter_fun):
    first_data = get_single_data(limit)
    total = int(first_data["total"])
    for data in filter(filter_fun, first_data["items"]):
        yield data
    for offset in range(limit, total, limit):
        next_data = get_single_data(limit, offset)
        for data in filter(filter_fun, next_data["items"]):
            yield data


def main(*args):
    parser = argparse.ArgumentParser(description="Query BonusWay api for campaigns and filter, sort, and print result")
    parser.add_argument(
        "-f",
        "--filter",
        type=DynamicExprFunction,
        default=DynamicExprFunction("commission.max.amount > 2.25 and commission.max.unit == '%'"),
        help="A python expression expressing the items to keep"
    )
    parser.add_argument(
        "-s",
        "--sort",
        type=DynamicExprFunction,
        default=DynamicExprFunction("title.lower()"),
        help="A python expression expressing the attribute the output should be sorted in"
    )
    parser.add_argument(
        "-p",
        "--print",
        default="{title}",
        help="A format string for printing each item"
    )
    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="Clear the cache before making the request"
    )
    options = parser.parse_args(args)
    requests_cache.install_cache(".cache", backend="filesystem")
    if options.clear:
        requests_cache.clear()
    for data in sorted(list(get_data(10, options.filter)), key=options.sort):
        print(options.print.format(**DictNoDefault(data)))


if __name__ == "__main__":
    main(*sys.argv[1:])
