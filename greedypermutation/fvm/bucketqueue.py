import logging
from math import log2, floor, inf
from collections import defaultdict


class BucketQueue:
    """
    A simple implementation of a bucket queue.
    Every bucket has a level.
    A dictionary maps levels to corresponding buckets.
    A separate dictionary maps every item in the queue to its current level for faster lookups.

    When inserting an item, if the level is within num_buckets of the current max level,
    then the item is inserted into the corresponding bucket.
    Else, it goes on the backburner.
    Removemax pops the largest bucket.
    """

    def __init__(
        self,
        items=(),
        key=lambda x: x,
        bucket_size=1,
        num_buckets=None,
    ):
        self.buckets = defaultdict(set)                                         # maps levels to buckets
        self.levels = dict()                                                    # maps items to levels
        if bucket_size < 1:
            logging.error(f"Bucket parameter passed is {bucket_size}.")
            raise RuntimeError("Bucket size should be greater than 1.")
        self.bucket_size = bucket_size  # should be greater than 1
        self.key = key
        self.num_buckets = inf if num_buckets is None else num_buckets
        for item in items:
            self.insert(item, key(item))
        logging.debug(f"Number of buckets at construction is {len(self.buckets)}")

    def insert(self, item, priority=None):
        """
        Insert an item with priority in the bucket queue.
        """
        if priority is None:
            priority = self.key(item)
        # Compute the level to insert item.
        level = self._bucket(priority)
        # Check if item should go on the backburner
        if self._too_small(level):
            level = "bb"
        # else add it to bucket on main queue
        self.levels[item] = level
        self.buckets[level].add(item)

    def findmax(self):
        """
        Return an item from the bucket with the highest level in the queue without removing it.
        """
        max_level = self.maxlevel()
        max_item = next(iter(self.buckets[max_level]))
        return max_item

    def removemax(self):
        """
        Remove an arbitrary item from the bucket with highest level in the queue.
        A RuntimeError is raised if the queue is empty.
        """
        if len(self) == 0:
            raise RuntimeError("Bucket queue is empty.")
        output = self.findmax()
        self._remove_item(output)
        return output

    def changepriority(self, item, priority=None):
        """
        Update the priority of an existing item to the input priority.
        """
        self._remove_item(item)
        self.insert(item, priority)

    def _remove_item(self, item):
        """
        Remove given item from its bucket in the queue.
        A RuntimeError is raised if the item is not in the queue.
        """
        if item not in self.levels:
            raise RuntimeError("Removing non-existent item")
        level = self.levels[item]
        if item not in self.buckets[level]:
            raise RuntimeError("Removing non-existent item")
        del self.levels[item]
        self.buckets[level].remove(item)
        if self._bucket_empty(level):
            self._remove_bucket(level)

    def _remove_bucket(self, level):
        """
        Remove bucket for given level from the queue.
        """
        if level in self.buckets:
            del self.buckets[level]

    def _bucket_empty(self, level):
        """
        Return True if the bucket for given level is empty.
        """
        return len(self.buckets[level]) == 0

    def _has_buckets(self):
        """
        Return True if the queue has a non-zero number of buckets.
        """
        return len({x for x in self.buckets} - {"bb"}) > 0

    def maxlevel(self):
        """
        Compute the level of the top-most bucket in the queue.
        """
        max_level = max(self.buckets)
        while self._bucket_empty(max_level) and self._has_buckets():
            self._remove_bucket(max_level)
            max_level -= 1
        if not self._has_buckets():
            # SID: Need to check backburner in this case
            self._pop_bb()
            return self.maxlevel()
        return max_level

    def _pop_bb(self):
        """
        Pop an item from the backburner and insert it in the main queue.
        Raises a RuntimeError if the backburner is empty.
        """
        bb = self.buckets['bb']
        if len(bb) == 0:
            raise RuntimeError("Backburner is empty.")
        # pop off bb
        item = bb.pop()
        # add to main queue
        self.insert(item)

    def _too_small(self, level):
        """
        Return True if the input bucket level is so small that it should be put on the bucket queue.
        """
        return self.maxlevel() - level > self.num_buckets

    def _bucket(self, priority):
        """
        Compute the relevant bucket for an item given its priority.
        """
        return floor(log2(priority + 1e-8) / log2(self.bucket_size))

    def __len__(self):
        return sum(len(bucket) for bucket in self.buckets)
