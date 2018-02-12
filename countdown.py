#!/usr/bin/python

""" Does the Countdown numbers game. Give it a list of numbers. It'll use all
but the last number in a formula using the +, -, * and / operators to try
to generate the last number. Only integer arithmetic is allowed, and not all
of the numbers need to be used.

Syntax: countdown n_1 n_2 ... n_m sum

Licensed under the MIT licence. See the LICENSE file for details.

David Llewellyn-Jones, 2018
david@flypig.co.uk
"""

import copy
import sys

def findprev(layer, cols):
	"""For a particular column in a particular layer, find the next earlier
	column in the layer that contains a node
	"""
	found = -1
	pos = cols - 1
	while (pos >= 0) and (found < 0):
		if layer[pos] == 1:
			found = pos
		pos = pos - 1
	return found

def shuntup(layer, end):
	""" Given a particular choice of attaching nodes in columns to create a layer
	move to the next layer configuration in the enumeration
	"""
	movedto = -1
	last = findprev(layer, end)
	if last >= 0:
		if last == (end - 1):
			movedto = shuntup(layer, last)
			if movedto >= 0:
				movedto = movedto + 1
				layer[last] = 0
				layer[movedto] = 1
		else:
			layer[last] = 0
			layer[last + 1] = 1
			movedto = last + 1

	return movedto

def evaluate(formula, operators, numbers):
	""" Evaluate a formula represented as a tree into a single integer result
	If the formula involves a non-integer division, NaN will be returned
	"""
	calc = float("NaN")
	left = formula[0]
	op = operators[formula[1]]
	right = formula[2]

	if isinstance(left, list):
		left = evaluate(left, operators, numbers)
	else:
		left = numbers[left]

	if isinstance(right, list):
		right = evaluate(right, operators, numbers)
	else:
		right = numbers[right]

	if op == 0:
		calc = left + right
	elif op == 1:
		calc = left - right
	elif op == 2:
		calc = left * right
	elif op == 3:
		if (right != 0) and (left % right == 0):
			calc = left / right
	elif op == 4:
		calc = left
	elif op == 5:
		calc = right

	return calc

def formulatostring(formula, operators, numbers):
	""" Convert a formula represented as a tree into a string representation
	"""
	calc = ""
	left = formula[0]
	op = operators[formula[1]]
	right = formula[2]

	if isinstance(left, list):
		left = formulatostring(left, operators, numbers)
	else:
		left = str(numbers[left])

	if isinstance(right, list):
		right = formulatostring(right, operators, numbers)
	else:
		right = str(numbers[right])

	if op == 0:
		calc = "(" + left + ' + ' + right + ")"
	elif op == 1:
		calc = "(" + left + " - " + right + ")"
	elif op == 2:
		calc = "(" + left + " * " + right + ")"
	elif op == 3:
		calc = "(" + left + " / " + right + ")"
	elif op == 4:
		calc = left
	elif op == 5:
		calc = right

	return calc

def permutations(elements):
	""" From a list of elements return a list of permutations of those elements
	"""
	if len(elements) <=1:
		yield elements
	else:
		for perm in permutations(elements[1:]):
			for i in range(len(elements)):
				yield perm[:i] + elements[0:1] + perm[i:]

