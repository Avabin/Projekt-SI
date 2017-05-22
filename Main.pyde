from math import sin, cos, radians
from random import randint

width = 1200
height = 1200    #wielkosc okna
nr_of_drones = 10
nr_of_obstacles = 20
nr_of_moves = 300    #po tylu ruchach tworzone jest nowe pokolenie
max_move_dist = 20
mutation_probability = 0.03    #prawdopodobienstwo wystapienia mutacji czyli dodanie nowych ruchow w losowym miejscu listy ruchow


def setup():
    size (width, height)
    #frameRate(5)
    stroke(255)
    global generation
    print("Pokolenie nr: "+str(generation))
    generation+=1

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

class Move(object):
    def __init__(self, angle, distance):
        self.angle = angle
        self.distance = distance

    def __str__(self):
        return "Angle: " + str(self.angle) + ", Distance: " + str(self.distance)

class Entity(object):
    def __init__(self):
        self.current_angle = -90
        self.moves = list()
        self.pos = Position(startpos.x, startpos.y)
        self.currentMove = 0;
        self.smallest_distance = get_distance(self.pos, goal.pos)
        self.steps_to_closest_position = 0
        self.fitness = 0
        
    def measure_fitness(self):
        self.fitness = 1/sqrt(self.smallest_distance+1)/(self.steps_to_closest_position+1)

    def update_position(self):
        if (self.currentMove >= len(self.moves)):
            self.currentMove = 0
        global moves_made
        move = self.moves[self.currentMove]
        self.current_angle = move.angle
        x = self.pos.x + round(move.distance * cos(radians(move.angle)))
        y = self.pos.y + round(move.distance * sin(radians(move.angle)))
        if(x>0 and x < width and y >0 and y < height and check_obstacles(x,y)):
            self.pos.x=x
            self.pos.y=y
            current_distance = get_distance(self.pos, goal.pos)
            if (current_distance < self.smallest_distance):
                self.smallest_distance = current_distance
                self.steps_to_closest_position = moves_made
        self.currentMove+=1
        
    def show(self):
        fill(255)
        noStroke()
        ellipse(self.pos.x, self.pos.y, 10, 10)

    def __str__(self):
        retval = "Entity:\n" + \
                 "Current Angle: " + str(self.current_angle) + "\n" \
                 "Position: " + str(self.pos) + "\n"
        for move, i in zip(self.moves, range(0, len(self.moves))):
            retval += "Move " + str(i) + ": " + str(move) + "\n"
        return retval

    def generate_moves(self, amount, dist):
        new_moves = list()
        new_moves.append(Move(self.current_angle + randint(-30, 30), randint(dist/2, dist)))
        for i in range(1, amount):
            angle = new_moves[i-1].angle + randint(-30, 30)
            distance = randint(dist/2, dist)
            new_moves.append(Move(angle, distance))
        self.moves = new_moves
        
    def mutate(self):
        amount = randint(1,len(self.moves)/4)
        startplace = randint(1,len(self.moves))
        for i in range(startplace, startplace+amount):
            angle=self.moves[startplace-1].angle+randint(-30,30)
            distance = randint(max_move_dist/2, max_move_dist)
            self.moves.insert(i, Move(angle, distance))
            
class Obstacle(object):
    def __init__(self,x,y,width,height):
        self.pos=Position(x,y)
        self.width = width
        self.height = height
        
    def show(self):
        fill(200,100,100)
        strokeWeight(4)
        stroke(0)
        rect(self.pos.x, self.pos.y, self.width, self.height, 4)

class Goal(object):
    def __init__(self, pos):
        self.pos = pos
        
    def show(self):
        fill(20,250,20)
        stroke(0)
        ellipse(self.pos.x, self.pos.y, 30, 30)
        
def check_obstacles(x,y):
    for obstacle in obstacles:
        if (x > obstacle.pos.x and
            x < obstacle.pos.x + obstacle.width and
            y > obstacle.pos.y and
            y < obstacle.pos.y + obstacle.height):
            return 0
    return 1

def get_distance (a, b):
    return (a.x - b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y)

def get_random_position():    #zwraca obiekt klasy Position z losowymi wspolrzednymi mieszczacymi sie na ekranie minimum 30 pikseli od krawedzi
    x = randint(30,width-30)
    y = randint(30,height-30)
    return Position(x,y)

def prepare_drones():
    fitness_sum = 0
    global drones
    for drone in drones:
        drone.measure_fitness()
        fitness_sum += drone.fitness
    for drone in drones:
        drone.fitness = map(drone.fitness, 0, fitness_sum, 0, 1)
    crossing()
        
def pick_drone():
    global drones
    index = 0
    pick = random(1)
    while (pick > 0):
        pick = pick - drones[index].fitness
        index+=1    
    return drones[index-1]

def crossing():
    global max_move_dist
    global drones
    new_drones = list()
    for i in range (nr_of_drones):
        a = pick_drone()
        b = pick_drone()
        while (a==b):
            b = pick_drone()
        c = Entity()
        partinga = random(1)
        partingb = 1-partinga
        partinga = int(map(partinga, 0, 1, 0, a.steps_to_closest_position))
        partingb = int(map(partingb, 0, 1, 0, b.steps_to_closest_position))
        for m in range (partinga):
            c.moves.append(a.moves[m%len(a.moves)])
        for m in range (partingb, b.steps_to_closest_position):
            c.moves.append(b.moves[m%len(b.moves)])
        if (random(1)<mutation_probability and len(c.moves)>10):
            c.mutate()
        if(len(c.moves)<10):
            c.generate_moves(nr_of_moves, max_move_dist)
        new_drones.append(c)
    drones=new_drones
    for drone in drones:
        drone.pos = Position(startpos.x, startpos.y)
    global moves_made
    moves_made=0

def mouseClicked():
    goal.pos.x = mouseX
    goal.pos.y = mouseY
    print("Pozycja celu zmieniona na: x="+str(goal.pos.x)+" y="+str(goal.pos.y))
    global generation
    generation = 0

moves_made = 0
generation = 0
startpos = Position(width/2, height-50)
obstacles = [Obstacle(randint(50,width-200), randint(50,height-200), randint(40,200), randint(40,200)) for i in range(nr_of_obstacles)]
goalpos = get_random_position()
while (not check_obstacles(goalpos.x, goalpos.y) or get_distance(Position(startpos.x, startpos.y), goalpos)<300000):
    goalpos = get_random_position()
goal = Goal(goalpos)

drones = [Entity() for i in range (nr_of_drones)]
for drone in drones:
    drone.generate_moves(nr_of_moves, max_move_dist)

def draw():
    background (60)
    global moves_made
    for obstacle in obstacles:
        obstacle.show()
    goal.show()
    if (moves_made < nr_of_moves):
        moves_made+=1
        for drone in drones:
            drone.update_position()
            drone.show()
    else:
        prepare_drones()
        global generation
        print("Pokolenie nr: "+str(generation))
        generation+=1
        
        
        