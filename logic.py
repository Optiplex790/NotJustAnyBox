import pygame, math, pymunk
from pygame import BLEND_RGBA_MULT

pygame.init()
pygame.font.init()
fps_font = pygame.font.SysFont("Arial", 24)

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

basebox_img = pygame.image.load("basebox.jpg").convert()
light_circle = pygame.image.load("light_circle.png").convert_alpha()
overlay = pygame.image.load("overlay.png").convert_alpha()
logo_img = pygame.image.load("NOT just Any Box.png").convert_alpha()
play_img = pygame.image.load("PLAY.png").convert_alpha()
first_screen_img = pygame.image.load("first_screen.png").convert_alpha()
first_screen_img.set_alpha(0)

background_imgs = []
for i in range(13):
    background_imgs.append(pygame.image.load(f"level_bg/level_bg ({i+1}).png").convert())

#Gets the distance between pos1 and pos2
def get_distance(pos1, pos2):
    pos3 = math.sqrt((pos2[0]-pos1[0])**2+(pos2[1] - pos1[1])**2)
    return pos3

#Rotates an image around its center instead of by the left top corner
def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect

#Returns the global position of a relative position of a body
def get_relative_position(rel_pos, body):
    rel_dist, rel_angle = math.hypot(*rel_pos), math.atan2(rel_pos[1], rel_pos[0])
    angle = rel_angle + body.angle
    pos = body.position[0] + rel_dist * math.cos(angle), body.position[1] + rel_dist * math.sin(angle)
    return pos

def pixel_perfect_collision(mask1, mask2, offset):
    return mask1.overlap_mask(mask2, offset)

def screen_lighting(objects, screen):
    new_image = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.SRCALPHA)
    new_image.fill("black")
    for object in objects:
        new_image.blit(object[2], (object[0][0]-object[2].get_width()/2, object[0][1]-object[2].get_height()/2))
        new_image.blit(overlay, (object[0][0]-overlay.get_width()/2, object[0][1]-overlay.get_height()/2))
    screen.blit(new_image, (0,0), special_flags=BLEND_RGBA_MULT)

def get_vertices(shape):
    verts = []
    for v in shape.get_vertices():
        x = v.rotated(shape.body.angle)[0] + shape.body.position[0]
        y = v.rotated(shape.body.angle)[1] + shape.body.position[1]
        verts.append((x, y))
    print(verts)

class physbox():
    def __init__(self, x, y, space, image = basebox_img, static = False, mass = 1, friction = 0.5):
        #Pygame variables
        self.image = pygame.transform.scale(image, (image.get_width()+1, image.get_height()+1))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_frect()
        self.image.set_colorkey((0,0,0))
        #Pymunk variables
        self.static = static
        if not self.static:
            self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, (self.rect.width, self.rect.height)))
        else:
            self.body = pymunk.Body(body_type=self.static)
        self.poly = pymunk.Poly.create_box(self.body,(self.rect.width, self.rect.height))
        self.poly.mass, self.poly.friction = mass, friction
        self.rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        space.add(self.body, self.rotation_limit_body, self.poly)
        self.body.position = (x+self.rect.width/2,y+self.rect.height/2)
        space.reindex_shapes_for_body(self.body)

    def update(self, screen, space):
        #Rotates an image and changes the rect accordingly if dynamic
        self.rect.centerx = self.body.position[0]
        self.rect.centery = self.body.position[1]
        self.rotated_image, self.rect = rot_center(self.image, math.degrees(-self.body.angle), self.rect.centerx, self.rect.centery)
        self.rotated_image.set_colorkey((0,0,0,0))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.draw(screen)

    def change_type(self, override = None):
        if not self.static or override == "static":
            self.body.body_type = pymunk.Body.STATIC
            self.static = True
        elif override == "dynamic":
            self.body.body_type = pymunk.Body.DYNAMIC
            self.static = False
        else:
            self.body.body_type = pymunk.Body.DYNAMIC
            self.static = False

    def draw(self, screen):
        screen.blit(self.rotated_image, (self.rect.x, self.rect.y))

