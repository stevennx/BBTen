"""Author: Steven Xu

    Date: May 20th, 2016

    Description: This program is a single player game based off the popular game
                 BBtan. The player uses the mouse to shoot balls to destroy
		 blocks to accumulate points for a highscore. This game also
		 features buffs and several sprites that will help the user
		 in destroying the blocks.
"""

# Import and initialize
import pygame, myBBtanSprites, random, os
pygame.init()
pygame.mixer.init()

# Create screen and caption
screen = pygame.display.set_mode((500,700))
pygame.display.set_caption("BBTan")

# Image Path
image_path = "../Images/"
music_path = "../Music/"

def create_row(blockGroup, buffGroup, allSprites, scoreboard, top, background):
    """This function creates sprites that will appear at the top row of the game
       screen."""

    condition = True
    y = top

    # Increases the health of blocks to make the game harder as it progresses
    if scoreboard.get_score() < 10:
	start = 1
    elif scoreboard.get_score() > 9 and scoreboard.get_score() < 20:
	start = 5
    elif scoreboard.get_score() > 19:
	start = (scoreboard.get_score() / 10 - 1) * 10

    # Creates sprites in the top row
    # Make sure that every row contains more than 4 blocks
    while condition:

	# Set 2 super blocks every 5 levels
	if scoreboard.get_score() % 5 == 0:
	    super_block = 2
	else:
	    super_block = 0

	powerup_spawn = True
	laser_spawn = True
	randomizer_spawn = True
	block_list = []
	buff_list = []
	x = 0

	for i in range(10):
	    num = random.randrange(0, 6)
	    health = random.randrange(start, scoreboard.get_score() + 1)

	    # Spawns a block
	    if num > 3:

		# Super blocks have twice the health of the current score
		if super_block != 0:
		    block = myBBtanSprites.Block(x, y, scoreboard.get_score() * 2)
		    super_block -= 1
		else:
		    block = myBBtanSprites.Block(x, y, health)
		block_list.append(block)

	    # Spawns a random powerup sprite that adds a ball to the user
	    elif num == 0 and powerup_spawn:
		power_up = myBBtanSprites.Powerup(x, y)
		buff_list.append(power_up)
		powerup_spawn = False

	    # Spawns a laser sprite that shoots a beam when it gets hit
	    elif scoreboard.get_score() % 2 == 0 and laser_spawn and \
		 (num == 2 or num == 3):
		if num == 2:
		    laser = myBBtanSprites.Laser(x, y, "up")
		elif num == 3:
		    laser = myBBtanSprites.Laser(x, y, "side")
		buff_list.append(laser)
		laser_spawn = False

	    # Spawns a random direction sprite that randomly changes the
	    # direction of the ball from one of 3 directions
	    elif randomizer_spawn and scoreboard.get_score() % 3 == 0:
		randomizer_spawn = False
		randomizer = myBBtanSprites.Random(x, y)
		buff_list.append(randomizer)

	    x += 50

	if len(block_list) > 4:
	    condition = False

    # Add all sprites into allSprites
    blockGroup.add(block_list)
    buffGroup.add(buff_list)
    allSprites.add(buffGroup, blockGroup)


def create_ball(screen, player, endzone, ball_list, allSprites, scoreboard):
    """This function creates a new ball."""

    ball = myBBtanSprites.Ball(screen, player, endzone, ball_list)
    ball_list.append(ball)
    allSprites.add(ball_list)
    scoreboard.add_newball(ball)

