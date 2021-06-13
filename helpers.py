from MempoolTransaction import MempoolTransaction

def parse_mempool_csv(mempool_file):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(mempool_file) as f:
        data  = f.readlines()
        data = data[1:] # first line contains header

        return([MempoolTransaction(*line.strip().split(',')) for line in data])