def buildformula(built):
	""" Build a formula from a sparse representation of a binary tree. The tree is
	represented as a list of lists, one list for each row. The list in each
	row represents list of zeroes and ones. A zero means there are no
	children to the node, a one means there are two children of the node.
	This provides a cononical encoding of the tree, which can be rebult fully,
	and this function converts it into a tree formed as a set of nested lists,
	each element either containing a trio containing two subelements and an
	operator, or a number representing a leaf node.
	"""
	formula = copy.deepcopy(built)

	leaf = 0
	operator = 0
	for layer in range(len(built)):
		if built[layer] != 0:
			for op in range(len(built[layer])):
				if built[layer][op] == 1:
					formula[layer][op] = [0, operator, 0]
					operator = operator + 1
				else:
					formula[layer][op] = leaf
					leaf = leaf + 1

	for layer in range(len(built)):
		nextpos = 0
		if built[layer] != 0:
			for op in range(len(built[layer])):
				if built[layer][op] == 1:
					if (layer < len(built) - 1) and (built[layer + 1] != 0):
						formula[layer][op][0] = formula[layer + 1][nextpos]
						formula[layer][op][2] = formula[layer + 1][nextpos + 1]
						nextpos = nextpos + 2
					else:
						formula[layer][op][0] = leaf
						formula[layer][op][2] = leaf + 1
						leaf = leaf + 2
						nextpos = nextpos + 2

	return formula[0]

def shuntoperator(operators, pos):
	if pos >= 0:
		operators[pos] = operators[pos] + 1
		if operators[pos] > 4:
			operators[pos] = 0
			return shuntoperator(operators, pos - 1)
		return True
	else:
		return False

def chooselayer(connections, built, start, height, numbers, find, closest):
	""" For a given number of nodes set in each layer of a tree (defined by
	connections), starting from layer start and going up to layer height, cycle
	through all the possible trees that could be created in this configuration.
	For each such tree, cycle through all permuutations of the numbers,
	and all possible operators, and compare the output from the resulting
	formula to the number to find.
	The function will print out the closest formula it can find as it goes
	along, until hopefully an exact match is found.
	"""
	if (start < height) and (connections[start] > 0):
		hangers = 2*connections[start - 1]
		coats = connections[start]

		if hangers >= coats:
			layer = [1] * coats + [0] * (hangers - coats)
			movedto = hangers
			while movedto >= 0:
				built[start] = layer
				closest = chooselayer(connections, built, start + 1, height, numbers, find, closest)
				movedto = shuntup(layer, hangers)
	else:
		formula = buildformula(built)
		for perm in permutations(numbers):
			operators = [0] * height
			more = True
			while more:
				more = shuntoperator(operators, height - 1)
				calc = evaluate(formula[0], operators, perm)
				if calc == calc:
					distance = abs(calc - find)
					if distance <= closest:
						if (distance == 0) and (closest != 0):
							print "#######################################"

						string = formulatostring(formula[0], operators, perm) + " = " + str(calc)
						closest = distance
						print string
	return closest

def shuntconnection(connections, height, maxnodes, nodes):
	""" Given a particular configuration of connections, move to
	the next connection in the enumeration
	"""
	changed = 0

	if (height >= 1):
		current = connections[height - 1]
		nodesbelow = nodes - current

		if (height <= 1):
			prev = 0
		else:
			prev = connections[height - 2]

		if (current >= 2**prev) or (nodesbelow + current >= maxnodes):
			changed = shuntconnection(connections, height - 1, maxnodes, nodesbelow)

			if nodesbelow + changed < maxnodes:
				connections[height - 1] = 1
				changed = changed - current + 1
				if height == maxnodes:
					changed = -1
			else:
				connections[height - 1] = 0
				changed = changed - current
		else:
			connections[height - 1] = current + 1
			changed = 1

	return changed

def connections(numbers, find):
	""" Cycle through all of the possible trees that contain a given fixed number
	of nodes
	"""
	nodes = len(numbers) - 1
	connections = [1] * nodes
	changed = 0;

	closest = 10000000000	
	while changed == 0:
		#print connections
		built = [[1]] + [0] * (nodes - 1)
		closest = chooselayer(connections, built, 1, nodes, numbers, find, closest)
		changed = shuntconnection(connections, nodes, nodes, nodes)


""" Main entry point
"""
if len(sys.argv) > 3:
	find = int(sys.argv[-1])
	nums = map(int, sys.argv[1:-1])

	connections(nums, find)
else:
	print "Syntax: countdown n_1 n_2 ... n_m sum"



