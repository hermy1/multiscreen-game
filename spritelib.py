from __future__ import annotations

import random
from tkinter import *
from enum import Enum


class Point:
	def __init__(self, x: int, y: int) -> None:
		super().__init__()
		self.x = x
		self.y = y
	
	@property
	def x(self):
		return self._x
	
	@x.setter
	def x(self, value):
		self._x = value
	
	@property
	def y(self):
		return self._y
	
	@y.setter
	def y(self, value):
		self._y = value
	
	def __str__(self) -> str:
		return f'Point({self._x},{self._y})'
	
	def __repr__(self) -> str:
		return self.__str__()


class Clamp:
	def __init__(self, left_limit: int = 0, right_limit: int = 800, top_limit: int = 0,
				 bottom_limit: int = 600) -> None:
		super().__init__()
		self.left_limit = left_limit
		self.right_limit = right_limit
		self.top_limit = top_limit
		self.bottom_limit = bottom_limit
	
	def clampall(self, sprite: Sprite):
		Clamp.clamp_all(sprite, self.left_limit, self.right_limit, self.top_limit, self.bottom_limit)
	
	@classmethod
	def clamp_x(cls, sprite: Sprite, left_limit: int = 0, right_limit: int = 800):
		if sprite.x < left_limit:
			sprite.x = left_limit
		elif sprite.right > right_limit:
			sprite.right = right_limit
	
	@classmethod
	def clamp_y(cls, sprite: Sprite, top_limit: int = 0,
				bottom_limit: int = 600):
		if sprite.y < top_limit:
			sprite.y = top_limit
		elif sprite.bottom > bottom_limit:
			sprite.bottom = bottom_limit
	
	@classmethod
	def clamp_all(cls, sprite: Sprite, left_limit: int = 0, right_limit: int = 800,
				  top_limit: int = 0, bottom_limit: int = 600):
		cls.clamp_x(sprite, left_limit, right_limit)
		cls.clamp_y(sprite, top_limit, bottom_limit)


class Direction(Enum):
	LEFT = "Left"
	UP = "Up"
	RIGHT = "Right"
	DOWN = "Down"
	STOPPED = "Stopped"


