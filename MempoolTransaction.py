class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = fee
        self.weight = weight
        self.parents = parents
        # TODO: add code to parse weight and parents fields

    def __str__(self):
        return f"txid: {self.txid}\nfee: {self.fee}\nweight: {self.weight}\nparents: {self.parents}"