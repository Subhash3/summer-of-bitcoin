from helpers import parse_mempool_csv, construct_block, export_block
from MempoolTransaction import MempoolTransaction
import typing

transactions: typing.List[MempoolTransaction] = list()
transactions, txid__to_transaction_map = parse_mempool_csv('./resources/mempool.csv')
n = len(transactions)
# print(n)

# t = transactions[526]
# print(t)
# for ptxid in t.parents :
#     print(txid__to_transaction_map[ptxid])

weight_limit = 100000
max_profit, block = construct_block(weight_limit, transactions, n)
print(block)

print(f"Max profit: {max_profit}")
# for txid in block :
#     print(txid__to_transaction_map[txid])
export_block(max_profit, block)