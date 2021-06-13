from helpers import parse_mempool_csv
from MempoolTransaction import MempoolTransaction
import typing

transactions: typing.List[MempoolTransaction] = list()
transactions = parse_mempool_csv('./resources/mempool.csv')

print(transactions[0])