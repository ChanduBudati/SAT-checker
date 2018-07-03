#!/usr/bin/env python3
import sys
import copy

class literal:
	def __init__(self, var):
		self.var = var
	def evaluate(self, vlist):
		val = vlist[abs(self.var)]
		if self.var < 0:
			if val == 0:
				val = 1
			elif val == 1:
				val = 0
		return val

class clause:
	def __init__(self, clist):
		self.literals = list()
		for lit in clist: 
			self.literals.append(literal(lit))
	def evaluate(self, vlist):
		for lit in self.literals:
			if lit.evaluate(vlist) == 1:
				return True
		return False
	def popfalse(self, vlist):
		for i in self.literals:
			if i.evaluate(vlist) == 0:
				self.literals.remove(i)

def dpll(cdata, vlist):

	rlist = []
	for c in cdata:
		if c.evaluate(vlist):
			rlist.append(c)
	for i in rlist:
		cdata.remove(i)
	for i in range(len(cdata)):
		cdata[i].popfalse(vlist)

	if(len(cdata) == 0):
		print("SATISFIABLE")
		for i in vlist.keys():
			if vlist[i] != -1:
				print(str(i) + "\t" + str(vlist[i]))
		return True
	for i in cdata:
		if len(i.literals) == 0:
			return False

	for i in cdata:
		if len(i.literals)== 1:
			if vlist[abs(i.literals[0].var)] == -1:
				vlist1 = copy.deepcopy(vlist)
				if i.literals[0].var < 0:
					vlist1[abs(i.literals[0].var)] = 0
					cdata1 = copy.deepcopy(cdata)
				else :
					vlist1[abs(i.literals[0].var)] = 1
					cdata1 = copy.deepcopy(cdata)
				if not dpll(cdata1, vlist1):
					return False
				return True

	for i in vlist.keys():
		if vlist[i] == -1:
			vlist1 = copy.deepcopy(vlist)
			vlist1[i] = 1
			cdata1 = copy.deepcopy(cdata)
			v1 = dpll(cdata1, vlist1)
			if v1:
				return True
			vlist1[i] = 0
			cdata1 = copy.deepcopy(cdata)
			v0 = dpll(cdata1, vlist1)
			if v0:
				return True
			return False

def main():
	file = open("IN7",'r')
	data = file.read().splitlines()
	cdata = list()
	vlist = {}
	for i in data:
		if 'p' not in i and 'c' not in i:
			i = [int(lit) for lit in i.split()]
			cdata.append(i)
	for i in range(len(cdata)):
		for j in cdata[i][:-1]:
			if abs(j) not in vlist.keys():
				vlist[abs(j)] = -1
		cdata[i] = clause(cdata[i][:-1])
	if not dpll(cdata, vlist):
		print("UNSATISFIABLE")
main()