# BST is a wrapper around all nodes.
class BST:
    node_count = 0
    root = None

    # can also make this recursive
    def contains(self, elem):
        if not self.root:
            return False
        curr = self.root
        while curr:
            # print("curr is: ", curr.data)
            # print("left: " , curr.left)
            # print("right: ",  curr.right)
            if curr.data < elem:
                curr = curr.right
            elif curr.data > elem:
                curr = curr.left
            else:
                return True
        return False

        # public method, simply public facing interface for adding

    def add(self, elem):
        if self.contains(elem):
            return False

        else:
            self.root = self.add_node(self.root, elem)
            self.node_count += 1
            return True

        # should be a private method
        # add a node to the BST, current element is node

    def add_node(self, node, elem):
        if node is None:
            node = Node(None, None, elem)

        else:
            if elem < node.data:
                node.left = self.add_node(node.left, elem)
            else:
                node.right = self.add_node(node.right, elem)
        return node

        # wrapper around remove_node, user facing

    def remove(self, elem):
        if not self.contains(elem):
            return False
        root = self.root
        self.remove_node(root, elem)
        self.node_count -= 1
        return True

        # actual method to remove
        # mutates but also returns value

    def remove_node(self, node, elem):
        if node is None:
            return node
        # 3 different cases
        if elem < node.data:
            node.left = self.remove_node(node.left, elem)
        elif elem > node.data:
            node.right = self.remove_node(node.right, elem)

        else:
            # 3 cases
            # if there is no left child, return the node on the right which will later
            # be assigned to node.right or node.left

            if node.left is None:
                right_child = node.right
                node.data = None
                node = None
                return right_child
            if node.right is None:
                left_child = node.left
                node.data = None
                node = None
                return left_child

            else:
                smallest = node.right

                # traverse ↙ direction to find smallest node in right subtree
                # aka dig left
                while smallest.left:
                    smallest = smallest.left
                node.data = smallest.data
                # remove node to prevent duplicates
                self.remove_node(smallest, smallest.data)

    def height(self, node):
        if node is None: return 1
        return max(self.height(node.left), self.height(node.right)) + 1

    def size(self):
        return self.node_count

    def is_empty(self):
        return self.node_count == 0


class Node:
    data = None
    left = None
    right = None

    def __init__(self, left: 'Node', right: 'Node', data):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data) + " " + str(self.left) + " " + str(self.right)


if __name__ == "__main__":
    tree = BST()
    tree.add(4)
    print(tree.contains(4))
    print("adding 100: ", tree.add(100))
    print("100 in tree: ", tree.contains(100))
    print("Adding 5: " , tree.add(5))
    print("5 in tree: ", tree.contains(5))
    print("removing 5: ", tree.remove(5))
    print("5 in tree: ", tree.contains(5))

    print("height of tree: ", tree.height(tree.root))

    print("size: ", tree.size())
