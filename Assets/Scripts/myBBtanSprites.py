import pygame, math, random

image_path = "../Images/"
music_path = "../Music/"

class Powerup(pygame.sprite.Sprite):
    """This class simulates a sprite which increases the number of balls by 1."""

    def __init__(self, left, top):
	"""This method sets the image and position of the powerup sprite."""
	pygame.sprite.Sprite.__init__(self)

	# Set image
	self.image = pygame.image.load(image_path+"powerup.png")
	self.image = self.image.convert()

	# Set position
	self.rect = self.image.get_rect()
	self.rect.centerx = 50 / 2 + left
	self.rect.centery = 50 / 2 + top

	# Set attributes
	self.__left = left
	self.__top = top
	self.__kill_status = False

    def shift_down(self):
	"""This method shifts the powerup sprite 50 pixels downwards."""

	self.rect.centery += 50
	self.__top += 50


    def set_killstatus(self, boolean):
	"""This method sets the boolean value of the self.__kill_status
	   attribute."""

	self.__kill_status = boolean

    def get_killstatus(self):
	"""This method returns the boolean value referenced by the
	   self.__kill_status attribute."""

	return self.__kill_status

    def get_left(self):
	"""This method returns the value referenced by the self.__left
	   attribute."""

	return self.__left

    def get_top(self):
	"""This method returns the value referenced by the self.__top
	   attribute."""

	return self.__top

    def get_type(self):
	"""This method returns the type of buff sprite, in this case its a
	   powerup buff sprite."""

	return "power_up"

class Random(Powerup):
    """This class simulates a random direction sprite and inherits attributes
       and methods from the powerup class."""

    def __init__(self, left, top):
	"""This method sets the image and position of the random direction
	   sprite which changes the direction of the ball in 1 of 3
	   directions."""

	# Initializes parent class attributes and methods
	Powerup.__init__(self, left, top)

	# Set image
	self.image = pygame.image.load(image_path+"random2.png")
	self.image = self.image.convert()

	# Set position
	self.rect = self.image.get_rect()
	self.rect.centerx = 50 / 2 + left
	self.rect.centery = 50 / 2 + top

	# Set attributes
	self.__kill_status = False
	self.__change_image = False

    def get_type(self):
	"""This method returns the type of buff sprite, in this case it's a
	   random direction sprite."""

	return "random"

    def update(self):
	"""This method updates the image of the random direction sprite so that
	   it cannot be used when it is first created (in the top row)."""

	if self.get_top() != 50 and self.__change_image == False:
	    self.image = pygame.image.load(image_path+"random.png")
	    self.image = self.image.convert()


class Laser(Powerup):
    """This class simulates a laser sprite and inherits attributes and
       methods from the powerup class."""

    def __init__(self, left, top, buff):
	"""This method sets the image and position of the laser sprite."""

	# Initializes parent class attributes and methods
	Powerup.__init__(self, left, top)

	# Set image
	if buff == "up":
	    self.image = pygame.image.load(image_path+"laser_up.png")
	else:
	    self.image = pygame.image.load(image_path+"laser_side.png")
	self.image = self.image.convert()

	# Set position
	self.rect = self.image.get_rect()
	self.rect.centerx = 50 / 2 + left
	self.rect.centery = 50 / 2 + top

	# Set attributes
	self.__type = buff

    def get_type(self):
	"""This method returns the type of buff sprite, through the value
	   referenced by the self.__type attribute."""

	return self.__type

class Beam(pygame.sprite.Sprite):
    """This class simulates a beam that will shoot when the ball collides with a
       laser sprite."""

    def __init__(self, endzone, laser):
	"""This method initializes the image list, laserup, endzone and shoot
	   attributes."""

	pygame.sprite.Sprite.__init__(self)

	self.__time = 0
	self.__image_list = []
	self.__laser = laser
	self.__endzone = endzone

	for num in range(1,4):
	    if self.__laser.get_type() == "up":
		self.__image_list.append(pygame.image.load(image_path+"Beam" + str(num) \
		                                           + ".png").convert())
	    else:
		self.__image_list.append(pygame.image.load(image_path+"Beam" + \
		                    str(num + 3) + ".png").convert())

    def update(self):
	"""This method iterates through the image list creating a laser beam
	   animation and setting its position using the rect attribute of the
	   laserup and endzone sprites."""

	# After iterating through the image list, kill the laser beam
	if self.__time > 6:
	    self.kill()

	# Every 3 frames load an image from the image list and set its position
	elif self.__time % 3 == 0:
	    self.image = self.__image_list[self.__time / 3]
	    self.rect = self.image.get_rect()
	    if self.__laser.get_type() == "up":
		self.rect.centerx = self.__laser.rect.centerx
		self.rect.bottom = self.__endzone.rect.top - 5
	    elif self.__laser.get_type() == "side":
		self.rect.centery = self.__laser.rect.centery
		self.rect.left = 5

	self.__time += 1

