#!/usr/bin/python

import sys

def increment(seq, pos):
	if pos < len(seq):
		seq[pos] += 1
		if seq[pos] > 4:
			seq[pos] = 0
			seq = increment(seq, pos + 1)
	return seq

def operate(val, op, num):
	if op == 0:
		val = val + num
	elif op == 1:
		val = val - num
	elif op == 2:
		val = val * num
	elif op == 3:
		if (val % num) == 0:
			val = val / num
		else:
			val = 0
	return val

def displayop(op):
	string = ""
	if (op < 4):
		string += (" + ", " - ", " * ", " / ")[op]
	return string

def calc(nums, seq):
	val = nums[0]
	for pos in range(len(nums) - 1):
		if val != 0:
			val = operate(val, seq[pos + 1], nums[pos + 1])
	return val

def display(nums, seq):
	string = "(" * (len(nums) - 1) + str(nums[0])
	for pos in range(len(nums) - 1):
		if seq[pos + 1] != 4:
			string += displayop(seq[pos + 1])
			string += str(nums[pos + 1])
		string += ")"
	return string

def permutations(elements):
	if len(elements) <=1:
		yield elements
	else:
		for perm in permutations(elements[1:]):
			for i in range(len(elements)):
				yield perm[:i] + elements[0:1] + perm[i:]

def getclose(nums, find, closest, closelist):
	op = [0] * len(nums)
	while op != [4] * len(nums):
		op = increment(op, 0)
		val = calc(nums, op)
		diff = abs(val - find)
		if diff < closest:
			closest = diff
			closelist = [(nums, op[:])]
		elif diff == closest:
			closelist += [(nums, op[:])]
		if diff == 0 and len(closelist) == 1:
			print(display(nums, op))
	return (closest, closelist)

if len(sys.argv) > 2:
	find = int(sys.argv[len(sys.argv) - 1])
	nums = []
	for pos in range(1, len(sys.argv) - 1):
		nums += [int(sys.argv[pos])]
	closest = 100000000000
	closelist = []

	for perm in permutations(nums):
		res = getclose(list(perm), find, closest, closelist)
		closest = res[0]
		closelist = res[1]

	output = []
	for seq in closelist:
		output += [display(seq[0], seq[1])]

	unique = set(output)

	print()
	print("Found: {}".format(len(unique)))
	for seq in unique:
		print(seq)

	print()
	print("Found: {}".format(len(unique)))
	print("Closest: {}".format(closest))
else:
	print("Syntax: naive n1 n2 n3 n4 n5 n6 sun")