class Sprite:
	def __init__(self, x: int = 0, y: int = 0, width: int = 25,
				 height: int = 25,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '', image: PhotoImage = None) -> None:
		super().__init__()
		self.x = x
		self.y = y
		self._width = width
		self._height = height
		self.border_color = border_color
		self.border_width = border_width
		self.fill_color = fill_color
		self._image = image
		if self._image is not None:
			self._width = self._image.width()
			self._height = self._image.height()
	
	@property
	def center_x(self):
		return self.x + self._width // 2
	
	@center_x.setter
	def center_x(self, value: int):
		self.x = value - self._width // 2
	
	@property
	def center_y(self):
		return self.y + self._height // 2
	
	@center_y.setter
	def center_y(self, value):
		self.y = value - self._height // 2
	
	@property
	def center(self):
		return Point(self.x + self._width // 2, self.y + self._height // 2)
	
	@center.setter
	def center(self, value: Point):
		self.x = value.x - self._width // 2
		self.y = value.y - self._height // 2
	
	@property
	def width(self):
		return self._width
	
	@width.setter
	def width(self, value):
		if self._image is not None:
			raise Exception('cannot set width if sprite has image')
		self._width = value
	
	@property
	def height(self):
		return self._height
	
	@height.setter
	def height(self, value):
		if self._image is not None:
			raise Exception('cannot set height if sprite has image')
		self._height = value
	
	@property
	def image(self):
		return self._image
	
	@image.setter
	def image(self, value):
		self._image = value
		self._width = self._image.width()
		self._height = self._image.height()
	
	@property
	def left(self):
		return self.x
	
	@left.setter
	def left(self, value):
		self.x = value
	
	@property
	def right(self):
		return self.x + self._width
	
	@right.setter
	def right(self, value):
		self.x = value - self._width
	
	@property
	def top(self):
		return self.y
	
	@top.setter
	def top(self, value):
		self.y = value
	
	@property
	def bottom(self):
		return self.y + self._height
	
	@bottom.setter
	def bottom(self, value):
		self.y = value - self._height
	
	def draw(self, canvas: Canvas):
		canvas.create_rectangle(self.left, self.top,
								self.right, self.bottom,
								outline=self.border_color,
								fill=self.fill_color,
								width=self.border_width)
		canvas.create_image(self.x, self.y, anchor=NW,
							image=self._image)
	
	def increment_x(self, distance: int):
		self.x += distance
	
	def increment_y(self, distance: int):
		self.y += distance
	
	def bbox(self):
		t = (self.left, self.top, self.right, self.bottom)
		return t
	
	def intersects(self, box):
		a = self
		b = Sprite(box[0], box[1], box[2] - box[0], box[3] - box[1])
		return not (a.right < b.left or a.left > b.right
					or a.bottom < b.top or a.top > b.bottom)
	
	def contains(self, x: int, y: int):
		return (x in range(self.left, self.right)) \
			   and (y in range(self.top, self.bottom))
	
	def __str__(self) -> str:
		return str(self.__dict__).replace('_', '')


class Mover:
	def __init__(self, sprite: Sprite,
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 100, speed: int = 1):
		self._sprite = sprite
		self._direction = direction
		self._delay_time = delay_time
		self._speed = abs(speed)
		self._elapsed_time = 0
	
	def update(self, delta_time: int):
		self._elapsed_time += delta_time
		if self._elapsed_time >= self._delay_time:
			self._elapsed_time = 0
			if self._direction == Direction.LEFT:
				self._sprite.increment_x(-self._speed)
			elif self._direction == Direction.RIGHT:
				self._sprite.increment_x(self._speed)
			elif self._direction == Direction.UP:
				self._sprite.increment_y(-self._speed)
			elif self._direction == Direction.DOWN:
				self._sprite.increment_y(self._speed)
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def direction(self):
		return self._direction
	
	@direction.setter
	def direction(self, value: Direction):
		self._direction = value
	
	@property
	def delay_time(self):
		return self._delay_time
	
	@delay_time.setter
	def delay_time(self, value: int):
		self._delay_time = value
	
	@property
	def speed(self):
		return self._speed
	
	@speed.setter
	def speed(self, value: int):
		self._speed = abs(value)
	
	def backup(self):
		if self._direction == Direction.LEFT:
			self._sprite.increment_x(self._speed)
		elif self._direction == Direction.RIGHT:
			self._sprite.increment_x(-self._speed)
		elif self._direction == Direction.UP:
			self._sprite.increment_y(self._speed)
		elif self._direction == Direction.DOWN:
			self._sprite.increment_y(-self._speed)


class Jumper:
	
	def __init__(self, sprite: Sprite, jump_ability: int = -5,
				 vertical_delay_time: int = 10,
				 gravity: float = .1,
				 platforms: list = None) -> None:
		super().__init__()
		self._sprite = sprite
		self._vertical_speed = 0
		self._jump_ability = jump_ability
		self._vertical_delay_time = vertical_delay_time
		self._gravity = gravity
		self._is_jumping = True
		self._elapsed_time = 0
		self._platforms = platforms
	
	@property
	def platforms(self):
		return self._platforms
	
	@platforms.setter
	def platforms(self, value: list):
		self._platforms = value
	
	@property
	def jump_ability(self):
		return self._jump_ability
	
	@jump_ability.setter
	def jump_ability(self, value):
		self._jump_ability = value
	
	@property
	def is_jumping(self):
		return self._is_jumping
	
	@is_jumping.setter
	def is_jumping(self, value: bool):
		self._is_jumping = value
	
	@property
	def gravity(self):
		return self._gravity
	
	@gravity.setter
	def gravity(self, value: float):
		self._gravity = value
	
	@property
	def vertical_delay_time(self):
		return self._vertical_delay_time
	
	@vertical_delay_time.setter
	def vertical_delay_time(self, value: int):
		self._vertical_delay_time = value
	
	@property
	def vertical_speed(self):
		return self._vertical_speed
	
	@vertical_speed.setter
	def vertical_speed(self, speed: int):
		self._vertical_speed = speed
	
	def jump(self, force: int = None):
		if not self._is_jumping:
			self._is_jumping = True
			if force is None:
				self._vertical_speed = self._jump_ability
			else:
				self._vertical_speed = force
	
	@property
	def sprite(self):
		return self._sprite
	
	def get_intersects_with(self):
		for p in self._platforms:
			if self._sprite.intersects(p.bbox()):
				return p
		return None
	
	def update(self, delta_time: int):
		if self.get_intersects_with() is None:
			self._is_jumping = True
		if self._is_jumping:
			self._elapsed_time += delta_time
			if self._elapsed_time >= self._vertical_delay_time:
				self._elapsed_time = 0
				intersects = False
				self._vertical_speed += self._gravity
				self._sprite.increment_y(int(self._vertical_speed))
				platform = self.get_intersects_with()
				if platform is not None:
					if self._vertical_speed < 0:
						self._vertical_speed = -self._vertical_speed  # doesn't allow jumper to pass through platform
						# self._vertical_speed = 0  # allows jumper to pass through platform
						self._sprite.top = platform.bottom
					
					elif self._vertical_speed > 0 and \
							self._sprite.bottom >= platform.top:
						self._is_jumping = False
						self._vertical_speed = 0
						self._sprite.bottom = platform.top
				
				else:
					self.is_jumping = True


class Animation:
	def __init__(self, sprite: Sprite, images: list,
				 frame_delay: int = 100) -> None:
		self._images = images
		self._frame_delay = frame_delay
		self._current_frame = 0
		self._elapsed_time = 0
		self._paused = False
		self._sprite = sprite
	
	def update(self, deltaTime: int):
		if self._paused:
			self._elapsed_time = 0
		else:
			self._elapsed_time += deltaTime
			if self._elapsed_time > self._frame_delay:
				self._elapsed_time = 0
				self._current_frame += 1
				if self._current_frame >= len(self._images):
					self._current_frame = 0
			self._sprite.image = self._images[self._current_frame]
	
	@property
	def paused(self):
		return self._paused
	
	@paused.setter
	def paused(self, value: bool):
		self._paused = value
	
	@property
	def frame_delay(self):
		return self._frame_delay
	
	@frame_delay.setter
	def frame_delay(self, value: int):
		self._frame_delay = value
	
	@property
	def current_frame(self):
		return self._current_frame
	
	@property
	def images(self):
		return self._images
	
	@property
	def current_image(self):
		return self._images[self._current_frame]
	
	@images.setter
	def images(self, image_list: list):
		self._images = image_list
	
	def __str__(self) -> str:
		return "frame delay: {}, current frame: {}, elapsed time: {}".format(self._frame_delay, self._current_frame,
																			 self._elapsed_time)


class AnimatedMovingSprite:
	
	def __init__(self, images: list, x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800,
				 top_limit: int = 0, bottom_limit: int = 600
				 ) -> None:
		super().__init__()
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, images[0])
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, images, frame_delay)
		self.clamp = Clamp(left_limit, right_limit, top_limit, bottom_limit)
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		self._animation.update(delta_time)
		self.clamp.clamp_all(self._sprite)