class Endzone(pygame.sprite.Sprite):
    """This class simulates an endzone that prevents the ball from moving past
       a certain line on the screen and ends the game if a block hits the
       endzone."""

    def __init__(self, screen):
	"""This method sets the image and position of the sprite."""

	pygame.sprite.Sprite.__init__(self)

	# Set image
	self.image = pygame.Surface((screen.get_width(), 1))
	self.image = self.image.convert()
	self.image.fill((255, 255, 255))

	# Set position
	self.rect = self.image.get_rect()
	self.rect.bottom = screen.get_height() - 60
	self.rect.left = 0

class Player(pygame.sprite.Sprite):
    """This class simulates a the player sprite which determines the location
       of the balls."""

    def __init__(self, screen, endzone):
	"""This method sets the image and position of the sprite and a creates
	   self.__screen and self.__shooting attributes."""

	pygame.sprite.Sprite.__init__(self)

	# Attributes
	self.__screen = screen
	self.__shooting = False

	# Set image
	self.set_image()

	# Set position
	self.rect = self.image.get_rect()
	self.rect.centerx = screen.get_width() / 2
	self.rect.centery = endzone.rect.centery - 5

    def set_position(self, right):
	"""This method shifts the play 10 pixels left of the screen if the
	   player goes off the screen to the right."""

	# Player will not go off the screen to the left completely because the
	# player's position is dictated by the landing position of the first
	# ball
	self.rect.left = right + 5
	if self.rect.left > self.__screen.get_width():
	    self.rect.left = self.__screen.get_width() - 20

    def set_shooting(self, boolean):
	"""This method sets the boolean value for the self.__shooting
	   attribute."""

	self.__shooting = boolean

    def set_image(self):
	"""This image sets the image for the player sprite based on the
	   self.__shooting attribute."""

	if self.__shooting:
	    self.image = pygame.image.load(image_path+"monkey2.png")
	else:
	    self.image = pygame.image.load(image_path+"monkey.png")

	self.image = self.image.convert()
	self.image.set_colorkey((0,0,0))

    def update(self):
	"""This method changes the image on the monkey when it stops or starts
	   shooting."""

	self.set_image()

class Block(pygame.sprite.Sprite):
    """This class simulates a block sprite that the player has to destroy to
       accumulate points."""

    def __init__(self, left, top, health):
	"""This method initializes the font, left, top, health and changey
	   attributes and sets the image of the sprite."""

	pygame.sprite.Sprite.__init__(self)

	# Set attributes
	self.__font = pygame.font.SysFont("Courier", 18, True)
	self.__left = left
	self.__top = top
	self.__health = health
	self.__changey = 0

	# Set image and position
	self.set_image()
	self.update_health()

    def lose_health(self):
	"""This method decreses the value of the health attribute by 1."""

	self.__health -= 1

    def set_image(self):
	"""This method sets the image and color of the font."""

	if self.__health > 19:
	    self.__image = image_path+"Block_yellow.png"
	    self.__color = (255,227,103)
	elif self.__health > 9:
	    self.__image = image_path+"Block_blue.png"
	    self.__color = (95,11, 208)
	else:
	    self.__image = image_path+"Block_red.png"
	    self.__color = (231, 32, 101)

    def shift_down(self):
	"""This method shifts the block down 50 pixels and adds 50 to the
	   self.__changey attribute."""

	self.rect.bottom += 50
	self.__changey += 50

    def get_midpoints(self):
	"""This method returns the 4 side midpoints of the block rect."""

	# Returns the 4 side midpoints of the rect for side collision detection
	return self.rect.midtop, self.rect.midleft, self.rect.midbottom, \
	       self.rect.midright

    def get_left(self):
	"""This method returns the value referenced by the self.__left
	   attribute."""

	return self.__left

    def get_top(self):
	"""This method returns the value referenced by the self.__top
	   attribute."""

	return self.rect.top

    def update_health(self):
	"""This method sets the image and position of the block sprite and the
	   health of the block in the middle."""

	# Positions health text on the block based on number of digits
	if self.__health > 99:
	    self.__message_pos = (10, 15)
	elif self.__health > 9:
	    self.__message_pos = (15,15)
	else:
	    self.__message_pos = (20, 15)

	# Set image
	self.image = pygame.image.load(self.__image)
	self.image = self.image.convert()

	# Set position
	self.rect = self.image.get_rect()
	self.rect.left = self.__left
	self.rect.top = self.__top + self.__changey

	# Set health in the middle of the block
	message = self.__font.render(str(self.__health), 1, self.__color)
	self.image.blit(message, self.__message_pos)

    def update(self):
	"""This method checks if the block health has reached 0 or less and
	   kills it if condition is True."""

	if self.__health <= 0:
	    self.kill()

