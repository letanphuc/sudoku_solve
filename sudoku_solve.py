import sys
import math
import time


SIZE = 9
SMALL_SIZE = int(math.sqrt(SIZE))
total_step = 0
print_log = False

def not_fixed(x):
	if x == 0:
		return True
	else:
		return False

def parse_input(filename):
	sudoku_map = []
	input_file = open(filename, 'r')

	for line in input_file:
		line = line.replace(' ', '').replace('\n', '').replace('\r', '')
		if len(line) >= SIZE:
			for i in range(0, SIZE):
				c = line[i]
				if c == 'x':
					sudoku_map.append(0)
				else:
					sudoku_map.append(ord(c) - ord('0'))
	return sudoku_map

def print_map(sudoku_map):
	if len(sudoku_map) == (SIZE*SIZE):
		print '-'*25
		for i in range(0, SIZE):
			for j in range(0, SIZE):
				c = sudoku_map[i*SIZE + j]
				if not not_fixed(c):
					if (j % SMALL_SIZE) == 0:
						sys.stdout.write("| %d " %c)
					else:
						sys.stdout.write("%d " %c)
				else:
					if (j % SMALL_SIZE) == 0:
						sys.stdout.write("| x " )
					else:
						sys.stdout.write("x ")
			print '|'
			if (i % SMALL_SIZE) == (SMALL_SIZE - 1):
				print '-'*25

def scan_values(x, y, sudoku_map):
	values = []
	for i in range(0, SIZE):
		# row
		if not (sudoku_map[i*SIZE + y] in values):
			values.append(sudoku_map[i*SIZE + y])
		# col
		if not (sudoku_map[x*SIZE + i] in values):
			values.append(sudoku_map[x*SIZE + i])

	row = x - (x % SMALL_SIZE)
	col = y - (y % SMALL_SIZE)
	for i in range(row, row + SMALL_SIZE):
		for j in range(col, col + SMALL_SIZE):
			if not (sudoku_map[i*SIZE + j] in values):
				values.append(sudoku_map[i*SIZE + j])
	return values

def find_first(sudoku_map):
	for i in range(0, SIZE):
		for j in range(0, SIZE):
			if not_fixed(sudoku_map[i*SIZE+j]):
				return (i,j)
	return (-1, -1)

def list_available(x, y, sudoku_map):
	values = []
	exits = scan_values(x, y, sudoku_map)
	for v in range(1, SIZE + 1):
		if not (v in exits):
			values.append(v)
	return values

def solve(sudoku_map, degree):
	global total_step
	total_step += 1
	(x, y) = find_first(sudoku_map)
	if x == -1  or y == -1:
		#end & have fun !
		return (True, sudoku_map)
	else:
		values = list_available(x,y,sudoku_map)
		if len(values) == 0:
			# it is not the right way
			if print_log:
				print '[%d] Death at (%d, %d)' %(degree, x, y)
			return (False, sudoku_map)

		if print_log:
			print '[%d] List of (%d, %d)' %(degree, x, y) , '=', values

		for v in values:
			sudoku_map[x*SIZE + y] = v
			if print_log:
				print '[%d] Fill %d -> (%d, %d)' %(degree, v, x, y)
			# print_map(sudoku_map)

			(result, sudoku_map) = solve(sudoku_map, degree + 1)
			if result:
				# found the answer
				return (True, sudoku_map)

		# return to the parent
		sudoku_map[x*SIZE + y] = 0		
		return (False, sudoku_map)
	return (False, sudoku_map) # not go here

# main function here
sudoku_map = parse_input(sys.argv[1])
print 'Beggin:'
print_map(sudoku_map)

start = time.time()
(result, sudoku_map) = solve(sudoku_map, 0)
end = time.time()

if result:
	print "pingo :)"
else:
	print 'can not solve :('
print 'Time = ', (end - start), 'seconds'
print 'Total step = ', total_step
print_map(sudoku_map)

