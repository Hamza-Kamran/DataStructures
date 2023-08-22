import sys
import  math


class Tombstone:
    def __init__(self):
        super().__init__()

class HashTable:
    DEFAULT_CAPACITY = 8
    def __init__(self, capacity=12, load_factor=0.5):

        if capacity < 1 or load_factor > 1:
            raise Exception("Load factor must be less than 1 and capacity must be greater than 1")
        
        self.load_factor = load_factor
        self.capacity = max(capacity, next2Power(capacity))
        self.threshold = int(self.load_factor * self.capacity)
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.used_buckets = 0
        self.keys_count = 0

    def __iter__(self):
        self.keys_left = self.keys_count
        self.x = 0
        return self

    def _hasNext(self):
        return self.keys_left != 0

    def __next__(self):
        x = self.x
        while self._hasNext():
            while self.keys[x] is None or isinstance(self.keys[x], Tombstone):
                x += 1
            key, value = self.keys[x], self.values[x]
            x += 1
            self.keys_left -= 1
            self.x = x
            return (key, value)

        raise StopIteration

    def normalize_index(self, keyHash):
        return (abs(keyHash)) % self.capacity

    def clear(self):
        for i in range(self.capacity):
            self.keys[i] = None
            self.values[i] = None
        self.used_buckets = self.keys_count = 0

    def resize_table(self):
        self.capacity = next2Power(self.capacity)
        self.threshold = int(self.capacity * self.load_factor)
        new_keys = [None] * self.capacity
        new_values = [None] * self.capacity
        old_keys = self.keys
        old_values = self.values

        self.keys = new_keys
        self.values = new_values

        self.keys_count = 0
        self.used_buckets = 0
        for i in range(len(old_keys)):
            old_key, old_value = old_keys[i], old_values[i]
            if old_key is not None and type(old_key) != Tombstone:
                self.insert(old_key, old_value)

    def insert(self, key, value):
        if self.used_buckets >= self.threshold:
            self.resize_table()
        hash_val = hash(key)
        offset = self.normalize_index(hash_val)
        j = -1
        x = 0
        i = offset
        while True:
            if type(self.keys[i]) is Tombstone:
                if j == -1:
                    j = i

            elif self.keys[i] is not None:
                if self.keys[i] == key:
                    old_value = self.values[i]
                    if j == -1:
                        self.values[i] = value
                    else:
                        self.keys[i] = Tombstone()
                        self.values[i] = None
                        self.keys[j] = key
                        self.values[j] = value

                    return old_value

            else:
                if j == -1:
                    self.keys[i] = key
                    self.values[i] = value
                    self.keys_count += 1
                    self.used_buckets += 1

                else:
                    self.keys_count += 1
                    self.keys[j] = key
                    self.values[j] = value

                return None

            x += 1
            i = self.normalize_index(offset + p(x))

    def get(self, key):
        if key is None:
            raise KeyError("Key is None. Not allowed")

        x = 0
        hash_value = hash(key)
        offset = self.normalize_index(hash_value)
        index = offset
        j = -1
        while True:

            if type(self.keys[index]) == Tombstone:
                j = index

            elif self.keys[index] != None:

                if self.keys[index] == key:
                    if j != -1:
                        #swap index with first Tombstone
                        self.keys[j], self.keys[index] = self.keys[index], self.keys[j]
                        self.values[j], self.values[index]  = self.values[index], self.values[j]

                    else:
                        return self.values[index]

            else:
                return None
            x = x + 1
            index = offset + p(x)

    def delete(self, key):
        if key is None:
            raise KeyError("Key is None. Not allowed")
        x = 0
        hash_value = hash(key)
        offset = self.normalize_index(hash_value)
        index = offset
        while True:

            if self.keys[index] is None:
                return None

            else:
                if self.keys[index] == key:
                    val = self.values[index]
                    self.keys[index] = Tombstone()
                    self.values[index] = None
                    self.keys_count -= 1
                    return val
            x += 1
            index = self.normalize_index(offset + p(x))

    def key_function(self, key):
        return key % self.capacity


def next2Power(i):
    return 2 ** (math.floor(math.log(i, 2)) + 1)


#Probing function for open hashing collision
def p(x):
    return (x**2 + x)>> 1




h = HashTable()
h.insert("Bob", 1)
h.insert("Alice", 2)
h.insert("Something", 100)
# h.delete("Alice")
print(h.get("Alice"))


it = iter(h)

print(next(it))
print(next(it))
print(next(it))
print(next(it))

