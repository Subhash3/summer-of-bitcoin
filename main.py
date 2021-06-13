from helpers import parse_mempool_csv, describe_transactions_list
from MempoolTransaction import MempoolTransaction
import typing
from Block import Block


def get_transactions_without_parents(transactions) :
    transactions_without_parents = list()
    for transaction in transactions :
        if len(transaction.parents) == 0 :
            transactions_without_parents.append(transaction)
    return transactions_without_parents


def analyse_block_file(block_file, txid_to_transaction_map, txid_to_index_map) :
    with open(block_file)  as f :
        data = f.readlines()
        block_array = [line.strip() for line in data]
        block_transactions = [txid_to_transaction_map[txid] for txid in block_array]
        describe_transactions_list(block_transactions, f"Transactions of block {block_file}")

        is_valid_block = Block.validate_block_array(block_array, txid_to_transaction_map, txid_to_index_map)
        print(f"is_valid_block: {is_valid_block}")




def Main() :
    transactions: typing.List[MempoolTransaction] = list()
    transactions, txid_to_transaction_map = parse_mempool_csv('./resources/mempool.csv')
    describe_transactions_list(transactions, "All Transactions")

    # Create a map of transaction IDs to their original indices
    total_no_of_transactions = len(transactions)
    txid_to_index_map = dict()
    for i in range(total_no_of_transactions) :
        txid_to_index_map[transactions[i].txid] = i

    # Get transactions without any parent transactions
    transactions_without_parents = get_transactions_without_parents(transactions)
    describe_transactions_list(transactions_without_parents, "Transactions without parents")

    ## ## Constructing and exporting a block ## ## #
    weight_limit = 12345
    n = len(transactions_without_parents)
    b = Block(weight_limit, transactions_without_parents, n)
    max_profit, block_array = b.construct()
    print(f"{len(block_array)} transactions are there in the block")

    print(f"Max profit: {max_profit}")
    b.export()
    is_valid_block = b.validate(txid_to_transaction_map, txid_to_index_map)
    print(f"is_valid_block: {is_valid_block}")
    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    # Analyse an exported block file
    block_file = "./resources/block_sample.txt"
    analyse_block_file(block_file, txid_to_transaction_map, txid_to_index_map)

if __name__ == "__main__":
    Main()