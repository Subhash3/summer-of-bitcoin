# SUMMER OF BITCOIN CHALLENGE

#### Approach
- Task is to find the sequence of transaction_ids whose sum of weights is not greater than the block size and whose sum of fees is maximized.
- This sounds like `knapsack problem` to me. The only thing is that, the objects need to retain their original order.