class AnimatedHorizontalMovingSprite:
	
	def __init__(self, left_images: list, right_images: list, x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 15, speed: int = 3,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800
				 ) -> None:
		super().__init__()
		self.left_images = left_images
		self.right_images = right_images
		self.left_limit = left_limit
		self.right_limit = right_limit
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, right_images[0])
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, right_images, frame_delay)
	
	@property
	def left_images(self):
		return self._left_images
	
	@left_images.setter
	def left_images(self, value):
		self._left_images = value
	
	@property
	def right_images(self):
		return self._right_images
	
	@right_images.setter
	def right_images(self, value):
		self._right_images = value
	
	@property
	def left_limit(self):
		return self._left_limit
	
	@left_limit.setter
	def left_limit(self, value):
		self._left_limit = value
	
	@property
	def right_limit(self):
		return self._right_limit
	
	@right_limit.setter
	def right_limit(self, value):
		self._right_limit = value
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		
		if self._sprite.left < self._left_limit:
			self._sprite.left = self._left_limit
		elif self._sprite.right > self._right_limit:
			self._sprite.right = self._right_limit
			
		if self._mover.direction == Direction.LEFT:
			self._animation.images = self._left_images
		elif self._mover.direction == Direction.RIGHT:
			self._animation.images = self._right_images
		self._animation.update(delta_time)


