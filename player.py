import pygame
GRID_SIZE = 50 

class Player:
    def __init__(self, speed,grid, dim=(25,25), pos = (1,1), color=(20,100,125) ):
        # not sure of what attributes to even give this
        self.speed = speed 
        
        self.dim = dim # height and width of the player

        self.pos = pos # starting position, this is in terms of the Grid Indices, not pixel values

        self.actualPos = (pos[0]*dim[0], pos[1]*dim[0]) # in terms of actual pixel values
        
        self.targetPos = self.actualPos # for initialisation

        self.color = color # RGB format

        # this is the rect for movement smoothing
        self.rect = pygame.Rect(self.actualPos, self.dim) # Pygame rect
        self.direction = (0,0)# player is stationary by default
       
        # To keep track of when the player is actually in the
        # state of moving to next grid, but not quite there yet
        self.isMoving = False;
        
        # To know which moves are illegal.
        self.grid = grid
        
        print(f"Created Player: {self.dim, self.pos}") 


    def set_direction(self, direction):
        match direction.upper():
            case "UP":
                self.direction = ( 0,-1 )
            case "DOWN":
                self.direction = ( 0, 1 )

            case "LEFT":
                self.direction = (-1, 0 )
            case "RIGHT":
                self.direction = ( 1, 0 )

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 
    
    def move(self):
        
        if self.isMoving == False:
            if self.direction == (0,0): # for the initial condition, theres def a better approach to handling the default
                return

            # THIS IS WHERE I'M PREVENTING THE PLAYER FROM MOVING INTO A WALL!
            # check if the current pos + direction == wall

            # In terms of the grid, first value, refers to the Y axis,
            # second value for the X axis, this is opposite to the convention followed
            # in pygame (which is absurd in it's own right)

            upcomingY = self.pos[0] + self.direction[0]
            upcomingX = self.pos[1] + self.direction[1]
            
            if self.grid[upcomingX][upcomingY] == 1:
                self.direction = (0,0)
                return


            self.targetPos = (self.rect.x + (GRID_SIZE * self.direction[0]), self.rect.y + (GRID_SIZE * self.direction[1]))
            self.isMoving = True
            
            # go to next frame.
            return
        else:

            #if the player is moving, handle the offset and stop/update condition
            # Applying linear interpolation for the smooth movement.
            
            deltaX = self.targetPos[0] - self.rect.x
            deltaY = self.targetPos[1] - self.rect.y

            distance = ((deltaX**2 + deltaY**2))**0.5
            moveDistance = min(distance, self.speed)
            print("Distance, moveDistance", distance, moveDistance)
           
            xMove = deltaX / distance * moveDistance
            yMove = deltaY / distance * moveDistance
            
            # if the player reaches close enough to the target, just snap its position to the target
            # set moving to false, so a new target can be calculated
            if distance <= self.speed:
                self.rect.topleft = self.targetPos
                self.pos = (self.targetPos[0] // GRID_SIZE, self.targetPos[1]//GRID_SIZE)

                
                
                self.isMoving = False
                return
            
            self.rect.move_ip(xMove, yMove)



    # this method wont be needed in terms of collisions with the walls,
    # only for possibly detecting when the player gets a point? or gets killed?

    def collidelistall(self, *args, **kwargs):
        return self.rect.collidelistall(*args, **kwargs)
   
    def __repr__(self):
        # Clears the console and prints some debug information
        print("\033[2J\033[H", end="")
        return f"""

        -------------------------------------
            Grid Size: {GRID_SIZE},
            Direction : {self.direction},
            Raw Position: {self.rect.topleft},
            Grid Position: {self.pos},
            Target Position: {self.targetPos},
            State: {self.isMoving}
            Dist: {self.targetPos[0] - self.rect.x, self.targetPos[1] - self.rect.y}
        -------------------------------------
        
        """