class Ball(pygame.sprite.Sprite):
    """This class simulates a ball with side collision detection."""

    def __init__(self, screen, player, endzone, ball_list):
	"""This method initializes the speed, screen, endzone, ball_list,
	   collide, dx and dy attributes, and sets the image and position of the
	   sprite."""

    	pygame.sprite.Sprite.__init__(self)

	# Set image
    	self.image = pygame.image.load(image_path+"ball3.png")
    	self.image = self.image.convert()
	self.image.set_colorkey((0,0,0))

	# Set position
    	self.rect = self.image.get_rect()
	self.rect.right = player.rect.left - 5
	self.rect.bottom = endzone.rect.top - 5

	# Attributes
	self.__time = 0
	self.__speed = 10
	self.__screen = screen
	self.__player = player
	self.__endzone = endzone
	self.__ball_list = ball_list
	self.__laser_collide = True
	self.__random_collide = True
	self.__dx = 0
	self.__dy = 0

    def add_time(self):
	"""This method adds 1 to the value of the self.__time attribute."""

	self.__time += 1

    def reset_time(self):
	"""This method resets the value of the self.__time attribute to 0."""
	self.__time = 0

    def shift_up(self):
	"""This method prevents the ball from moving and shifts it 5 pixels
	   above the endzone."""

	# Stops moving
	self.__dx = 0
	self.__dy = 0

	self.rect.bottom = self.__endzone.rect.top - 5

    def set_position(self):
	"""This method sets the position of the ball 5 pixels to the left of the
	   player and calls the shift_up() method."""

	self.rect.right = self.__player.rect.left - 5
	self.shift_up()

    def set_centerxy(self, random):
	"""This method sets the centerx and centery values of the ball to the
	   centerx and centery values of the random direction sprite."""

	if random.get_top() != 50:
	    self.rect.centerx = random.rect.centerx
	    self.rect.centery = random.rect.centery

    def set_lasercollide(self, boolean):
	"""This method sets the boolean value of the self.__laser_collide
	   attribute."""

	self.__laser_collide = boolean

    def set_randomcollide(self, boolean):
	"""This method sets the boolean value of the self.__random_collide
	   attribute."""

	self.__random_collide = boolean

    def shoot(self, mouse_pos):
	"""Sets the direction of the ball towards the mouse."""

	# Algorithm for determining ball direction and speed
	distance = self.calc_distance(mouse_pos)
	self.__dx = (self.__diffx / distance) * self.__speed
	self.__dy = (self.__diffy / distance) * self.__speed

    def find_player(self):
	"""Stop moving vertically and start moving horizontally towards
	   player."""

	# Stops moving upwards and move towards the location of the player based
	# on self.__speed attribute
	self.__dy = 0
	self.rect.bottom = self.__endzone.rect.top
	if self.__player.rect.x > self.rect.x:
	    self.__dx = self.__speed
	elif self.__player.rect.x < self.rect.x:
	    self.__dx = -self.__speed

    def check_collision(self, collide_list):
	"""This method takes collide_list as a parameter, calculates the
	   distance from each side midpoint of the block in collide_list to the
	   centerx and centery value of the ball, then determine the change in
	   direction based on the shortest distance."""

	# ALGORITHM FOR SIDE COLLISION DETECTION
	for block in collide_list:
	    midpoints_dict = {}
	    distance_list = []

	    # Get the 4 side midpoints of each block
	    midpoints_list = block.get_midpoints()

	    # Calculate distance of centerx/centery of the ball to each side
	    # midpoint of the block
	    # Append each distance value to the list for sorting and dict for
	    # direct access to the specific midpoint
	    for index in range(len(midpoints_list)):
		self.calc_distance(midpoints_list[index])
		distance_list.append(self.__distance)
		midpoints_dict[index] = self.__distance

	    # Sort the distance list and get the lowest distance value
	    # Use the dictionary to get the midpoint location and use it to
	    # determine direction change
	    distance_list.sort()
	    for key in midpoints_dict:
		if midpoints_dict[key] == distance_list[0]:
		    self.set_direction(key, midpoints_list)
		    break

    def set_direction(self, index, midpoints_list):
	"""This method sets the dx direction of the ball based the closest side
	   midpoint for the collided block and shifts in the opposite direction
	   based on the self.__speed attribute."""

	# Index 0 == top midpoint
	if index == 0:
	    self.__changex = False
	    self.rect.bottom = midpoints_list[index][1] - 1

	# Index 2 == bottom midpoint
	elif index == 2:
	    self.__changex = False
	    self.rect.top = midpoints_list[index][1] + 1

	# Index 1 == left midpoint
	elif index == 1:
	    self.__changex = True
	    self.rect.right = midpoints_list[index][0] - 1

	# Index 3 == right midpoint
	elif index == 3:
	    self.__changex = True
	    self.rect.left = midpoints_list[index][0] + 1

    def change_direction(self):
	"""This method changes the direction of dx based on the value of the
	   attribute self.__changex."""

	if self.__changex:
	    self.__dx = -self.__dx
	elif self.__changex == False:
	    self.__dy = -self.__dy

    def switch_direction(self, num):
	"""This method changes the direction of self.__dx and self.__dy based on
	   the random num that is passed as a parameter."""

	# Ball moves towards top left corner
	if num == 0:
	    self.__dx = -6
	    self.__dy = -7

	# Ball moves straight up
	elif num == 1:
	    self.__dx = 0
	    self.__dy = -10

	# Ball moves towards top right corner
	elif num == 2:
	    self.__dx = 6
	    self.__dy = -7

    def calc_distance(self, xy):
	"""This method calculates the distance between the xy parameter and
	   center xy values of the Ball."""

	# Used for calculating direction for the ball movement and distance for
	# side collision detection
	self.__diffx = xy[0] - self.rect.centerx
	self.__diffy = xy[1] - self.rect.centery
	self.__distance = math.hypot(self.__diffx, self.__diffy)

	return self.__distance

    def get_time(self):
	"""This method returns the value referenced by the self.__time
	   attribute."""

	return self.__time

    def get_right(self):
	"""This method returns the value referenced by the self.rect.right
	   attribute."""

	return self.rect.right

    def get_dx(self):
	"""This method returns the value referenced by the self.__dx
	   attribute."""

	return self.__dx

    def get_dy(self):
	"""This method returns the value referenced by the self.__dy
	   attribute."""

	return self.__dy

    def get_randomcollide(self):
	"""This method returns the value referenced by the self.__random_collide
	   attribute."""

	return self.__random_collide

    def get_lasercollide(self):
	"""This method returns the value referenced by the self.__laser_collide
	   attribute."""

	return self.__laser_collide

    def update(self):
	"""This method keeps the ball moving based on the self.__dx and
	   self.__dy attributes and returns to the position beside the player
	   when ball hits the endzone."""

	# If the ball hits the player while moving horizontally, move it beside
	# the player and above the endzone and stop moving
	if self.rect.colliderect(self.__player.rect) and self.__dy == 0 and \
	   self.__dx != 0:
	    self.set_position()

	# If the ball hits the endzone, move it towards the player
	if self.rect.colliderect(self.__endzone.rect):
	    self.find_player()

	# If the ball is approaching the left or right side of the screen
    	# without touching the edges of the screen, the cube moves at a constant
    	# rate based on self.__dx, if the cube hits the left or right edges, the
    	# direction is reversed
	if (self.rect.left > 0 and self.__dx < 0) or \
	   (self.rect.right < self.__screen.get_width() and self.__dx > 0):
	    self.rect.centerx += self.__dx
    	else:
	    self.__dx = -self.__dx

	# If the ball is approaching the top or bottom side of the screen
    	# without touching the edges of the screen, the cube moves at a constant
    	# rate based on self.__dy, if the cube hits the top or bottom edges, the
    	# direction is reversed
	if (self.rect.top > 50 and self.__dy < 0) or \
	   (self.rect.bottom < self.__screen.get_height() and self.__dy > 0):
	    self.rect.centery += self.__dy
    	else:
	    self.__dy = -self.__dy

