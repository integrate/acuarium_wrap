import random

import wrap

wrap.add_sprite_dir("sprite")

wrap.world.create_world(800, 600)
wrap.world.set_back_color(255, 255, 255)

water = wrap.sprite.add("aqua", 400, 300, "water")
wrap.sprite.set_size(water, 800, 400)
wrap.sprite.move_bottom_to(water, 600)

fishes = []
def add_fish(name):
    f = wrap.sprite.add("fish", random.randint(100, 700), random.randint(350, 550), name)
    wrap.sprite.set_reverse_x(f, random.choice([True, False]))
    angle = wrap.sprite.get_angle(f)
    wrap.sprite.set_angle(f, angle+random.randint(-25, 25))
    fishes.append(f)


@wrap.always(25)
def swim():
    for f in fishes:
        wrap.sprite.move_at_angle_dir(f, 8)
        right = wrap.sprite.get_right(f)
        left = wrap.sprite.get_left(f)
        if right>800:
            wrap.sprite.set_reverse_x(f, True)
            wrap.sprite.move_right_to(f, 800)
            wrap.sprite.set_angle(f, random.randint(-115, -65))
        elif left<0:
            wrap.sprite.set_reverse_x(f,False)
            wrap.sprite.move_left_to(f, 0)
            wrap.sprite.set_angle(f, random.randint(65, 115))

        top = wrap.sprite.get_top(f)
        bottom = wrap.sprite.get_bottom(f)
        if bottom>600:
            if wrap.sprite.get_reverse_x(f):
                wrap.sprite.set_angle(f, random.randint(-90, -65))
            else:
                wrap.sprite.set_angle(f, random.randint(65, 90))

        if top<180:
            if wrap.sprite.get_reverse_x(f):
                wrap.sprite.set_angle(f, random.randint(-115, -90))
            else:
                wrap.sprite.set_angle(f, random.randint(90, 115))


add_fish(random.choice(["fish blue1", "fish colored1", "fish colored2", "fish colored3"]))