def game():
    """This function displays and runs the game BBtan, a single-player game that
       requires the user to shoot balls to break as many blocks as possible to
       accumulate a new highscore."""

    # Creates and blits a background Surface on the screen
    background = pygame.image.load(image_path+"background.png")
    background = background.convert()
    screen.blit(background, (0,0))

    # Sound effects and background music
    hit = pygame.mixer.Sound(music_path+"hit.wav")
    hit.set_volume(0.8)
    hit2 = pygame.mixer.Sound(music_path+"hit2.wav")
    hit2.set_volume(1.0)
    laser = pygame.mixer.Sound(music_path+"laser.wav")
    laser.set_volume(0.8)Could not get lock /var/lib/apt/lists/lock - open (11: Resource temporarily unavailable)

    powerup = pygame.mixer.Sound(music_path+"powerup.wav")
    powerup.set_volume(0.8)

    # Create player, scoreboard and endzone sprites
    endzone = myBBtanSprites.Endzone(screen)
    scoreboard = myBBtanSprites.Scoreboard(screen)
    blockGroup = pygame.sprite.Group()
    buffGroup = pygame.sprite.Group()
    ball_list = []
    ballmove_list = []
    player = myBBtanSprites.Player(screen, endzone)
    counter = myBBtanSprites.Counter(player, endzone, ball_list, ballmove_list)

    # Start off with 1 ball
    allSprites = pygame.sprite.OrderedUpdates(endzone, counter, player, \
                                              scoreboard)

    # Create first row and ball
    create_row(blockGroup, buffGroup, allSprites, scoreboard, 100, background)
    create_ball(screen, player, endzone, ball_list, allSprites, scoreboard)

    # Create counter to keep track of # of frames that have past, create ball
    # counter to keep track of the numbers of balls that have been shot and
    # create hit_endzone variable to determine if a ball has hit the endzone
    count = 0
    ball_count = 0
    condition = True
    hit_endzone = True
    clock = pygame.time.Clock()

    # Display highscore
    scoreboard.get_highscore()
    scoreboard.update_score()

    while condition:

	clock.tick(60)
	count += 1

	# Create mouse_pos1 variable to make sure that mouse cursor is above the
	# player sprite when shooting the ball
	mouse_pos1 = pygame.mouse.get_pos()

	# Event handling
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		scoreboard.set_highscore()
		return False

	    # SHOOTING FIRST BALL
	    # When user clicks mousebutton, if there are no balls moving, and
	    # the mousebutton is above the player sprite then
	    # Create 1 ball, reset counter to 0 and set hit_endzone to true
	    elif event.type == pygame.MOUSEBUTTONDOWN and ballmove_list == [] \
	         and mouse_pos1[1] < player.rect.top:
		mouse_pos = pygame.mouse.get_pos()
		ball_list[0].shoot(mouse_pos)
		ballmove_list.append(ball_list[0])
		player.set_shooting(True)
		ball_count += 1
		hit_endzone = True
		count = 0

	#CHECKING FOR BALL MOVEMENT
	#If any ball in the ballmove_list stops moving, remove it from the list
	if ballmove_list:
	    for ball in ballmove_list:
		if ball.get_dx() == 0 and ball.get_dy() == 0:
		    ballmove_list.remove(ball)

	# SHOOTS OTHER BALLS
	# Every  5 frames, shoot a new ball, until the counter is the same
	# number as the number of balls in the ball_list
	if count == 5 and (ball_count < len(ball_list)) and ball_count > 0:
	    if ball_list[ball_count] not in ballmove_list and \
	       ball_list[ball_count] not in scoreboard.get_newball_list():
		ball_list[ball_count].shoot(mouse_pos)
		ballmove_list.append(ball_list[ball_count])
	    count = 0
	    ball_count += 1

	# RESET BALL COUNTER
	# If the counter as reached the number of balls in the ball_list, reset
	# it to 0
	if ball_count == len(ball_list):
	    player.set_shooting(False)
	    ball_count = 0

	# MOVING PLAYER TO BALL LANDING POSITION
	# Determines the first ball that hit the endzone and sets the location
	# of the player next to the ball
	ball_collide = pygame.sprite.spritecollide(endzone, ball_list, False)
	if ball_collide and hit_endzone:
	    for ball in ball_collide:
		player.set_position(ball.get_right())
		ball.set_position()
		hit_endzone = False
		break

	    # Reposition new balls that have been created
	    for ball in ball_list:
		if ball in scoreboard.get_newball_list():
		    ball.set_position()

	# MOVING BLOCKS DOWN AND INCREASING LEVEL
	# If the last ball hits the endzone, shift all blocks down and creates
	# a new first row
	if len(ballmove_list) == 0 and hit_endzone == False:
	    hit_endzone = True
	    for block in blockGroup:
		block.shift_down()
	    for buff in buffGroup:
		buff.shift_down()
		if (buff.get_type() == "up" or buff.get_type() == "side" or \
		    buff.get_type() == "random") and buff.get_killstatus():
		    buff.kill()

	    scoreboard.add_score()
	    scoreboard.update_score()
	    create_row(blockGroup, buffGroup, allSprites, scoreboard, 50, background)
	    allSprites.add(buffGroup, blockGroup)
	    scoreboard.reset_newball_list()

	# SIDE COLLISION DETECTION
	# If a ball collides with a block, check the collision to determine the
	# change in direction
	for ball in ball_list:
	    if ball in ballmove_list:

		# COLLIDING WITH BLOCKS
		block_collide = pygame.sprite.spritecollide(ball, blockGroup, False)
		if block_collide:
		    ball.check_collision(block_collide)
		    ball.change_direction()
		    for block in block_collide:
			block.lose_health()
			block.update_health()
			hit.play()

		    # When ball hits a block reset the timer to acknowledge that
		    # the ball isn't stuck
		    ball.reset_time()

		# Create ball timer to prevent ball from getting stuck going
		# side by side, when the count hits above 800, it will
		# acknowledge that the ball is currently stuck and will be
		# placed to its starting position
		elif ball.get_time() > 800:
		    ball.set_position()
		    ball.reset_time()
		elif int(ball.get_dy()) == 0:
		    ball.add_time()
		else:
		    ball.reset_time()


		# COLLIDING WITH BUFFS
		# If ball collides with a buff sprite, kill the buff sprite and
		# apply the buff
		buff_collide = pygame.sprite.spritecollide(ball, buffGroup, False)
		if buff_collide:
		    for buff in buff_collide:

			# If the ball hits a powerup sprite, a new ball is created
			# and the powerup sprite is killed
			if buff.get_type() == "power_up":
			    powerup.play()
			    create_ball(screen, player, endzone, ball_list, \
				        allSprites, scoreboard)
			    buff.kill()

			# If the ball hits a laser sprite a laser beam is shot and
			# all the blocks in that specific row/col loses 1 health
			elif (buff.get_type() == "up" or buff.get_type() == "side")\
			     and ball.get_lasercollide():
			    buff.set_killstatus(True)
			    laser.play()
			    beam = myBBtanSprites.Beam(endzone, buff)
			    allSprites.add(beam)

			    for block in blockGroup:

				# Check which laser beam is being shot and takes
				# away 1 health from the block that is in the
				# same row/column as the laser sprite
				if buff.get_type() == "up" and \
				   block.get_left() == buff.get_left() or \
				   buff.get_type() == "side" and\
				   block.get_top() == buff.get_top():
				    block.lose_health()
				    block.update_health()

			    # Prevents the same ball to hit laser sprite more than
			    # once when it collides
			    ball.set_lasercollide(False)

			# If the ball hits the random direction sprite, it shoots
			# the ball at one of 3 directions and places the ball 1
			# pixel above the random direction sprite
			elif buff.get_type() == "random" and buff.get_top() != 50 \
			     and ball.get_randomcollide():
			    hit2.play()
			    num = random.randrange(0, 3)
			    ball.set_centerxy(buff)
			    ball.switch_direction(num)
			    buff.set_killstatus(True)
			    ball.set_randomcollide(False)

		else:

		    # When ball stops colliding with laser and random direction
		    # sprite make it able to collide again
		    ball.set_randomcollide(True)
		    ball.set_lasercollide(True)


	# If the buffs reach the endzone, kill it
	for buff in buffGroup:
	    if buff.rect.bottom > endzone.rect.top - 25:
		buff.kill()

	# GAME OVER
	# If a block hits the endzone, check if player achieved a new highscore
	# and game ends
	if pygame.sprite.spritecollide(endzone, blockGroup, True):
	    scoreboard.set_highscore()
	    condition = False

	# Clear, update and draw the sprites on the screen
	allSprites.clear(screen, background)
	allSprites.update()
	allSprites.draw(screen)
	pygame.display.flip()

    return True

