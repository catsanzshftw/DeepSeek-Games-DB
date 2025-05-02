from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title="Minecraft Clone", fullscreen=False)

# Set target FPS
window.fps_counter.enabled = True
window.fps_counter.position = (0, 0)
window.fps_counter.scale = 2

class Voxel(Button):
    def __init__(self, position=(0,0,0), color=color.green):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=color,
            highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal, color=color.random_color())
            if key == 'right mouse down':
                destroy(self)

class Player(FirstPersonController):
    def __init__(self):
        super().__init__()
        self.cursor = Entity(
            parent=camera.ui,
            model='quad',
            color=color.red,
            scale=0.008,
            rotation_z=45
        )

player = Player()

# Generate terrain
for z in range(-20,20):
    for x in range(-20,20):
        for y in range(0,3):
            if y == 0:
                voxel = Voxel(position=(x,y,z), color=color.brown)
            elif y == 1:
                voxel = Voxel(position=(x,y,z), color=color.green)
            else:
                voxel = Voxel(position=(x,y,z), color=color.gray)

# Sky
Sky()

# Hand
hand = Entity(
    parent=camera.ui,
    model='cube',
    color=color.white,
    scale=(0.1,0.2,0.1),
    rotation=(10,10,10),
    position=(0.4,-0.4,0)
)

def update():
    if held_keys['escape']:
        application.quit()

app.run()