class Animated4WayMovingSprite:
	
	def __init__(self, left_images: list, right_images: list,
				 up_images: list, down_images: list,
				 x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800,
				 top_limit: int = 0, bottom_limit: int = 600) -> None:
		super().__init__()
		self._animated_moving_sprite = AnimatedMovingSprite(right_images, x, y, border_color,
															border_width, fill_color, direction, delay_time,
															speed, frame_delay, left_limit, right_limit,
															top_limit, bottom_limit)
		self._sprite = self._animated_moving_sprite.sprite
		self._mover = self._animated_moving_sprite.mover
		self._animation = self._animated_moving_sprite.animation
		self._left_images = left_images
		self._right_images = right_images
		self._up_images = up_images
		self._down_images = down_images
		if self.mover.direction == Direction.LEFT:
			self._animated_moving_sprite.animation.images = self._left_images
		elif self.mover.direction == Direction.RIGHT:
			self._animated_moving_sprite.animation.images = self._right_images
		elif self.mover.direction == Direction.UP:
			self._animated_moving_sprite.animation.images = self._up_images
		elif self.mover.direction == Direction.DOWN:
			self._animated_moving_sprite.animation.images = self._down_images
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return
	
	@property
	def left_images(self):
		return self._left_images
	
	@left_images.setter
	def left_images(self, images: list):
		self._left_images = images
	
	@property
	def right_images(self):
		return self._right_images
	
	@right_images.setter
	def right_images(self, images: list):
		self._right_images = images
	
	@property
	def up_images(self):
		return self.up_images
	
	@up_images.setter
	def up_images(self, images: list):
		self._up_images = images
	
	@property
	def down_images(self):
		return self._down_images
	
	@down_images.setter
	def down_images(self, images: list):
		self._down_images = images
	
	def draw(self, canvas):
		self._animated_moving_sprite.draw(canvas)
	
	def update(self, delta_time):
		self._animated_moving_sprite.update(delta_time)
		if self.mover.direction == Direction.LEFT:
			self._animated_moving_sprite.animation.images = self._left_images
		elif self.mover.direction == Direction.RIGHT:
			self._animated_moving_sprite.animation.images = self._right_images
		elif self.mover.direction == Direction.UP:
			self._animated_moving_sprite.animation.images = self._up_images
		elif self.mover.direction == Direction.DOWN:
			self._animated_moving_sprite.animation.images = self._down_images


class AnimatedHorizontalBouncer:
	def __init__(self, leftImages: list, rightImages: list,
				 x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800
				 ) -> None:
		super().__init__()
		self._left_images = leftImages
		self._right_images = rightImages
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, rightImages[0])
		self._sprite.border_width = 0
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, rightImages, frame_delay)
		self._left_limit = left_limit
		self._right_limit = right_limit
	
	@property
	def left_limit(self):
		return self._left_limit
	
	@left_limit.setter
	def left_limit(self, left_limit: int):
		self._left_limit = left_limit
	
	@property
	def right_limit(self):
		return self._right_limit
	
	@right_limit.setter
	def right_limit(self, right_limit: int):
		self._right_limit = right_limit
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		if self._mover.direction == Direction.LEFT and \
				self._sprite.left < self._left_limit:
			self._sprite.left = self._left_limit
			self._mover.direction = Direction.RIGHT
		
		elif self._mover.direction == Direction.RIGHT and \
				self._sprite.right > self._right_limit:
			self._sprite.right = self._right_limit
			self._mover.direction = Direction.LEFT
		
		if self._mover.direction == Direction.LEFT:
			self._animation.images = self._left_images
		elif self._mover.direction == Direction.RIGHT:
			self._animation.images = self._right_images
		
		self._animation.update(delta_time)


