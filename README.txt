# TODO.PY
## A Python script for managing a personal Todo.txt file.

This script can be used to interact with `todo.txt`, a text file which represents the _next actions_ list in a GTD-like productivity system. It has support for _contexts_ (different kinds of tasks) and _projects_ (grouping tasks into arbitrary groups). You can quickly view all the current tasks, certain contexts and projects, or a combination of both. Tasks can be quickly added and removed from the `todo.txt` file from the command line.

Todo.py doesn't do priorities, or deadlines, or anything else. It's a simple example of how Python can read and write plain text files, created as a teaching example. The rest of this `README` file contains a walk through the original version of the source code, published on [Two Stops Down][1] in May of 2009.

[1]: http://www.twostopsdown.com/2009/04/30/using-python-to-manage-todotxt

## History

24/04/2011: Original script and article as they appeared on Two Stops Down.

# Using Python to Manage Todo.txt

As my first experiment with the Python programming language, I made a
script that helps me look at things in my `todo.txt` file.

Even if you don't know Python, this should be pretty easy to follow. I'll step
through it with you!

    #!/usr/bin/env python
    #Filename: todo.py
    # A script to do things with todo.txt

These lines are just housekeeping. We're saying where Python is on the system
and what we're here to do.

    import os
    import sys
    import re

Bringing in a few things to help us do things. `os` helps us get the location
of the todo.txt file, `sys` allows us to read command line arguments, and `re`
lets us do regular expressions.

    # Configuration
    
    todo_path = os.path.expanduser('~/todo.txt')

Somewhere for us to set the location of our file. The `os.path.expanduser`
replaces the `~` with our actual home directory.

Now we're onto our **functions**. These are things our program will do, and we
define them here rather than write it out every time we use it.

    def LoadTodos():
    	global todos
    	todo_file = open(todo_path, 'r')
    	raw_todos = todo_file.readlines()
    	todo_file.close()
    	todos = []
    	for item in raw_todos:
    		item = item.strip("\n")
    		todos.append(item)

Our first function, `LoadTodos()`, does a few things. First of all, it opens
our `todo.txt` in a read-only mode. Next up, it pulls all the text out and
puts all the lines of text into a list (array). Just to finish up, we go
through each item and remove any line breaks - we add them ourselves later on.

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

This function adds things to our `todo.txt`. This time, the file is opened in
append mode. This mode means every time we write to the file, we're just
adding on to the end of it.

Once we have the file, we check to see if we're on a new line already. We
check the very last character of the very last line and see if it's a new line
`\n`.

Finally, we check if we have any data to add, and then write it to the file.
We also add a newline (just a convention of mine).

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

Our last function is used to show our results. This is more complex.

This function takes two arguments. It takes the results we're going to show,
as well as something called 'numbers', which we set to 1 by default. This
variable says if we want to enumerate the results or not.

Firstly we run a sanity check. If we have no results, we have nothing to show.
So we say just that.

If we do have results, we start a counter, and iterate through them. If we're
enumerating, we print them like "1. First item", "2. Second item", etc. If
not, we just print it.

    # And on with the show...
    
    # If we've got nothing to do, show what we've got!
    if len(sys.argv) == 1:
    	LoadTodos()
    	ShowResults(todos)
    	sys.exit()

If someone just runs the script by itself (i.e., there are no arguments), we
run our `LoadTodos() `function and show the results. We then run sys.exit() to
finish up early.

    # What if we want to look up something?
    arg = sys.argv[1:]
    results = []

Here's some more housekeeping. Notice how earlier, to check if there were no
arguments, we checked to see if `sys.argv` (a list of command line arguments)
had _one_ entry? The command itself is included as a command line argument, so
we have to trim that off somehow. Here, we make a new variable, `arg`, and
give it all the arguments bar the first (`sys.argv[0]`).

We also start an empty list called results, for when we need it.
 
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

Now we have our arguments, we can start to parse it. Here we say, if the first
argument we get is an 'equals' sign or an 'at' sign, we load our `todo.txt`
and find all words starting with an equals or an at.

