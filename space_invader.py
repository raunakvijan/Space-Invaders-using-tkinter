from tkinter import *
import time
import threading 
import random
from tkinter import messagebox


class Fire:
	def __init__(self, x, y, direction):
		self.x = x
		if(direction == "up"):
			self.line = canvas.create_line(self.x, 410, self.x, 390, fill="red")
			self.moveUp()
		else:
			self.line = canvas.create_line(self.x, y + 20, self.x, y, fill="red")
			self.moveDown()

	def moveUp(self):
		canvas.move(self.line, 0, -speed)
		for n,alien in enumerate(alien_array):
			if(not alien.alive):
				continue
			x = canvas.coords(self.line)

			if(x[1] < 0):
				canvas.delete(self.line)
				return 
			min_x , _, max_x, _ = alien_c = canvas.coords(alien.a)

			if (alien.y >= x[3] and min_x < self.x + alien.r and max_x > self.x - alien.r):
				global kills
				kills+=1
				canvas.delete(alien.a)
				canvas.delete(self.line)
				alien.alive = False
				del self
				return
		canvas.after(50, self.moveUp)

	def moveDown(self):
		canvas.move(self.line, 0, speed)

		x = canvas.coords(self.line)
		#print(x)
		space_c = canvas.coords(spaceship.poly)
		x1 = space_c[2] 
		x2 = space_c[4]
		# print(x[3])
		# print(x1,x2)
		# print(self.x)

		if(x[3]>=420):
			canvas.delete(self.line
				)
			return
		if(400 <= x[3] and self.x >= x1 and x2 >= self.x):
			print()

			print("BOOM")
			global end

			if(end  == False):
				end = True
				messagebox.showerror("Game over", "You killed "+ str(kills)+ " aliens")
				canvas.delete(self.line)
				exit()

		canvas.after(100, self.moveDown)
		

class Alien:
	def __init__(self, x, y, r, color):
		self.x = x
		self.y = y
		self.r = r
		self.alive = True
		x0 = x - r

		y0 = y - r
		x1 = x + r
		y1 = y + r
		self.steps = 0
		self.direction = 1 
		self.a = canvas.create_oval(x0, y0, x1, y1,fill=color)
		self.move()


	def move(self):
		self.steps+=1
		if(self.steps<= 8):
			canvas.move(self.a, self.direction*5, 1)
		else:
			self.direction*=-1
			self.steps = -8
		canvas.after(1000, self.move)


class Spaceship:
	def __init__(self, master):

		self.x = 250
		self.side = 20
		self.displace = 0
		self.screen_size = 500
		self.ht = self.screen_size//2 - self.side//2
		self.draw(master)

	def draw(self,master):
		self.poly = canvas.create_polygon([self.side//2 + self.ht ,420,self.ht ,self.side + 420,self.side + self.ht ,self.side + 420], outline='gray', fill='gray', width=2)

	def moveLeft(self,master):
		if(self.displace>= -230):
			self.displace-=10
			canvas.move(self.poly, -10, 0)
			canvas.update()
			time.sleep(.01)
		
	def moveRight(self,master):
		if(self.displace<= 230):
			self.displace+=10
			canvas.move(self.poly, 10, 0)
			canvas.update()
			time.sleep(.01)

	def fire(self,master):
		Fire(canvas.coords(self.poly)[0], 0, "up")

## speed of fire
speed = 10
kills = 0
end = False 

## opponent move speed 
opp_speed = 10

## move
root = Tk()

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)


# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

frame  = Frame(root, width = 500, height = 500)
frame.pack_propagate(0)
frame.pack()
w = Label(frame,text="SPACE INVADERS", bg="grey")

canvas = Canvas(frame, width=500, height=500, bg="black")

spaceship = Spaceship(root)
root.bind("<Left>", spaceship.moveLeft)
root.bind("<Right>", spaceship.moveRight)
root.bind("<Return>", spaceship.fire)

w.config(height=2, font= 44)

w.pack(fill=X)
canvas.pack(fill=BOTH, anchor="s")


alien_array = []

color = "green"
for y in range(30,200, 50):
	for x in range(100,430, 50):
		alien_array.append(Alien(x,y, 10, color))
		color = "blue" if color == "green" else "green"		

def move_b():
	alien = alien_array[random.randint(0, len(alien_array)) - 1] 
	Fire(alien.x, alien.y+alien.r ,"down")
	root.after(1000, move_b)

move_b()
root.mainloop()