class AnimatedHorizontalRepeater:
	def __init__(self, leftImages: list, rightImages: list,
				 x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800
				 ) -> None:
		super().__init__()
		self._left_images = leftImages
		self._right_images = rightImages
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, rightImages[0])
		self._sprite.border_width = 0
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, rightImages, frame_delay)
		self._left_limit = left_limit
		self._right_limit = right_limit
	
	@property
	def left_limit(self):
		return self._left_limit
	
	@left_limit.setter
	def left_limit(self, left_limit: int):
		self._left_limit = left_limit
	
	@property
	def right_limit(self):
		return self._right_limit
	
	@right_limit.setter
	def right_limit(self, right_limit: int):
		self._right_limit = right_limit
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		if self._mover.direction == Direction.LEFT:
			self._animation.images = self._left_images
		elif self._mover.direction == Direction.RIGHT:
			self._animation.images = self._right_images
		
		if self._mover.direction == Direction.LEFT and \
				self._sprite.right < self._left_limit:
			self._sprite.left = self._right_limit
		elif self._mover.direction == Direction.RIGHT and \
				self._sprite.left > self._right_limit:
			self._sprite.right = self._left_limit
		
		self._animation.update(delta_time)


class AnimatedVerticalBouncer:
	def __init__(self, upImages: list, downImages: list,
				 x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.DOWN,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 top_limit: int = 0, bottom_limit: int = 600
				 ) -> None:
		super().__init__()
		self._up_images = upImages
		self._down_images = downImages
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, downImages[0])
		self._sprite.border_width = 0
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, downImages, frame_delay)
		self.top_limit = top_limit
		self._bottom_limit = bottom_limit
	
	@property
	def top_limit(self):
		return self._top_limit
	
	@top_limit.setter
	def top_limit(self, top_limit: int):
		self._top_limit = top_limit
	
	@property
	def bottom_limit(self):
		return self._bottom_limit
	
	@bottom_limit.setter
	def bottom_limit(self, bottom_limit: int):
		self._bottom_limit = bottom_limit
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		if self._mover.direction == Direction.UP and \
				self._sprite.top < self.top_limit:
			self._sprite.top = self.top_limit
			self._mover.direction = Direction.DOWN
		
		elif self._mover.direction == Direction.DOWN and \
				self._sprite.bottom > self._bottom_limit:
			self._sprite.bottom = self._bottom_limit
			self._mover.direction = Direction.UP
		
		if self._mover.direction == Direction.UP:
			self._animation.images = self._up_images
		elif self._mover.direction == Direction.DOWN:
			self._animation.images = self._down_images
		self._animation.update(delta_time)
		
		self._animation.update(delta_time)


class AnimatedVerticalRepeater:
	def __init__(self, upImages: list, downImages: list,
				 x: int = 0, y: int = 0,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 direction: Direction = Direction.DOWN,
				 delay_time: int = 100, speed: int = 1,
				 frame_delay: int = 100,
				 top_limit: int = 0, bottom_limit: int = 600
				 ) -> None:
		super().__init__()
		self._up_images = upImages
		self._down_images = downImages
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, downImages[0])
		self._sprite.border_width = 0
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._animation = Animation(self._sprite, downImages, frame_delay)
		self.top_limit = top_limit
		self._bottom_limit = bottom_limit
	
	@property
	def top_limit(self):
		return self._top_limit
	
	@top_limit.setter
	def top_limit(self, top_limit: int):
		self._top_limit = top_limit
	
	@property
	def bottom_limit(self):
		return self._bottom_limit
	
	@bottom_limit.setter
	def bottom_limit(self, bottom_limit: int):
		self._bottom_limit = bottom_limit
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		
		if self._mover.direction == Direction.UP and \
				self._sprite.bottom < self.top_limit:
			self._sprite.top = self.bottom_limit
		elif self._mover.direction == Direction.DOWN and \
				self._sprite.top > self._bottom_limit:
			self._sprite.bottom = self._top_limit
		
		if self._mover.direction == Direction.UP:
			self._animation.images = self._up_images
		elif self._mover.direction == Direction.DOWN:
			self._animation.images = self._down_images
		self._animation.update(delta_time)


