import logging
from math import log2, floor
# from greedypermutation.maxheap import MaxHeap
from collections import defaultdict


class BucketQueue:
    """
    Store the bucket lower bounds in a heap.
    Use this heap to keep track of the largest bucket value.
    Implement each bucket as a set.

    To insert, compute bucket value of priority.
    If bucket value is within num_buckets of the max, insert it into the corresponding bucket.
    Else, it goes on the backburner.

    Removemax pops the largest bucket.
    """

    def __init__(
        self,
        items=(),
        key=lambda x: x,
        bucket_size=1,
        use_backburner=False,
        num_buckets=None,
    ):
        self.buckets = defaultdict(set)  # maps levels to buckets
        self.levels = dict()  # maps items to levels
        if bucket_size < 1:
            logging.error(f"Bucket parameter passed is {bucket_size}.")
            raise RuntimeError("Bucket size should be greater than 1.")
        self.bucket_size = bucket_size  # should be greater than 1
        self.key = key
        if use_backburner:
            self.use_backburner = True
            if num_buckets is None:
                raise RuntimeError("Number of buckets not specified.")
            self.num_buckets = num_buckets
        else:
            self.use_backburner = False
        self.use_backburner = False
        for item in items:
            self.insert(item, key(item))
        logging.debug(f"Number of buckets at construction is {len(self.buckets)}")

    def insert(self, item, priority=None):
        if priority is None:
            priority = self.key(item)
        # Compute the level to insert item.
        level = self.get_bucket(priority)
        # Check if item should go on the backburner
        if self.too_small(level):
            level = "bb"
        # else add it to bucket on main queue
        self.levels[item] = level
        self.buckets[level].add(item)

    def findmax(self):
        max_level = self.maxlevel()
        max_cell = next(iter(self.buckets[max_level]))
        return max_cell

    def removemax(self):
        if len(self) == 0:
            raise RuntimeError("Bucket queue is empty.")
        output = self.findmax()
        self.remove_item(output)
        return output

    def changepriority(self, item, priority=None):
        self.remove_item(item)
        self.insert(item, priority)

    def remove_item(self, item):
        if item not in self.levels:
            raise RuntimeError("Removing non-existent item")
        level = self.levels[item]
        if item not in self.buckets[level]:
            raise RuntimeError("Removing non-existent item")
        del self.levels[item]
        self.buckets[level].remove(item)
        if self.bucket_empty(level):
            self.remove_bucket(level)

    def remove_bucket(self, level):
        if level in self.buckets:
            del self.buckets[level]

    def bucket_empty(self, level):
        return len(self.buckets[level]) == 0

    def has_buckets(self):
        return len({x for x in self.buckets} - {"bb"}) > 0

    def maxlevel(self):
        max_level = max(self.buckets)
        while self.bucket_empty(max_level) and self.has_buckets():
            self.remove_bucket(max_level)
            max_level -= 1
        if not self.has_buckets():
            # SID: Need to check backburner in this case
            self.pop_bb()
            return self.maxlevel()
        return max_level
    def pop_bb(self):
        # pop off bb
        # add to main queue
        pass

    def too_small(self, bucket_num):
        return self.use_backburner and self.maxlevel() - bucket_num > self.num_buckets

    def get_bucket(self, priority):
        return floor(log2(priority + 1e-8) / log2(self.bucket_size))

    def __len__(self):
        return sum(len(bucket) for bucket in self.buckets)
