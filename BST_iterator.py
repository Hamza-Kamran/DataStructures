from BST import BST

class InorderIterator():

    def __init__(self, tree):
        self.root = tree.root
        self._nextitem = None
        self._hasnext = None

    def __iter__(self):
        return self

    def hasnext(self):
        if self._hasnext is None:
            try:
                item = next(self)
                self._nextitem = item
                return True
            except StopIteration:
                self._hasnext = False
                return False
        else:
            self._hasnext = True
        return self._hasnext


    def __next__(self):
        yield from self._generate()


    def _generate(self):
        #using morris traversal with O(n) time complexity and O(1) space complexity

        #there is already a next so use that
        if self._hasnext:
            result = self._nextitem
            self._hasnext = None
            return result
        else:
            #there is no next stored so use morris traversal
            curr = self.root

            while curr is not None:
                #no left branch so visit the current root and move down right
                if curr.left is None:
                    result = curr.data
                    yield result
                    curr = curr.right

                #there is a left branch so visit the rightmost left child and connect it to parent
                else:
                    parent = curr
                    curr = curr.left
                    while curr.right and curr.right != parent:
                        curr = curr.right

                    # we already visited the node so now go to right child
                    if curr.right == parent:
                        result = parent.data
                        yield result
                        curr = parent.right

                    else:
                    #we have not visited the node so visit it
                        curr.right = parent
                        curr = parent.left
            self.root = curr


if __name__ == "__main__":
    tree = BST()
    print(tree.add(5))
    print(tree.add(2))
    print(tree.add(1))
    print(tree.add(9))
    print(tree.add(100))

    i = InorderIterator(tree)
    gen_obj = next(i)
    print(next(gen_obj))
    print(next(gen_obj))
    print(next(gen_obj))
    print(next(gen_obj))
    print(next(gen_obj))