class AnimatedPlatformer:  # animated clamped moving jumping sprite
	
	def __init__(self, left_images: list, right_images: list,
				 x: int = 0, y: int = 0,
				 border_color: str = '', border_width: int = 0,
				 fill_color: str = '',
				 direction: Direction = Direction.RIGHT,
				 delay_time: int = 33, speed: int = 3,
				 jump_ability: int = -12,
				 vertical_delay_time: int = 10,
				 gravity: float = .5,
				 platforms: list = None, left_limit: int = 0,
				 right_limit: int = 800, top_limit: int = 0,
				 bottom_limit: int = 600,
				 frame_delay: int = 75
				 ) -> None:
		super().__init__()
		self._sprite = Sprite(x, y, 0, 0, border_color=border_color, border_width=border_width, fill_color=fill_color)
		self._mover = Mover(self._sprite, direction, delay_time, speed)
		self._jumper = Jumper(self._sprite, jump_ability, vertical_delay_time, gravity, platforms)
		self._clamper = Clamp(left_limit, right_limit, top_limit, bottom_limit)
		self._left_images = left_images
		self._right_images = right_images
		self._animation = Animation(self._sprite, self._right_images, frame_delay)
		if self._mover.direction == Direction.LEFT:
			self._animation.images = self._left_images
	
	@property
	def left_images(self):
		return self._left_images
	
	@left_images.setter
	def left_images(self, value: list):
		left_images = value
	
	@property
	def right_images(self):
		return self._right_images
	
	@right_images.setter
	def right_images(self, value: list):
		right_images = value
	
	@property
	def animation(self):
		return self._animation
	
	@property
	def clamper(self):
		return self._clamper
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def jumper(self):
		return self._jumper
	
	def draw(self, canvas: Canvas):
		self._sprite.draw(canvas)
	
	def update(self, delta_time: int):
		d = self._mover.direction
		if d == Direction.LEFT or d == Direction.RIGHT:
			self._mover.update(delta_time)
			if d == Direction.LEFT:
				self._animation.images = self._left_images
			elif d == Direction.RIGHT:
				self._animation.images = self._right_images
		self._jumper.update(delta_time)
		self._clamper.clamp_all(self._sprite)
		if self._sprite.bottom == self._clamper.bottom_limit:
			self._jumper.is_jumping = False
			self._jumper.vertical_speed = 0
		self._animation.update(delta_time)