class Scoreboard(pygame.sprite.Sprite):
    """This class simulates a scoreboard sprite that tracks the current score,
       the previous highscore, and the new balls on the screen."""

    def __init__(self, screen):
	"""This method initializes the font, score, newball_list and screen
	   attributes and starts the score at 1."""

	pygame.sprite.Sprite.__init__(self)

	# Set attributes
	self.__font = pygame.font.SysFont("Courier", 25, True)
	self.__score = 1
	self.__newball_list = []
	self.__screen = screen
	self.__highscore = 1

	self.update_score()

    def add_score(self):
	"""This method increases the value of the self.__score attribute by
	   1."""

	self.__score += 1

    def add_newball(self, ball):
	"""This method appends the ball parameter to the self.__newball_list
	   attribute."""

	self.__newball_list.append(ball)

    def reset_newball_list(self):
	"""This method resets the value of the self.__newball_list to an empty
	   list."""

	self.__newball_list = []

    def set_highscore(self):
	"""This method checks if the user has achieved a new highscore and
	   writes it in the highscore.txt file if condition is True."""

	# Add the new highscore if the current score is greater than the
	# previous highscore
	highscore = self.get_highscore()
	if self.__score > highscore:
	    infile = open("highscore.txt", 'w')
	    infile.write(str(self.__score))
	    infile.close()

    def get_highscore(self):
	"""This method returns the integer value stored in the highscore.txt
	   file."""

	# Get the high_score from the highscore.txt file, if file doesnt exist,
	# set the self.__highscore attribute to 1
	try:
	    infile = open("highscore.txt", 'r')
	    self.__highscore = int(infile.readline())
	    infile.close()

	except IOError:
	    self.__highscore = 1

	return self.__highscore

    def get_score(self):
	"""This method returns the value referenced by the self.__score
	   attribute."""

	return self.__score

    def get_newball_list(self):
	"""This method returns the value referenced by the self.__newball_list
	   attribute."""

	return self.__newball_list

    def update_score(self):
	"""This method updates the score of the player and sets the image and
	   position of the sprite."""

	# When player's score is higher than the previous highscore, keep
	# changing the highscore based on the current score
	if self.__score > self.__highscore:
	    self.__highscore = self.__score

	# Display current score and highscore at the top of the screen
	message = "%d       Top: %d" % (self.__score, self.__highscore)
	self.image = self.__font.render(message, 1, (255, 255, 255))
	self.rect = self.image.get_rect()
	self.rect.center = (self.__screen.get_width() - 145, 25)


class Counter(pygame.sprite.Sprite):
    """This class simulates a counter sprite that will keep track of the number
       of balls that is beside the player."""

    def __init__(self, player, endzone, ball_list, ballmove_list):
	"""This method initializes the font, player, endzone, ball_list and
	   ballmove_list attributes."""

	pygame.sprite.Sprite.__init__(self)

	# Set attributes
	self.__font = pygame.font.SysFont("Arial", 15, True)
	self.__player = player
	self.__endzone = endzone
	self.__ball_list = ball_list
	self.__ballmove_list = ballmove_list

    def update(self):
	"""This method updates the number of balls that the player has and
	   displays it beside the player sprite."""

	# Set number of balls beside the player
	count = len(self.__ball_list) - len(self.__ballmove_list)
	message = "x%d" % (count)

	# Set image and position
	self.image = self.__font.render(message, 1 , (255, 255, 255))
	self.rect = self.image.get_rect()
	self.rect.bottom = self.__endzone.rect.top - 30
	self.rect.right = self.__player.rect.left - 5
