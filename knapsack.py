import time

class Item :
    def __init__(self, txid, weight, fee) :
        self.weight = weight
        self.fee = fee
        self.txid = txid
    
    def __str__(self) :
        return f"({self.weight}, {self.fee}, {self.txid})"


def include_item_condition(item, used_items) :
    return True

class Knapsack:

    def __init__(self):
        self.max_profit = None
        self.used_items_for_max_profit = list()

    def knapsack_util(self, items, used_items, free_space, profit_so_far, i, n, spacing) :
        # print(f"{spacing}{used_items}, {free_space}, {profit_so_far}, {i}, {n}, max_profit: {self.max_profit}")

        if self.max_profit == None or profit_so_far > self.max_profit :
            self.max_profit = profit_so_far
            self.used_items_for_max_profit = used_items[:]

        if i >= n :
            return

        if items[i].weight > free_space :
            # # print(f"Weight {items[i].weight} > {free_space}")
            self.knapsack_util(items, used_items, free_space, profit_so_far, i+1, n, spacing+"\t")
        else :
            # Include
            if include_item_condition(items[i], used_items) :
                # print(f"{spacing}Including {items[i].txid}")
                used_items.append(items[i].txid)
                self.knapsack_util(items, used_items, free_space - items[i].weight, profit_so_far + items[i].fee, i+1, n, spacing+"\t")
                used_items.pop()
            else :
                # print(f"{spacing}Not including {items[i].txid} as it doesn't pass include_item_condition")
                pass

            # Exclude
            # print(f"{spacing}Excluding {items[i].txid}")
            self.knapsack_util(items, used_items, free_space, profit_so_far, i+1, n, spacing+"\t")
        return


    def knapsack(self, items, total_weight) :
        used_items = list()
        n = len(items)
        start = time.time()
        self.knapsack_util(items, used_items, total_weight, 0, 0, n, spacing="")
        end = time.time()
        print(f"Time taken: {round(end-start, 3)}")

# k = Knapsack()


# items = [
#     Item(1, 10, 60),Item(2, 20, 100), Item(3,30,120)
# ]

# k.knapsack(items, 50)
# print(k.max_profit)
# print(k.used_items_for_max_profit)