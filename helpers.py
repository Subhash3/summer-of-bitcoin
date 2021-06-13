from MempoolTransaction import MempoolTransaction

def parse_mempool_csv(mempool_file):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(mempool_file) as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

