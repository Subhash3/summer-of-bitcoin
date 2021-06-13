class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        # TODO: add code to parse weight and parents fields

    def __str__(self):
        return f"txtid: {self.txtid}\nfee: {self.fee}\nweight: {self.weight}\nparents: {self.parents}"