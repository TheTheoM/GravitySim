import sys, pygame, random, turtle, time, array, math, itertools


def FillBlack_And_ExitLogic() -> None:
    """Fills the Screen with black to cover up old drawn items. ALso Allows Alt-F4 to work."""
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

def Add_Body_Object(mass: float, radius: int, position: array, color: tuple, velocity: array, InitialVelocity: array, Body_Dict: dict, fixed: bool, name: str) -> dict: 
    """Creates Class Body object and appends it to Body_Dict"""
    temp = Body(name = name,mass =  mass, radius = radius, position = [position[0], position[1]], color = color,  velocity = [velocity[0],velocity[1]], InitialVelocity = [velocity[0],velocity[1]], fixed=fixed)
    Body_Dict[name] = temp
    return Body_Dict


def Iterator(Sun, Body_Dict: dict, mode: int) -> dict:
    """" Mode 1: Any collisions delete both body. Mode 2. Collisions only happen to the Sun and the colliding body is deleted. Mode 3. The Sun and the Moon cannot be deleted. """
    match mode:
        case 1:
            for Key_Array in (itertools.permutations(Body_Dict, 2)):
                    if (Body_Dict[Key_Array[0]].GMMR(Body_Dict[Key_Array[0]], Body_Dict[Key_Array[1]])):
                        print(f"Deleted: {Body_Dict[Key_Array[0]].name, Body_Dict[Key_Array[1]].name}")
                        del Body_Dict[Key_Array[0]], Body_Dict[Key_Array[1]]
                        break                    
        case 2:
            Planet_Dict = Body_Dict.copy()
            del Planet_Dict[Sun.name]
            for Body in Planet_Dict.values():
                Local_Flag = True
                if (Sun.GMMR(Sun, Body)):
                    if Local_Flag:
                        Key = (list(Body_Dict.keys())[list(Body_Dict.values()).index(Body)])
                        print(f"Deleted: {Key} Came into Contact with: {Sun.name}")
                        del Planet_Dict[Key], Body_Dict[Key]
                        Local_Flag = False
                        break
                if (Body.GMMR(Body, Sun)):
                    if Local_Flag:
                        Key = (list(Body_Dict.keys())[list(Body_Dict.values()).index(Body)])
                        print(f"Deleted: {Key} Came into Contact with: {Sun.name}")
                        del Planet_Dict[Key], Body_Dict[Key]
                        Local_Flag = False
                        break
                Local_Flag = True
        case 3:
            for Key_Array in (itertools.permutations(Body_Dict, 2)):
                if (Body_Dict[Key_Array[0]].GMMR(Body_Dict[Key_Array[0]], Body_Dict[Key_Array[1]])):
                    print(f"Deleted: {Body_Dict[Key_Array[0]].name, Body_Dict[Key_Array[1]].name}")
                    if True: #Toggles Making the Sun and Moon immortal.
                        if Body_Dict[Key_Array[0]].name == "Sun":
                            del Body_Dict[Key_Array[1]]
                            break
                        if Body_Dict[Key_Array[1]].name == "Sun":
                            del Body_Dict[Key_Array[0]]
                            break
                        if Body_Dict[Key_Array[0]].name == "Moon":
                            del Body_Dict[Key_Array[1]]
                            break
                        if Body_Dict[Key_Array[1]].name == "Moon":
                            del Body_Dict[Key_Array[0]]
                            break

                    del Body_Dict[Key_Array[0]], Body_Dict[Key_Array[1]]
                    break                    


    return Body_Dict
                
def Checker(spacer, Position, Array, LenArray) -> array:
    if len(Array) == 0:
        Array.append(Position)
    else:
        if (abs(Position[0] - Array[-1][0]) > spacer) or (abs(Position[0] - Array[-1][1]) > spacer):
            Array.append(Position)
    if len(Array) > LenArray:
        Array.pop(0)
    return (Array)


