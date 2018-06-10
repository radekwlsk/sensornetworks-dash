class Node:
    def __init__(self, i, keys, coords):
        self.id = i
        self.keys = keys
        self.x = coords[0]
        self.y = coords[1]
        self.neighbours = set()
        self.shared_keys = dict()

    def in_range(self, node, r):
        return abs(self.x-node.x) + abs(self.y-node.y) <= r

    def establish_shared_keys(self, node):
        for k in self.keys:
            if k in node.keys:
                self.neighbours.add(node.id)
                if node.id in self.shared_keys:
                    self.shared_keys[node.id].append(k)
                else:
                    self.shared_keys.update({node.id: [k]})

    def __str__(self):
        return "Node {} ({}, {}), neighbours: {}".format(
            self.id,
            self.x,
            self.y,
            ', '.join([str(n) for n in self.neighbours])
        )

    def __repr__(self):
        return "<Node {} ({},{}) neighbours={}>".format(
            self.id,
            self.x,
            self.y,
            self.neighbours
        )
