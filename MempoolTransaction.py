class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = parents.strip().split(';')
        # TODO: add code to parse weight and parents fields

    def __str__(self):
        return f"txid: {self.txid}\nfee: {self.fee}\nweight: {self.weight}\nparents: {self.parents}"