class physramp(physbox):
    def __init__(self,topleft, angle, space, image = basebox_img, static = False, mass = 1, friction = 0.5):
        super().__init__(topleft[0], topleft[1], space, image, static, mass, friction)
        self.body.angle = angle
        pymunk.Space.reindex_shapes_for_body(space, self.body)
        print(get_vertices(self.poly))
        self.rect.centerx = self.body.position[0]
        self.rect.centery = self.body.position[1]
        self.rotated_image, self.rect = rot_center(self.image, math.degrees(-self.body.angle), self.rect.centerx,
                                                   self.rect.centery)
        self.rotated_image.set_colorkey((0, 0, 0, 0))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.draw(screen)

    def update(self, screen, space):
        #Rotates an image and changes the rect accordingly if dynamic
        self.draw(screen)

class player_block(physbox):
    def __init__(self, x, y, space, image = basebox_img.convert_alpha(), mass = 3, friction = 0.5, static = True):
        super().__init__(x, y, space,image, static, mass, friction)
        #pygame variables
        if self.static:
            self.image.fill((0, 25, 49))
        else:
            self.image.fill((1, 24, 1))

    def keyboard_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.body.apply_impulse_at_world_point((30, 0), (self.body.position[0]+10, self.body.position[1]))
        if keys[pygame.K_a]:
            self.body.apply_impulse_at_world_point((-30, 0), (self.body.position[0]-10, self.body.position[1]))
        if keys[pygame.K_s]:
            self.body.apply_impulse_at_world_point((0, 50), (self.body.position[0], self.body.position[1]+10))

    def jump(self, level_group):
        for collide_rect in self.rect.collidelistall(level_group):
            try:
                collision_points = pixel_perfect_collision(self.mask, level_group[collide_rect].mask,
                                               (level_group[collide_rect].rect.topleft[0]-self.rect.topleft[0], level_group[collide_rect].rect.topleft[1]-self.rect.topleft[1]))
            except:
                collision_points = None
            if collision_points is not None:
                for x in range(collision_points.get_size()[0]-4):
                    if collision_points.get_at((x+2, collision_points.get_size()[1]-1)):
                        #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA I SPENT TWO HOURS DEBUGGING NOTHING AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                        self.body.apply_impulse_at_world_point((0, -908), (self.body.position[0], self.body.position[1] - 10))
                        return True

    def update(self, screen, space, movement):
        super(player_block, self).update(screen, space)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        if movement:
            self.keyboard_press()


    def change_type(self):
        if not self.static:
            self.body.body_type = pymunk.Body.STATIC
            self.static = True
            self.image.fill((0, 25, 49))
        else:
            self.body.body_type = pymunk.Body.DYNAMIC
            self.static = False
            self.image.fill((1, 24, 1))

class circle_push():
    def __init__(self, pos, space):
        self.radius = 100
        self.rect = pygame.Rect(0, 0, self.radius, self.radius)
        # Pymunk variables
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 100, 100),
                                body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        space.add(self.body, self.shape)
        self.body.position = (pos[0], 1024)
        space.reindex_shapes_for_body(self.body)
        self.body.velocity = (0, -1000)
        self.body.death_point = (pos[0], 774)
        self.alive = True

    def update(self, space, screen):
        if self.alive:
            self.rect.center = self.body.position
            if self.body.position[1] <= self.body.death_point[1]:
                self.body.velocity = (0, 1000)
            if self.body.position[1] >= 1024 + self.radius:
                self.alive = False
            pygame.draw.circle(screen, "black", self.rect.center, self.radius)
        else:
            space.remove(self.body, self.shape)

class event_rect():
    def __init__(self, pos, size):
        self.image = pygame.surface.Surface((size), flags = pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)
        self.image.fill((0,0,0, 100))
        self.rect = pygame.FRect(pos, size)

    def update(self, screen, player):
        if self.rect.colliderect(player.rect):
            if pixel_perfect_collision(self.mask, player.mask,
                                           (player.rect.topleft[0]-self.rect.topleft[0], player.rect.topleft[1]-self.rect.topleft[1])):
                return True
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class kill_rect(event_rect):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.type = "kill"
        self.image.fill((254, 6, 6))

class win_rect(event_rect):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.type = "win"
        self.image.fill((31, 254, 6))
