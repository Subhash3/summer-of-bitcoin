from MempoolTransaction import MempoolTransaction
import typing

def parse_mempool_csv(mempool_file):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(mempool_file) as f:
        data  = f.readlines()
        data = data[1:] # first line contains header

        transactions = list()
        txid__to_transaction_map: typing.Dict[str, MempoolTransaction] = dict()
        for line in data :
            tx_info = line.strip().split(',')
            txid, fee, weight, parent_txs = tx_info
            fee = int(fee)
            weight = int(weight)
            parent_txs = parent_txs.strip().split(';')
            
            # print(txid, fee, weight, parent_txs)
            tx = MempoolTransaction(txid, fee, weight, parent_txs)
            transactions.append(tx)
            txid__to_transaction_map[txid] = tx

        return transactions, txid__to_transaction_map