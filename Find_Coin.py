from tkinter import *
import time

class Game:
	def __init__(self):
		self.tk = Tk()
		self.tk.title('Find the Coin!')
		self.tk.resizable(0, 0)
		self.tk.wm_attributes('-topmost', 1)
		self.canvas = Canvas(self.tk, width=900, height=700, \
		highlightthickness=0)
		self.canvas.pack()
		self.tk.update()
		self.canvas_width = 900
		self.canvas_height = 700
		self.bg = PhotoImage(file='/Find_Coin/images/sprites/fon.gif')
		self.canvas.create_image(0, 0, image=self.bg, anchor='nw')
		self.sprites = []
		self.finding = True
		
	def mainloop(self):
		while 1:
			if self.finding:
				for sprite in self.sprites:
					sprite.move()
			self.tk.update_idletasks()
			self.tk.update()
			time.sleep(0.01)

class Coords:
	def __init__(self, x1=0, y1=0, x2=0, y2=0):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
class Sprite:
	def __init__(self, game):
		self.game = game
		self.endgame = False
		self.coordinates = None
	
	def move(self):
		pass
		
	def coodrs(self):
		return self.coordinates
		
class Wall(Sprite):
	def __init__(self, game, x, y):
		Sprite.__init__(self, game)
		self.photo_image = PhotoImage(file='/Find_Coin/images/sprites/stone.gif')
		self.image = game.canvas.create_image(x, y, \
		image=self.photo_image, anchor='nw')
		self.coordinates = Coords()
		
	def coords(self):
		xy = self.game.canvas.coords(self.image)
		self.coordinates.x1 = xy[0]
		self.coordinates.y1 = xy[1]
		self.coordinates.x2 = xy[0] + 90
		self.coordinates.y2 = xy[1] + 70
		return self.coordinates

class Flower(Sprite):
	def __init__(self, game, x, y):
		Sprite.__init__(self, game)
		self.photo_image = PhotoImage(file='/Find_Coin/images/sprites/flower.gif')
		self.image = game.canvas.create_image(x, y, \
		image=self.photo_image, anchor='nw')
		self.coordinates = Coords()
		self.vis = True
		
	def coords(self):
		xy = self.game.canvas.coords(self.image)
		self.coordinates.x1 = xy[0]
		self.coordinates.y1 = xy[1]
		self.coordinates.x2 = xy[0] + 70
		self.coordinates.y2 = xy[1] + 70
		return self.coordinates
				
	def move(self):
		for sprite in self.game.sprites:
			coord = self.coordinates
			sprite_coord = sprite.coordinates
			if sprite == self:
				continue
			if type(sprite) == Hero and (to_top(coord, sprite_coord) \
			or to_bottom(coord, sprite_coord) \
			or to_left(coord, sprite_coord) \
			or to_right(coord, sprite_coord)):
				self.game.canvas.itemconfig(self.image, state='hidden')
				self.vis = False
				self.game.sprites.remove(self)

class Coin(Sprite):
	def __init__(self, game, flower):
		Sprite.__init__(self, game)
		self.flower = flower
		self.photo_image = PhotoImage(file='/Find_Coin/images/sprites/coin.gif')
		
	def coords(self):
		return self.flower.coordinates
		
	def move(self):
		if self.flower.vis == False:
			self.image = self.game.canvas.create_image(self.flower.coordinates.x1, self.flower.coordinates.y1, \
			image=self.photo_image, anchor='nw')
			time.sleep(1)
			self.game.finding=False
			self.game.canvas.create_text(250, 250, text='YOU WON!')
		