class AnimatedRandomFallingObject:
	def __init__(self, downImages: list,
				 border_color: str = 'black', border_width: int = 2,
				 fill_color: str = '',
				 min_delay_time: int = 10, max_delay_time: int = 30,
				 min_speed: int = 1, max_speed: int = 10,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800,
				 top_limit: int = -600, bottom_limit: int = 600
				 ) -> None:
		super().__init__()
		self._down_images = downImages
		x = random.randint(0, right_limit - downImages[0].width())
		y = random.randint(top_limit, 0)
		speed = random.randint(min_speed, max_speed)
		delay_time = random.randint(min_delay_time, max_delay_time)
		self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
							  fill_color, downImages[0])
		self._sprite.border_width = 0
		self._mover = Mover(self._sprite, Direction.DOWN, delay_time, speed)
		self._animation = Animation(self._sprite, downImages, frame_delay)
		self.top_limit = top_limit
		self.bottom_limit = bottom_limit
		self.left_limit = left_limit
		self.right_limit = right_limit
		self.min_delay_time = min_delay_time
		self.max_delay_time = max_delay_time
		self.min_speed = min_speed
		self.max_speed = max_speed
	
	@property
	def down_images(self):
		return self._down_images
	
	@down_images.setter
	def down_images(self, images: list):
		self._down_images = images
		self._animation.images = images
	
	@property
	def min_delay_time(self):
		return self._min_delay_time
	
	@min_delay_time.setter
	def min_delay_time(self, value):
		self._min_delay_time = value
	
	@property
	def max_delay_time(self):
		return self._max_delay_time
	
	@max_delay_time.setter
	def max_delay_time(self, value):
		self._max_delay_time = value
	
	@property
	def min_speed(self):
		return self._min_speed
	
	@min_speed.setter
	def min_speed(self, value):
		self._min_speed = value
	
	@property
	def max_speed(self):
		return self._max_speed
	
	@max_speed.setter
	def max_speed(self, value):
		self._max_speed = value
	
	@property
	def left_limit(self):
		return self._left_limit
	
	@left_limit.setter
	def left_limit(self, left_limit: int):
		self._left_limit = left_limit
	
	@property
	def right_limit(self):
		return self._right_limit
	
	@right_limit.setter
	def right_limit(self, right_limit: int):
		self._right_limit = right_limit
	
	@property
	def top_limit(self):
		return self._top_limit
	
	@top_limit.setter
	def top_limit(self, top_limit: int):
		self._top_limit = top_limit
	
	@property
	def bottom_limit(self):
		return self._bottom_limit
	
	@bottom_limit.setter
	def bottom_limit(self, bottom_limit: int):
		self._bottom_limit = bottom_limit
	
	@property
	def sprite(self):
		return self._sprite
	
	@property
	def mover(self):
		return self._mover
	
	@property
	def animation(self):
		return self._animation
	
	def draw(self, canvas):
		self._sprite.draw(canvas)
	
	def reset_position(self):
		self._sprite.x = random.randint(0,
										self._right_limit - self._sprite.width)
		self._sprite.y = random.randint(self._top_limit, 0)
		self._mover.speed = random.randint(self._min_speed, self._max_speed)
		self._mover.delay_time = random.randint(self._min_delay_time,
												self._max_delay_time)
	
	def update(self, delta_time):
		self._mover.update(delta_time)
		
		if self._mover.direction == Direction.DOWN and \
				self._sprite.top > self._bottom_limit:
			self.reset_position()
		
		self._animation.update(delta_time)


class AnimatedRandomFallingObjects:
	
	def __init__(self, downImages: list, number_objects: int = 4,
				 border_color: str = 'black', border_width: int = 0,
				 fill_color: str = '',
				 min_delay_time: int = 10, max_delay_time: int = 30,
				 min_speed: int = 1, max_speed: int = 10,
				 frame_delay: int = 100,
				 left_limit: int = 0, right_limit: int = 800,
				 top_limit: int = -600, bottom_limit: int = 600) -> None:
		super().__init__()
		self.number_objects = number_objects
		self.objects = []
		for i in range(0, number_objects):
			obj = AnimatedRandomFallingObject(downImages, border_color,
											  border_width, fill_color,
											  min_delay_time, max_delay_time,
											  min_speed, max_speed,
											  frame_delay, left_limit,
											  right_limit, top_limit,
											  bottom_limit)
			self.objects.append(obj)
	
	@property
	def number_objects(self):
		return self._number_objects
	
	@number_objects.setter
	def number_objects(self, value):
		self._number_objects = value
	
	@property
	def objects(self):
		return self._objects
	
	@objects.setter
	def objects(self, value):
		self._objects = value
	
	def get_falling_object(self, index: int):
		if index < 0 or index >= len(self._objects):
			return self._objects[0]
		return self._objects[index]
	
	def draw(self, canvas):
		for obj in self._objects:
			obj.draw(canvas)
	
	def update(self, delta_time):
		for obj in self._objects:
			obj.update(delta_time)
	
	def intersects(self, bbox) -> list:
		intersections = []
		for obj in self._objects:
			if obj.sprite.intersects(bbox):
				intersections.append(obj)
		return intersections
