import random as random

# Returns:
#	Cell value of the given coordinates in the maze array
def get(arr, w, x, y):
	return arr[y*w+x]

# Sets the given coordinaes in the maze array to the given value 
# Returns:
#	Maze array
def set(arr, w, x, y, val):
	arr[y*w+x] = val

	return arr

# Returns:
#	True if the given coordinates are within the bounds of the maze
# 	False otherwise
def inBounds(w, h, x, y):
	 return 0 <= x and x < w and 0 <= y and y < h

# Returns:
#	True if the given coordinates are out of the maze's bounds
#	True if the cell in the array has been traversed in maze generation
# 	False otherwise
def isVisited(arr, w, h, x, y):
	if not inBounds(w, h, x, y):
		return True

	if get(arr, w, x, y) != 11:
		return True

	# If the cell to the Left is within maze bounds
	if inBounds(w, h, x-1, y):
		# AND if that left cell does NOT have its right-facing wall
		if get(arr, w, x-1, y) % 10 == 0:
			return True

	# If the cell to the Up is within maze bounds
	if inBounds(w, h, x, y-1):
		# AND if that left cell does NOT have its down-facing wall
		if get(arr, w, x, y-1) / 10 == 0:
			return True

	return False

def isRoomAvailable(arr, w, h, x, y, dirs):
	for d in dirs:
		if d == 1:
			y -= 1
		elif d == 2:
			x += 1
		elif d == 3:
			y += 1
		elif d == 4:
			x -= 1

		if d != 5 and isVisited(arr, w, h, x, y):
			return False

	return True

# Traverses in all four directions from the given cell in a random order.
# Depth-first
# Returns:
#	Maze array
def moveRandomly(arr, w, h, x, y):
	dirs = [1,2,3,4]
	random.shuffle(dirs)

	for d in dirs:
		# Up
		if d == 1:
			if not isVisited(arr, w, h, x, y-1):
				# If the cell Up of current is not visited
				# Remove Up cell's down-facing wall
				arr = set(arr, w, x, y-1, 1)

				#Traverse Up
				arr = step(arr, w, h, x, y-1)
		# Right
		elif d == 2:
			if not isVisited(arr, w, h, x+1, y):
				# If the cell Right of current is not visited
				# Removes the current cell's right-facing wall
				curr = get(arr, w, x, y)
				arr = set(arr, w, x, y, curr-1)

				# Traverse Right
				arr = step(arr, w, h, x+1, y)
		# Down
		elif d == 3:
			if not isVisited(arr, w, h, x, y+1):
				# If the cell Down of current is not visited
				# Remove current cell's down-facing wall
				curr = get(arr, w, x, y)
				arr = set(arr, w, x, y, curr-10)

				#Traverse Down
				arr = step(arr, w, h, x, y+1)
		# Left
		elif d == 4:
			if not isVisited(arr, w, h, x-1, y):
				# If the cell Left of current is not visited
				# Remove Left cell's right-facing wall
				arr = set(arr, w, x-1, y, 10)

				#Traverse Left
				arr = step(arr, w, h, x-1, y)

	return arr


def generateRoom(arr, w, h, x, y, dirs):
	if len(dirs) == 0:
		return arr

	d = dirs.pop(0)

	# Up
	if d == 1:
		curr = get(arr, w, x, y-1)
		if curr / 10 == 1:
			arr = set(arr, w, x, y-1, curr-10)
		arr = generateRoom(arr, w, h, x, y-1, dirs)

	# Right
	elif d == 2:
		curr = get(arr, w, x, y)
		if curr % 10 == 1:
			arr = set(arr, w, x, y, curr-1)
		arr = generateRoom(arr, w, h, x+1, y, dirs)

	# Down
	elif d == 3:
		curr = get(arr, w, x, y)
		if curr / 10 == 1:
			arr = set(arr, w, x, y, curr-10)
		arr = generateRoom(arr, w, h, x, y+1, dirs)

	# Left
	elif d == 4:
		curr = get(arr, w, x-1, y)
		if curr % 10 == 1:
			arr = set(arr, w, x-1, y, curr-1)
		arr = generateRoom(arr, w, h, x-1, y, dirs)

	# Remember exit point
	elif d == 5:
		arr = generateRoom(arr, w, h, x, y, dirs)
		step(arr, w, h, x, y)

	return arr


# Take a step in traversal
def step(arr, w, h, x, y):
	global roomList

	# Attempts to build room
	for r in roomList:
		if isRoomAvailable(arr, w, h, x, y, r):
			arr = generateRoom(arr, w, h, x, y, r[:])
			print "Made room at ",
			print (x,y)

	arr = moveRandomly(arr, w, h, x, y)

	return arr



# Depth-first traversal generation of a maze
# 	[width] cells wide and [height] cells high
# 	Cell (0, 0) will be the upper-left hand corner
#	Cell (width-1, 0) will be the upper-right hand corner
#
#	Each cell can have four possible values of [00, 10, 01, 11]
#		The first digit is [0] if the cell has no down-facing wall, [1] if it does
#		The second digit is [0] if the cell has no right-facing wall, [1] if it does
#
# Returns:
#	Maze in the form of a one-dimensional array of integers
def generate(width, height):
	# Initializes maze for all cells to have both down-facing and right-facing walls
	arr = [11]*(width*height)

	# Random starting point to begin traversal
	x = random.randint(0, width-1)
	y = random.randint(0, height-1)

	arr = step(arr, width, height, x, y)

	return arr


def parseRoomsFile(path):
	global roomList
	roomList = []

	for line in open(path, "r"):
		if line[0] == ">":
			curr = line[1:].split(",")

			# Initialize starting space as a branching-off point
			dirs = [5]
			
			for d in curr:
				dirs += [int(d)]
			
			roomList += [dirs]

	random.shuffle(roomList)




# Entry point
parseRoomsFile("rooms.txt")

width = 30
height = width
maze = generate(width, height)


# Prints the maze
print "\n_",
for x in range(width):
	print " _ ",
print "\n",
for y in range(height):
	print "|",
	for x in range(width):
		curr = get(maze, width, x, y)
		if curr / 10 == 1:
			print "_",
		else:
			print " ",
		if curr % 10 == 1:
			print "|",
		else:
			print " ",
	print "\n",




























