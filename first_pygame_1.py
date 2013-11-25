import pygame, sys, random
from pygame.locals import *

pygame.init()

def generatemine(count):
	mine = []
	while count>0:
		new_mine = random.randint(0,80)
    		if new_mine not in mine:
       		  mine.append(new_mine)
       		  count -= 1
	return mine

def loadflag(xblock, yblock):
	flagx = xblock*50
	flagy = yblock*50
	flag = pygame.image.load('flag.jpg')
	return flag, flagx, flagy

def printtext(number, colour, mousex, mousey):
	textsurf = BASICFONT.render(str(number), True, colour)
	textrect = textsurf.get_rect()
	textrect.center = mousex + 25, mousey + 25
	return textsurf, textrect

def checkmine(minelist, blocknum):
	if blocknum in minelist:
		return True
	else:
		return False

def checkminenumber(MINE, neighbour):
	minenumber = 0
	for tile in neighbour:
		if tile in MINE:
			minenumber += 1
	return minenumber

def getindex(num):
	if num == 0:
		return [num, num+1]
	elif num == 8:
		return [num-1, num]
	else:
		return [num-1, num, num+1]

def getneighbours(xindex, yindex):
	xneighbours = getindex(xindex)
	yneighbours = getindex(yindex)
	neighbours = [u*9+ v for u in xneighbours for v in yneighbours]
	return [x for x in neighbours if x != xindex*9 + yindex] 

def gameexit():
	pygame.quit()
	sys.exit()
	return

DisplaySurf = pygame.display.set_mode((450, 450))
pygame.display.set_caption('My Mines')
ROW = 9
COL = 9
BGCOLOR = (100, 100, 100)
WHITE = (255, 255, 255)
BASICFONT = pygame.font.Font('freesansbold.ttf', 28)
MINE = generatemine(10)

draw_index = [(x, y) for x in range(ROW) for y in range(COL)]

count = 0
while count< len(draw_index):
    pygame.draw.rect(DisplaySurf, WHITE, (draw_index[count][0]*50, draw_index[count][1]*50, 50, 50), 5)
    count +=1

def getBlockindex(x, y):
	xblock = x/50
	yblock = y/50
	return xblock, yblock

opentilelist = []
flagtilelist =[]

while True:
	mouseclick = False
	mineclick = False
	
	for event in pygame.event.get():
		if event.type == QUIT:
			gameexit()
		elif event.type == MOUSEBUTTONUP:
			mousex, mousey = event.pos
			mouseclick = True

	if mouseclick:
		xblock, yblock = getBlockindex(mousex, mousey)
		tile = xblock*9 +yblock

		if tile not in opentilelist or tile in flagtilelist:
			
			mineclick = checkmine(MINE, xblock*9 + yblock)

			if event.button == 1 and mineclick == False:
				opentilelist.append(tile)
				neighbours = getneighbours(xblock, yblock)
				minenumber = checkminenumber(MINE, neighbours)
				textsurf, textrect = printtext(minenumber, WHITE, xblock*50, yblock*50)
				DisplaySurf.blit(textsurf, textrect)
			elif event.button == 1 and mineclick == True:
				print 'GAME OVER'
				gameexit()
			elif event.button == 3:
				flagtilelist.append(tile)
				flag, flagx, flagy = loadflag(xblock, yblock)
				DisplaySurf.blit(flag, (flagx, flagy))
		if len(opentilelist) == 71:
			print 'You Won'
			gameexit()

 	pygame.display.update()