Just to explain my `todo.txt`: Each line is an action item, and optionally a
project (prefixed with an equals sign), and a context (prefixed with an at
sign). For example, if I have something to do with my website that I could
only do at my desk, it would appear like:

 
    Change all the fonts to Crazy ITC. [=website @desk]

I usually keep these tags in square brackets, for purely aesthetic reasons.
Back to the code!

Whenever we find a word beginning with an equals or at sign, we add it to
projects, which is a **set**. A set is like a list, except _its items are
unique_. If you try to add something it already has, nothing happens. That
way, we get a unique-ified list of all our projects or contexts. We then use the
ShowResults() function to show the results in a list, with the optional number
parameter set to 0.

Here's an example output:

    > todo =
    
    =photography
    =website
    =dinner
    =cookies
    
To continue:

    elif arg[0][0] == '@' or arg[0][0] == '=':
    	#Yes, we are looking for something! Let's find it.
    	search_terms = "|".join(arg)
    	regex = re.compile(search_terms)
    	LoadTodos()
    	for item in todos:
    		if re.search(regex, item):
    			results.append(item)
    	ShowResults(results)

Next, we check to see if the first _character_ of the first argument is an
equals or an at sign. In this case, we assume we're wanting to look at items
that belong to certain projects or contexts.

To do this, we're putting together a regular expression, separating each of
our arguments by a bar. In regular expressions, this means 'or', so it picks
up items that contains any of the arguments. We put these all in our results
list, and then show them.

In practice:

    > todo @town @home
    
    1. Take out the trash [@home]
    2. Bank heist [@town =mafia]

Onward:

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

Now we're getting deep. We want to do the same as before, but we want items
that match _all_ of the arguments. This is tricky to do in a single regular
expression, as the terms could be in any order in the `todo.txt` file.

To get around this we start with a list of all of our `todo.txt` items, and
iterate through each of our arguments, filtering the list down term by term.
Matching items are put into a new variable, which is then filtered by the next
argument, and so on. The remaining results are then shown.

For example:

    > todo @school =photography
    
    1. Ask repographics about A2 prints, kinds of paper? [@school =photography =bigprints]
    2. Play baseball with the Canon 1500mm f/5.6 [@school =sport =photography]

Let's continue:

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
    	if to_del != "q":
    		new_todos = []
    		for item in todos:
    			if item != numbered_results[int(to_del)]:
    				new_todos.append(item)
    		todo_file = open(todo_path, 'w')
    		todo_file.write("\n".join(new_todos))
    		todo_file.close()
    
Last but not least, one of the hardest. What's the easiest way to delete items
from our todo list? We're already numerating our search results, so with this
solution, we input the number of the item that's completed, and it removes it
from the file. To be specific, it opens our `todo.txt` in a **write** mode.
When we write to the file now, it completely overwrites it with our new list.

I won't go into depth on what's going on here, but essentially we're cloning
our first searching mechanism. We're then showing them to the user, asking for
a number, and then numerating the results for Python using a _dictionary_ (the
same as a two-dimensional array in PHP). This is just so Python can relate the
number it gets to an actual entry.

It then goes through the `todo.txt`, find the item we completed, and removes
it from its own internal copy of the list. We then write it out to the file,
using the join method to convert our array into a text stream.

Here's an example of it in action:

    > todo done @home
    
    1. Take out the trash [@home]
    
    ? 1

This removes the entry `"take out the trash"` from `todo.txt`.
 
    else:
    	# Looks like we want to add something instead.
    	WriteTodos(arg)
 
Well, all right. One more thing. If we've entered something else that we
haven't identified so far, we use our `WriteTodos()` function to add a new
entry to our file. For example:

    > todo "Give up on Ruby [=python]"
    
… adds the entry to the file.

It's a big job for such a simple task, but it's a good demonstration of some
simple file input-out, as well as integrating regular expressions into Python
functions.

I hope this was an interesting look at some basic code. Take care!

