from helpers import knapsack_optimized
import time
import numpy as np
from MempoolTransaction import MempoolTransaction
import typing

class Block:
    def __init__(self, weight_limit, transactions, n) :
        self.weight_limit = weight_limit
        self.transactions = transactions
        self.n = n
        self.block_array = []
        self.max_profit = 0
    
    def construct(self) :
        print(f"Weight limit: {self.weight_limit}")
        print(f"Total transactions: {self.n}")

        weights = [item.weight for item in self.transactions]
        profits = [item.fee for item in self.transactions]
        item_ids = [item.txid for item in self.transactions]

        weights = np.array(weights)
        profits = np.array(profits)
        item_ids = np.array(item_ids)

        start_time = time.time()
        max_profit, used_items = knapsack_optimized(self.weight_limit, weights, profits, item_ids, self.n)
        end_time = time.time()

        time_taken = round(end_time - start_time, 3)
        print(f"\nKnapsack took: {time_taken} sec\n")

        self.block_array = used_items
        self.max_profit = max_profit

        return max_profit, self.block_array

    def export(self):
        block_file = f"blocks/block_{self.max_profit}.txt"
        with open(block_file, 'w') as f:
            for line in self.block_array :
                f.write(f"{line}\n")

    def validate_block(self, txid_to_transaction_map: typing.Dict[str, MempoolTransaction]) :
        no_of_blocks = len(self.block_array)
        block_set = set(self.block_array)

        for i in range(no_of_blocks) :
            txid = self.block_array[i]
            transaction = txid_to_transaction_map[txid]
            parents = transaction.parents

            # all of its parents should appear in block
            for parent_id in parents :
                if parent_id not in block_set :
                    print(f"Parent of: {txid} with id: {parent_id} doesn't appear in block")
                    return False
        return True

    @staticmethod
    def validate_block_array(block_array, txid_to_transaction_map: typing.Dict[str, MempoolTransaction]) :
        no_of_blocks = len(block_array)
        block_set = set(block_array)

        for i in range(no_of_blocks) :
            txid = block_array[i]
            transaction = txid_to_transaction_map[txid]
            parents = transaction.parents

            # all of its parents should appear in block
            for parent_id in parents :
                if parent_id not in block_set :
                    print(f"Parent of: {txid} with id: {parent_id} doesn't appear in block")
                    return False
        return True