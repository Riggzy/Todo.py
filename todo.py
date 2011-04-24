#!/usr/bin/env python
#Filename: todo.py
# A script to do things with todo.txt

import os
import sys
import re

# Configuration

todo_path = os.path.expanduser('~/todo.txt')

def LoadTodos():
	global todos
	todo_file = open(todo_path, 'r')
	raw_todos = todo_file.readlines()
	todo_file.close()
	todos = []
	for item in raw_todos:
		item = item.strip("\n")
		todos.append(item)

def WriteTodos(arguments = ""):
	LoadTodos()
	todo_file = open(todo_path, 'a')
	
	# Is there a newline aready here for us? If not, add it.
	if todos[-1][-1] != "\n":
		todo_file.write("\n")
	
	# If we've been given something, add each of them followed by a new line.
	if arguments != "":
		for item in arguments:
			todo_file.write(str(item) + "\n")
	todo_file.close()

def ShowResults(results, numbers = 1):
	print('')
	if len(results) == 0:
		print("No results.")
	else:
		i = 1
		for item in results:
			if numbers == 1:
				print("{0}. {1}".format(i, item))
			else:
				print(item)
			i += 1
	print('')

# And on with the show...

# If we've got nothing to do, show what we've got!
if len(sys.argv) == 1:
	LoadTodos()
	ShowResults(todos)
	sys.exit()

# What if we want to look up something?
arg = sys.argv[1:]
results = []

if arg[0] == "=" or arg[0] == "@":
	regex = str(arg[0]) + r"\S*"
	projects = set()
	LoadTodos()
	for item in todos:
		matches = re.findall(regex, item)
		for match in matches:
			match = match.strip("]")
			projects.add(match)
	ShowResults(sorted(projects), 0)
elif arg[0][0] == '@' or arg[0][0] == '=':
	#Yes, we are looking for something! Let's find it.
	search_terms = "|".join(arg)
	regex = re.compile(search_terms)
	LoadTodos()
	for item in todos:
		if re.search(regex, item):
			results.append(item)
	ShowResults(results)
elif arg[0][0] == '+':						# Emulate an "AND" operator.
	LoadTodos()
	old_results = todos[:]					# Start with all the items.
	for term in arg[1:]:					# Iterate through each of the terms
		new_results = []
		regex = re.compile(term)
		for item in old_results:
			if re.search(regex, item):
				item = item.strip('\n')
				new_results.append(item)	# Move matching items into a new list
		old_results = new_results			# ... which goes on to the next round.
	ShowResults(new_results)
elif arg[0] == "done":
	search_terms = "|".join(arg[1:])
	regex = re.compile(search_terms)
	LoadTodos()
	for item in todos:
		if re.search(regex, item):
			results.append(item)
	i = 1
	numbered_results = {}
	for item in results:
		numbered_results[i] = item
		i += 1
	ShowResults(results)
	to_del = input("? ")
	to_del = to_del.split()
	if to_del != "q":
		new_todos = []
		for item in todos:
			keep = True
			for number in to_del:
				if item == numbered_results[int(number)]:
					keep = False
			if keep == True:
				new_todos.append(item)
		
		todo_file = open(todo_path, 'w')
		todo_file.write("\n".join(new_todos))
		todo_file.close()
else:
	# Looks like we want to add something instead.
	WriteTodos(arg)
