from helpers import parse_mempool_csv, describe_transactions_list
from MempoolTransaction import MempoolTransaction
import typing
from Block import Block

transactions: typing.List[MempoolTransaction] = list()
transactions, txid_to_transaction_map = parse_mempool_csv('./resources/mempool.csv')
# n = len(transactions)

describe_transactions_list(transactions)

transactions_without_parents = list()
for transaction in transactions :
    if len(transaction.parents) == 0 :
        transactions_without_parents.append(transaction)
n = len(transactions_without_parents)
describe_transactions_list(transactions_without_parents)

# print(n)

# t = transactions[526]
# print(t)
# for ptxid in t.parents :
#     print(txid_to_transaction_map[ptxid])

weight_limit = 200000
b = Block(weight_limit, transactions_without_parents, n)
max_profit, block_array = b.construct()
print(f"{len(block_array)} transactions are there in the block")

print(f"Max profit: {max_profit}")
b.export()
is_valid_block = b.validate(txid_to_transaction_map)
print(f"is_valid_block: {is_valid_block}")

# for txid in block :
#     print(txid_to_transaction_map[txid])

# block_file = "./blocks/block_1998524.0.txt"
# with open(block_file)  as f :
#     data = f.readlines()
#     block_array = [line.strip() for line in data]

#     is_valid_block = Block.validate_block_array(block_array, txid_to_transaction_map)
#     print(is_valid_block)