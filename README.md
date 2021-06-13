# SUMMER OF BITCOIN CHALLENGE

#### Approach
- Task is to find the sequence of transaction_ids whose sum of weights is not greater than the block size and whose sum of fees is maximized.
- This sounds like `knapsack problem` to me. The only thing is that, the transaction should appear in a block iff all of its parents appear and they need to retain their original order.

#### Note
1. A block is valid iff _A transaction apprears in a block only if all of its parents appear earlier in the block_.
#### TODO
    - [ ] Create a class `Block` to handle methods related to blocks.
    - [x] Write a function to verify if a block is valid (Using Note-1).
    - [x] Fix the `numba reflected list` error.

    