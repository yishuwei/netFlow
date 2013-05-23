from collections import deque

class Network():  
  """
  build the network from file
  capacities are kept in a dict, of the form {(i,j): capacity}
  node 0 = source, node 1 = sink
  neighbors[i] returns a set containing all neighbors of node i
  """
  def __init__(self, filename):
    self.capacities = {}
    self.neighbors = []
    file = open(filename, 'r')
    for line in file:
      numbers = line.split()
      if len(numbers) == 2:
        self.neighbors.append(set())
      elif len(numbers) == 3:
        outnode = int(numbers[0])
        innode = int(numbers[1])
        self.neighbors[outnode].add(innode)
        self.capacities[(outnode, innode)] = int(numbers[2])
    file.close()
  
  """
  current flow on edge (i,j)
  """
  def getValue(self, i, j):
    if (i,j) in self.flows:
      return self.flows[(i,j)]
    elif (j,i) in self.flows:
      return -self.flows[(j,i)]
    else:
      return 0
  
  """
  compute how much flow we can push from i to j, given current flow configuration
  """
  def getMaxPushValue(self, i, j):
    return (self.capacities[(i,j)] - self.getValue(i,j))
  
  """
  push given amount of flow on a path
  path should be a list of edges (i,j)
  """
  def augment(self, path, amount):
    for i, j in path:
      if i < j:
        self.flows[(i,j)] = self.getValue(i,j) + amount
      else:
        self.flows[(j,i)] = self.getValue(j,i) - amount
  
  """
  find the shortest augmenting path, using breadth-first search
  """
  def findPath(self):
    paths = deque()
    examined = set()
    
    # all paths start from node 0
    for node in self.neighbors[0]:
      maxPushValue = self.getMaxPushValue(0, node)
      if maxPushValue > 0:
        paths.append(([(0, node)], maxPushValue))
    examined.add(0)
    
    while len(paths) > 0:
      path, amount = paths.popleft()
      endnode = path[-1][1] # last node of the path
      if endnode == 1: # shortest augmenting path found
        return path, amount
      for node in self.neighbors[endnode]:
        if node in examined: continue
        maxPushValue = self.getMaxPushValue(endnode, node)
        if maxPushValue > 0:
          paths.append((path + [(endnode, node)], min(amount, maxPushValue)))
      examined.add(endnode)
    return None, 0
  
  """
  compute the max flow on the network
  """
  def maxFlow(self):
    self.flows = {}
    while True:
      path, amount = self.findPath()
      if path == None: break # no more flow can be pushed
      self.augment(path, amount)
    
    vflow = 0
    for node in self.neighbors[0]:
      vflow += self.getValue(0,node)
    return vflow

if __name__ == '__main__':
  from sys import argv
  if len(argv) < 2:
    print "Please specify network file."
  else:
    network1 = Network(argv[1])
    print network1.maxFlow()