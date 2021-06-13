#!/usr/bin/python3

from helpers import parse_mempool_csv, knapsack_generalized
from MempoolTransaction import MempoolTransaction
import typing

transactions: typing.List[MempoolTransaction] = list()
transactions, txid__to_transaction_map = parse_mempool_csv('./resources/mempool.csv')
n = len(transactions)
print(n)

# t = transactions[526]
# print(t)
# for ptxid in t.parents :
#     print(txid__to_transaction_map[ptxid])



profits = [ 60, 100, 120 ]
weights = [ 10, 20, 30 ]
total_weight = 50
n = len(profits)

max_profit, used_items = knapsack_generalized(40000, transactions, n)
print(max_profit)

for txid in used_items :
    print(txid__to_transaction_map[txid])
