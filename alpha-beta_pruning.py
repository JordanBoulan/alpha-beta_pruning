"""
Implements alpha-pruning and prints the order nodes were searched, not all nodes are searched since we prune.

Authors: Jordan Boulanger
Version: July 6th, 2023
"""

def best_first(graph, start):
	""" Gets of list of nodes to look at next based on a certain starting point
    
    :param graph: the graph to be used
    :param start: the current starting node to start opening nodes from
    :return: a list of the the nodes based on a heuristic for searching the graph from a starting node, this is not the same as the path taken because of the recursive nature of the prune function
    """
	
	opened = []
	cs = start
	index = 0
	for j in range(len(graph)):
		if graph[j][0][0] == cs[0]:
			index = j
			break
	children = graph[index][1:]
	
	for i in range(len(children)):
		#let h(child) be g(node) plus child's index in children (left to right heuristic)
		child = children[i]
		child[3][0] = child[3][1] + i
		opened.append(child)
		
	return opened
	
	

def prune(graph, node, alpha, beta, depth, traversal, bound = None):
	"""Prunes nodes from a graph recursivly, searching nodes

	:param graph: The input graph
	:param node: The node to start pruning from
	:param alpha: The current alpha value
	:param beta: the current beta value
	:param depth: The current depth we are in the graph
	:param traversal: The path taken so far
	:param bound: The depth to stop search at if any (only look so far ahead which is helpful for big graphs)
	"""

	heads = [graph[i][0][0] for i in range(len(graph))]
	if node[0] not in heads:
		traversal.append(node[0])
		return node[0]
	else:
		#use best-first to find successors
		traversal.append(node[0])
		successors = best_first(graph, node)

		if node[1] == 'MAX':
			for n in successors:
				alpha = max(alpha, prune(graph, n, alpha, beta, depth + 1, traversal))
				if alpha >= beta:
					return beta
			# stop at depth bound, if any 
			if depth == bound:
				return alpha 

		if node[1] == 'MIN':
			for n in successors:
				beta = min(beta, prune(graph, n, alpha, beta, depth + 1, traversal))
				if beta <= alpha:
					return alpha
			# stop at depth bound, if any	
			if depth == bound:
				return beta 
			
		if node[1] == 'MIN':
			return beta
		if node[1] == 'MAX':
			return alpha
				
def main():
	"""each node is (node name, max/min, backpointer, [f(node), g(node)])
	"""
	space = [[('C', 'MAX', -1, [0, 0]), ('A', 'MIN', 'C', [0, 1]), ('D', 'MIN', 'C', [0, 1]), ('E', 'MIN', 'C', [0, 1])],
			 [('A', 'MIN', 'C', [0, 1]), ('P', 'MAX', 'A', [0, 2]), ('B', 'MAX', 'A', [0, 2])],
			 [('D', 'MIN', 'C', [0, 1]), ('R', 'MAX', 'D', [0, 2]), (42, 'MAX', 'D', [0, 2])],
			 [('E', 'MIN', 'C', [0, 1]), ('T', 'MAX', 'E', [0, 2]), ('V', 'MAX', 'E', [0, 2])],
			 [('P', 'MAX', 'A', [0, 2]), (2, 'MIN', 'P', [0, 3]), (3, 'MIN', 'P', [0, 3])],
			 [('B', 'MAX', 'A', [0, 2]), (5, 'MIN', 'B', [0, 3]), (100, 'MIN', 'B', [0, 3])],
			 [('R', 'MAX', 'D', [0, 2]), (0, 'MIN', 'R', [0, 3])],
			 [('T', 'MAX', 'E', [0, 2]), (2, 'MIN', 'T', [0, 3]), (1, 'MIN', 'T', [0, 3])],
			 [('V', 'MAX', 'E', [0, 2]), (9, 'MIN', 'V', [0, 3]), (11, 'MIN', 'V', [0, 3])]]
	
	path = []
	prune(space, ('C', 'MAX', -1, [0, 0]), -float('inf'), float('inf'), 1, path)
	print(path)
	# notice that not all the nodes are in the path because we pruned nodes that we don't want to search

if __name__ == "__main__":	
	main()