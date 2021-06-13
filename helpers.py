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
        txid_to_transaction_map: typing.Dict[str, MempoolTransaction] = dict()
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
            txid_to_transaction_map[txid] = tx

        return transactions, txid_to_transaction_map


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

@jit
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

def describe_transactions_list(transactions: typing.List[MempoolTransaction], list_name="") :
    total_fees = 0
    total_weights = 0

    for tx in transactions :
        total_weights += tx.weight
        total_fees += tx.fee
    print(f"{list_name}:")
    print(f"\tNo. of txs: {len(transactions)}")
    print(f"\tTotal Fees: {total_fees}")
    print(f"\tTotal weights: {total_weights}")