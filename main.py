#!/usr/bin/python3

from helpers import parse_mempool_csv
from MempoolTransaction import MempoolTransaction
import typing

transactions: typing.List[MempoolTransaction] = list()
transactions, txid__to_transaction_map = parse_mempool_csv('./resources/mempool.csv')

t = transactions[526]
for ptxid in t.parents :
    print(txid__to_transaction_map[ptxid])