def loading_screen():
    """This function displays the loading screen until the user hits the play
       button or closes the game window."""

    # Create loading screen background
    background = pygame.image.load(image_path+"loading_screen.png")
    background = background.convert()
    screen.blit(background, (0,0))

    font = pygame.font.SysFont("Courier", 30, True)
    message = font.render("Steven", 1 , (221, 240, 114))
    screen.blit(message, (58, 379))

    pygame.display.flip()

    condition = True
    while condition:

	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		return False

	    # If the user clicks the PLAY button return True
	    elif event.type == pygame.MOUSEBUTTONDOWN:
		mouse_pos = pygame.mouse.get_pos()
		if mouse_pos[0] >= 177 and mouse_pos[0] <= 333 and \
		   mouse_pos[1] >= 468 and mouse_pos[1] <= 537:
		    return True

def main():
    """This function is the mainline logic of my program which starts off at the
       loading screen and runs the game when the user hits the play button, if
       the player loses, it will return to the first level until user closes
       the game window."""

    # Set background music
    pygame.mixer.music.load(music_path+"Vehicle.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    condition = True

    # Loops through the loading screen until the user clicks the play button or
    # closes the game window
    while condition:
	if loading_screen():
	    condition = game()
	else:
	    condition = False

    pygame.quit()

main()
