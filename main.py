from helpers import parse_mempool_csv, describe_transactions_list, knapsack_generalized
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

def construct_and_export(weight_limit, transactions, txid_to_transaction_map, txid_to_index_map) :
    n = len(transactions)
    b = Block(weight_limit, transactions, n)
    max_profit, block_array = b.construct()
    print(f"{len(block_array)} transactions are there in the block")

    print(f"Max profit: {max_profit}")
    b.export()
    is_valid_block = b.validate(txid_to_transaction_map, txid_to_index_map)
    print(f"is_valid_block: {is_valid_block}")


def combine_parents_util(tx: MempoolTransaction, txid_to_transaction_map, all_parents) :
    if len(tx.parents) == 0 :
        # print(tx.txid, tx.fee, tx.weight)
        return tx.txid, tx.fee, tx.weight

    combined_id = tx.txid
    combined_fee = tx.fee
    combined_weight = tx.weight
    for ptxid in tx.parents :
        all_parents.add(ptxid)
        ptx = txid_to_transaction_map[ptxid]
        new_id, new_fee, new_weight = combine_parents_util(ptx, txid_to_transaction_map, all_parents)
        combined_id = combined_id + ";" + new_id
        combined_fee += new_fee
        combined_weight += new_weight
    return combined_id, combined_fee, combined_weight
        

def combine_parents(transactions: typing.List[MempoolTransaction], txid_to_transaction_map) :
    all_parents = set()
    combined_parents_transactions:typing.List[MempoolTransaction] = list()
    for tx in transactions :
        if len(tx.parents) != 0 :
            combined_id, combined_fee, combined_weight = combine_parents_util(tx, txid_to_transaction_map, all_parents)
            combined_tx = MempoolTransaction(combined_id, combined_fee, combined_weight, [])
            combined_parents_transactions.append(combined_tx)
        else :
            if tx.txid not in all_parents:
                combined_parents_transactions.append(tx)
    return combined_parents_transactions
    


def Main() :
    transactions: typing.List[MempoolTransaction] = list()
    transactions, txid_to_transaction_map = parse_mempool_csv('./resources/mempool.csv')
    describe_transactions_list(transactions, "All Transactions")

    # Create a map of transaction IDs to their original indices
    total_no_of_transactions = len(transactions)
    txid_to_index_map = dict()
    for i in range(total_no_of_transactions) :
        txid_to_index_map[transactions[i].txid] = i


    # combined_parents_transactions = combine_parents(transactions, txid_to_transaction_map)
    # describe_transactions_list(combined_parents_transactions, "Combined parents transactions")

    # Get transactions without any parent transactions
    transactions_without_parents = get_transactions_without_parents(transactions)
    describe_transactions_list(transactions_without_parents, "Transactions without parents")

    ## ## Constructing and exporting a block ## ## #
    weight_limit = 90000
    # construct_and_export(weight_limit, transactions, txid_to_transaction_map, txid_to_index_map)
    # construct_and_export(weight_limit, combined_parents_transactions, txid_to_transaction_map, txid_to_index_map)
    construct_and_export(weight_limit, transactions_without_parents, txid_to_transaction_map, txid_to_index_map)
    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    # # Analyse an exported block file
    print("\n\n")
    block_file = "./blocks/block_4094954.0.txt"
    analyse_block_file(block_file, txid_to_transaction_map, txid_to_index_map)

if __name__ == "__main__":
    Main()