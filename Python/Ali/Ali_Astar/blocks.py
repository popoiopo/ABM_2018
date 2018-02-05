from agents import *
from model import *


# ------------------Functions--------------------------

def create_block(self, location_list, POI_locations):

	for i in range(len(location_list)):
			this_cell = self.grid.get_cell_list_contents(location_list[i])

			for agent in this_cell:
				if type(agent) is nodeAgent:
					agent.block = True

					for i in POI_locations:
						agent.locations[i] = 10000


def create_POI(self,location_list,moore_range):
	for r in range(len(location_list)):

		x = location_list[r][0]
		y = location_list[r][1]



		coordinates =[]
		for i in range(moore_range):
			for j in range(moore_range):
				if x+i > 0 and  len(self.grid_density) > x+i and y+j > 0\
				 and  len(self.grid_density[0]) > y+j:

					coordinates.append( (x+i,y+j) )
					coordinates.append( (x-i,y-j) )
					coordinates.append( (x-i,y+j) )
					coordinates.append( (x+i,y-j) )

		# for i in range(1, moore_range):

		# 	coordinates =[]
		# 	for j in range(2*i +1):

		# 		coordinates.append( (x+i, y-i+j))
		# 		coordinates.append( (x-i, y-i+j))

		# 	for k in range(1,2*i):
		# 		coordinates.append((x-i+k, y+i))
		# 		coordinates.append((x-i+k, y-i))


			for coords in coordinates:
				#if math.pow((coords[0] - x), 2) + math.pow((coords[1] - y), 2) <= math.pow(moore_range, 2):
				if not self.grid.out_of_bounds(coords):
					this_cell = self.grid.get_cell_list_contents(coords)

					for agent in this_cell:
						if type(agent) is nodeAgent:

							agent.POI = True
							
											

#------------------variables--------------------------
block_positions = []

block_list =[\
]

# [(20 + i, 5) for i in range(15)],
# [(20, 11), (20, 12), (20, 13), (20, 14)],
# [(20 + i, 20) for i in range(10)],
# [(20, 41), (20, 42), (20, 43), (20, 44)],
# [(25, 20 + i) for i in range(10)],
# [(25, 10 + i) for i in range(10)],
# [(10, 0 + i) for i in range(10)],
# [(0 + i, 30) for i in range(10)],
 #[(2 + i, 36) for i in range(30)],
 #[(2+i, 34) for i in range(48)]]



blocks = [item for sublist in block_list for item in sublist]

for b in blocks:
	block_positions.append(b)