class Hero(Sprite):
	def __init__(self, game):
		Sprite.__init__(self, game)
		self.photo_images_left = [
		PhotoImage(file='/Find_Coin/images/hero/heroL-1.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroL-2.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroL-3.gif')]
		self.photo_images_right = [
		PhotoImage(file='/Find_Coin/images/hero/heroR-1.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroR-2.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroR-3.gif')]
		self.photo_images_up = [
		PhotoImage(file='/Find_Coin/images/hero/heroB-1.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroB-2.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroB-3.gif')]
		self.photo_images_down = [
		PhotoImage(file='/Find_Coin/images/hero/heroF-1.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroF-2.gif'),
		PhotoImage(file='/Find_Coin/images/hero/heroF-3.gif')]
		self.x = 0
		self.y = 0
		self.current_image = 0
		self.image_add = 1
		self.image = game.canvas.create_image(100, 100, \
		image=self.photo_images_down[0], anchor='nw')
		self.last_time = time.time()
		self.coordinates = Coords()
		self.game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
		self.game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
		self.game.canvas.bind_all('<KeyPress-Up>', self.turn_back)
		self.game.canvas.bind_all('<KeyPress-Down>', self.turn_front)
		self.game.canvas.bind_all('<KeyRelease-Left>', self.stop_left)
		self.game.canvas.bind_all('<KeyRelease-Right>', self.stop_right)
		self.game.canvas.bind_all('<KeyRelease-Up>', self.stop_back)
		self.game.canvas.bind_all('<KeyRelease-Down>', self.stop_front)

	def coords(self):
		xy = self.game.canvas.coords(self.image)
		self.coordinates.x1 = xy[0]
		self.coordinates.y1 = xy[1]
		self.coordinates.x2 = xy[0] + 60
		self.coordinates.y2 = xy[1] + 60
		return self.coordinates

	def animate(self):
		if self.x != 0 or self.y != 0:
			if time.time() - self.last_time > 0.1:
				self.last_time = time.time()
				self.current_image += self.image_add
				if self.current_image >= 2:
					self.image_add = -1
				if self.current_image <= 0:
					self.image_add = 1
		if self.x != 0 and self.y == 0:
			if self.x > 0:
				self.game.canvas.itemconfig(self.image, \
				image=self.photo_images_right[self.current_image])
			if self.x < 0:
				self.game.canvas.itemconfig(self.image, \
				image=self.photo_images_left[self.current_image])
		if self.y != 0 and self.x == 0:
			if self.y > 0:
				self.game.canvas.itemconfig(self.image, \
				image=self.photo_images_down[self.current_image])
			if self.y < 0:
				self.game.canvas.itemconfig(self.image, \
				image=self.photo_images_up[self.current_image])

	def move(self):
		self.animate()
		coord = self.coords()
		if self.y > 0 and coord.y2 >= self.game.canvas_height:
			self.y = 0
		elif self.y < 0 and coord.y1 <= 0:
			self.y = 0
		if self.x > 0 and coord.x2 >= self.game.canvas_width:
			self.x = 0
		elif self.x < 0 and coord.x1 <= 0:
			self.x = 0
		for sprite in self.game.sprites:
			sprite_coord = sprite.coords()
			if sprite == self:
				continue
			if self.y < 0 and to_top(coord, sprite_coord):
				self.y = 0
			if self.y > 0 and to_bottom(coord, sprite_coord):
				self.y = 0
			if self.x < 0 and to_left(coord, sprite_coord):
				self.x = 0
			if self.x > 0 and to_right(coord, sprite_coord):
				self.x = 0
		self.game.canvas.move(self.image, self.x, self.y)

	def turn_left(self, evt):
		if self.y == 0:
			self.x = -2

	def turn_right(self, evt):
		if self.y == 0:
			self.x = 2

	def turn_back(self, evt):
		if self.x == 0:
			self.y = -2

	def turn_front(self, evt):
		if self.x == 0:
			self.y = 2

	def stop_left(self, evt):
		self.x = 0

	def stop_right(self, evt):
		self.x = 0

	def stop_back(self, evt):
		self.y = 0

	def stop_front(self, evt):
		self.y = 0

def inside_x(co1, co2):
	if (co1.x1 > co2.x1 and co1.x1 < co2.x2)\
	or (co1.x2 > co2.x1 and co1.x2 < co2.x2)\
	or (co2.x1 > co1.x1 and co2.x1 < co1.x2)\
	or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
		return True
	else:
		return False


def inside_y(co1, co2):
	if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
	or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
	or (co2.y1 > co1.y1 and co2.y2 < co1.y2) \
	or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
		return True
	else:
		return False

def to_top(co1, co2):
	if inside_x(co1, co2):
		if co1.y1 < co2.y2 and co1.y1 >=co2.y1:
			return True
	return False

def to_bottom(co1, co2):
	if inside_x(co1, co2):
		if co1.y2 > co2.y1 and co1.y2 <= co2.y2:
			return True
	return False	

def to_right(co1, co2):
	if inside_y(co1, co2):
		if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
			return True		
	return False

def to_left(co1, co2):
	if inside_y(co1, co2):
		if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
			return True
	return False
	
g = Game()
h = Hero(g)
w1 = Wall(g,500,500)
g.sprites.append(w1)
w2 = Wall(g,320,230)
g.sprites.append(w2)
w3 = Wall(g,100,500)
g.sprites.append(w3)
w4 = Wall(g,190,590)
g.sprites.append(w4)
w5 = Wall(g,10,510)
g.sprites.append(w5)
w6 = Wall(g,500,10)
g.sprites.append(w6)
w7 = Wall(g,410,200)
g.sprites.append(w7)
f1 = Flower(g,400,100)
g.sprites.append(f1)
f2 = Flower(g,350,410)
g.sprites.append(f2)
c1 = Coin(g,f2)
g.sprites.append(c1)
g.sprites.append(h)
g.mainloop()