class Body(turtle.Turtle):
    def __init__(self, mass: float, radius: int, position: array, color: tuple, velocity: array, InitialVelocity: array, fixed: bool, name: str) -> None:
        self.mass = mass
        self.radius = radius
        self.position = position
        self.color = color
        self.velocity = velocity
        self.object = None
        self.Draw_Body()
        self.fixed = fixed
        self.name = name
        self.PositionArray = []
        self.InitialVelocity = InitialVelocity
        self.InitialPosition = position


    def Logger(self) -> None:
        print(f"name: {self.name} Mass {self.mass}, Position {self.position}, Velocity {self.velocity}")

    def Draw_Body(self) -> None:
        """Draws the Object in Turtle based of class vars."""
        self.object = pygame.draw.circle(surface=screen, radius=self.radius, color=(self.color), center = (self.position))

    def MoveBy(self, x, y) -> None:
        """Moves the object by x,y on Turtle Canvas. Adds x,y to objects existing position."""
        self.position[0], self.position[1] = (self.position[0] + x), (self.position[1] + y)
        self.object.move((x), (y))

    def MoveTo(self, x, y) -> None:
        """Moves the object to the x,y."""
        if (not self.fixed):
            self.object.move((x), (y))

    def UpdateMotion(self) -> None:
        """Animates Bodies"""
        spacer = 0.0000
        if (not self.fixed):
            self.MoveBy(self.velocity[0], self.velocity[1])



    def GMMR(self, Body_one, Body_two) -> bool:
        """Calculates the velocity due to Gravitional Attraction. Returns True if there is a collisison, else false."""
        x1, y1 = Body_one.position
        x2, y2 = Body_two.position
        M1, M2 = Body_one.mass, Body_two.mass
        x = x2 - x1
        y = y2 - y1
        c = 1
        radius = math.sqrt(x**2 + y**2)
            
        if (radius <= Body_one.radius) or (radius <= Body_two.radius):
            return True

        Force = (M1 * M2) / (radius)**2
        angle = math.atan2(y, x)  
        y_a = (math.sin(angle) * Force * c) / M1
        x_a = (math.cos(angle) * Force * c) / M1
        self.velocity[0], self.velocity[1] = self.velocity[0] + x_a, self.velocity[1] + y_a

        return False


def RenderLoopBasic(UpdatesPerSec) -> None:
    global Body_Dict
    Body_Dict = {}
    global size
    size = 1920, 1000
    pygame.init()
    global screen
    screen = pygame.display.set_mode(size)
    screeen = pygame.display.set_caption('Gravity Simulator')

    last_second = 0
    interval = 1 / UpdatesPerSec
    n = 1
    ### Adding Objects
    Body_Dict = Add_Body_Object(mass = 10000,
                            radius = 100,
                            position = [1200, 540],
                            color = (255,255,0),
                            velocity = [0,0],
                            InitialVelocity = [0,0],
                            Body_Dict = Body_Dict,
                            fixed = True,
                            name = "Sun") 


    Body_Dict = Add_Body_Object(mass = 2000,
                                    radius = 40,
                                    position = [800, 150],
                                    color = (255,255,255),
                                    velocity = [4,0],
                                    InitialVelocity = [6,0],
                                    Body_Dict = Body_Dict,
                                    fixed = False,
                                    name = "Moon") 


    Body_Dict = Add_Body_Object(mass = 10,
                                    radius = 10,
                                    position = [Body_Dict['Moon'].position[0], Body_Dict['Moon'].position[0] - 40],
                                    color = (255,255,255),
                                    velocity = [-2,0],
                                    InitialVelocity = [9,0],
                                    Body_Dict = Body_Dict,
                                    fixed = False,
                                    name = "Moonlet") 

    for i in range(10):
        Body_Dict = Add_Body_Object(mass = 10,
                                            radius = 10,
                                            position = [1200, 850 + 50*i],
                                            color = (255 * i/10 ,255 - 255 * i/10,0),
                                            velocity = [(6-0.3*i),0],
                                            InitialVelocity = [6,0],
                                            Body_Dict = Body_Dict,
                                            fixed = False,
                                            name = f"{i}") 
    while True:
        if (time.time() > last_second + interval):
            n += 1
            last_second = time.time()
            FillBlack_And_ExitLogic()

            for body in Body_Dict.values():
                body.Draw_Body()
                body.UpdateMotion()

            if True: # Fun stuff random stuff
                if n % 50 == 0:
                    Body_Dict = Add_Body_Object(mass = 10,
                                                radius = 10,
                                                position = [random.randint(0, size[0]),random.randint(0, size[1])],
                                                color = (255 ,0,0),
                                                velocity = [random.randint(-6, 6), random.randint(-6, 6)],
                                                InitialVelocity = [0,0],
                                                Body_Dict = Body_Dict,
                                                fixed = False,
                                                name = f"{n}") 
                    if "Moonlet" not in Body_Dict.keys():
                        Body_Dict = Add_Body_Object(mass = 10,
                                        radius = 10,
                                        position = [Body_Dict['Moon'].position[0], Body_Dict['Moon'].position[1] - 80],
                                        color = (255,255,255),
                                        velocity = [random.randint(-8, 8),0],
                                        InitialVelocity = [9,0],
                                        Body_Dict = Body_Dict,
                                        fixed = False,
                                        name = "Moonlet") 

                if n % 300 == 0 and "Graveball" not in Body_Dict.keys():
                    count = 20
                    for i in range(count):
                        Body_Dict = Add_Body_Object(mass = 0.001,
                                                        radius=10,
                                                        position=[300, (1000 * i/count)],
                                                        color= (200, 50, 0),
                                                        velocity=[0, 0],
                                                        InitialVelocity=[0, 0],
                                                        Body_Dict=Body_Dict,
                                                        fixed=False,
                                                        name=f"GravBall_{i}")

                
            Body_Dict = Iterator(Body_Dict["Sun"], Body_Dict, 3)
        pygame.display.update()

if __name__ == "__main__":
    RenderLoopBasic(100)


