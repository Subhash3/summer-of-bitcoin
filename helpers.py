from MempoolTransaction import MempoolTransaction
import typing
import time
from numba import jit
import numpy as np

def parse_mempool_csv(mempool_file):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(mempool_file) as f:
        data  = f.readlines()
        data = data[1:] # first line contains header

        transactions = list()
        txid__to_transaction_map: typing.Dict[str, MempoolTransaction] = dict()
        for line in data :
            tx_info = line.strip().split(',')
            txid, fee, weight, parent_txs_string = tx_info
            fee = int(fee)
            weight = int(weight)
            parent_txs_string = parent_txs_string.strip()

            parent_txs = list()
            if parent_txs_string != '' :
                parent_txs = parent_txs_string.split(';')
            
            # print(txid, fee, weight, parent_txs)
            tx = MempoolTransaction(txid, fee, weight, parent_txs)
            transactions.append(tx)
            txid__to_transaction_map[txid] = tx

        return transactions, txid__to_transaction_map


def knapsack_generalized(total_weight, items:typing.List[MempoolTransaction], n):
    """
        Solves the knapsack problem.
        This has been taken from https://www.geeksforgeeks.org/printing-items-01-knapsack/ and modified to suit my needs.
    """
    lookup = [[0 for w in range(total_weight + 1)]
            for i in range(n + 1)]

    for i in range(n + 1):
        for w in range(total_weight + 1):
            if i == 0 or w == 0:
                lookup[i][w] = 0
            elif items[i - 1].weight <= w:
                lookup[i][w] = max(items[i - 1].fee + lookup[i - 1][w - items[i - 1].weight], lookup[i - 1][w])
            else:
                lookup[i][w] = lookup[i - 1][w]


    max_profit = lookup[n][total_weight]
    # print(max_profit)
    max_profit_bkup = max_profit

    used_items = list()

    w = total_weight
    for i in range(n, 0, -1):
        if max_profit <= 0:
            break

        if max_profit == lookup[i - 1][w]:
            continue
        else:
            # print(items[i - 1].weight)
            used_items.append(items[i - 1].txid)
            max_profit = max_profit - items[i - 1].fee
            w = w - items[i - 1].weight

    return max_profit_bkup, used_items

@jit(nopython=True)
def knapsack_optimized(total_weight, weights, profits, item_ids, n):
    """
        Solves the knapsack problem.
        This has been taken from https://www.geeksforgeeks.org/printing-items-01-knapsack/ and modified to suit my needs.
    """
    # lookup = [[0 for w in range(total_weight + 1)]
    #         for i in range(n + 1)]
    lookup = np.zeros((n+1, total_weight+1))

    for i in range(n + 1):
        for w in range(total_weight + 1):
            if i == 0 or w == 0:
                lookup[i][w] = 0
            elif weights[i-1] <= w:
                lookup[i][w] = max(profits[i-1] + lookup[i - 1][w - weights[i-1]], lookup[i - 1][w])
            else:
                lookup[i][w] = lookup[i - 1][w]


    max_profit = lookup[n][total_weight]
    # print(max_profit)
    max_profit_bkup = max_profit

    used_items = list()

    w = total_weight
    for i in range(n, 0, -1):
        if max_profit <= 0:
            break

        if max_profit == lookup[i - 1][w]:
            continue
        else:
            # print(items[i - 1].weight)
            used_items.append(item_ids[i - 1])
            max_profit = max_profit - profits[i-1]
            w = w - weights[i-1]

    return max_profit_bkup, used_items


def construct_block(weight_limit, transactions, n) :
    print(f"Weight limit: {weight_limit}")
    print(f"Total transactions: {n}")

    weights = [item.weight for item in transactions]
    profits = [item.fee for item in transactions]
    item_ids = [item.txid for item in transactions]

    weights = np.array(weights)
    profits = np.array(profits)
    item_ids = np.array(item_ids)

    start_time = time.time()
    max_profit, used_items = knapsack_optimized(weight_limit, weights, profits, item_ids, n)
    end_time = time.time()
    time_taken = round(end_time - start_time, 3)

    print(f"\nKnapsack took: {time_taken} sec\n")

    return max_profit, used_items

def export_block(max_profit, block) :
    block_file = f"blocks/block_{max_profit}.txt"
    with open(block_file, 'w') as f:
        for line in block :
            f.write(f"{line}\n")

def validate_block(block, txid_to_transaction_map: typing.Dict[str, MempoolTransaction]) :
    n = len(block)
    block_set = set(block)
    for i in range(n) :
        txid = block[i]
        transaction = txid_to_transaction_map[txid]
        parents = transaction.parents

        # all of its parents should appear in block
        for parent_id in parents :
            if parent_id not in block_set :
                print(f"Parent of: {txid} with id: {parent_id} doesn't appear in block")
                return False
    return True