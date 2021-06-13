# SUMMER OF BITCOIN CHALLENGE

#### Approach
- Task is to find the sequence of transaction_ids whose sum of weights is not greater than the block size and whose sum of fees is maximized.
- This sounds like `knapsack problem` to me. The only thing is that, the transaction should appear in a block iff all of its parents appear and they need to retain their original order.

#### Note
1. A block is valid iff _A transaction apprears in a block only if all of its parents appear earlier in the block_.


## Installation and Usage
- The system must have python >= 3.6.9 and pipenv installed.
- To install them:

```bash
sudo apt-get install python3
sudo python3 -m pip install pipenv
```
- Install dependencies
```bash
pipenv shell # activates the virtualenv
pipenv install # installs dependencies from Pipfile.lock
```

- To edit and run python file
```bash
python3 file.py # inside the virtualenv
```

#### TODO
    - [ ] Create a class `Block` to handle methods related to blocks.
    - [x] Write a function to verify if a block is valid (Using Note-1).
    - [x] Fix the `numba reflected list` error.
    - [ ] Turns out that some blocks generated by our knapsack are not valid. We need to figure out how to fix it.
    - [x] Use only those transactions which do not have parent transactions to avoid the above issue.
    - [x] The transactions in a block are in the reverse order because of knapsack. Due to this, transactions in the block files are in reverse order... Fix it!!
    - [x] Reverse the contents of previously generated block files.
