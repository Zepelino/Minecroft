from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grass_tex = load_texture('assets/Grass.png')
wood_tex = load_texture('assets/wood.png')

selected = 1

punch_sound = Audio('assets/punch_sound.wav', loop = False, autoplay = False)

def update():
    global selected
    if held_keys['1']: selected = 1
    elif held_keys['2']: selected = 2

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.normal()

class Voxel(Button):
    def __init__(self, pos = (0,0,0), tex = grass_tex):
        super().__init__(
            parent = scene,
            position = pos,
            model = 'assets/CUBE',
            texture = tex,
            color = color.color(0,0, random.uniform(0.9,1)),
            highlight_color = color.light_gray,
        )
    
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                tx = grass_tex
                if selected == 2:
                    tx = wood_tex
                voxel = Voxel(pos = self.position + mouse.normal, tex = tx)
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = 'sky_box.png',
            scale = 150,
            double_sided = True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/Hand',
            texture = 'assets/hand.png',
            rotation = Vec3(-50, -16, 2),
            position = Vec2(0.6, -0.6)
        )
    
    def active(self):
        self.rotation = Vec3(-30, -16, 2)
        self.position = Vec2(0.55, -0.55)
    
    def normal(self):
        self.rotation = Vec3(-50, -16, 2)
        self.position = Vec2(0.6, -0.6)

for x in range(20):
    for z in range(20):
        voxel = Voxel(pos = (x,0,z))

person = FirstPersonController()

sky = Sky()

hand = Hand()

app.run()