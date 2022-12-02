import random

import wrap

wrap.add_sprite_dir("sprite")

wrap.world.create_world(800, 600)
wrap.world.set_back_color(255, 255, 255)

water = wrap.sprite.add("aqua", 400, 300, "water")
wrap.sprite.set_size(water, 800, 400)
wrap.sprite.move_bottom_to(water, 600)

fishes = []
granulas = []

food = wrap.sprite.add("aqua", 730, 80, "fishfood")
molot = wrap.sprite.add("aqua", 640, 80, "molot")

mode = "empty" #food

def add_fish(name):
    f = wrap.sprite.add("fish", random.randint(100, 700), random.randint(350, 550), name)
    wrap.sprite.set_reverse_x(f, random.choice([True, False]))
    angle = wrap.sprite.get_angle(f)
    wrap.sprite.set_angle(f, angle+random.randint(-25, 25))

    perc = random.randint(10, 30)
    wrap.sprite.set_size_percent(f, perc, perc)
    fishes.append(f)


def add_granula(x, y):
    g = wrap.sprite.add("aqua", x, y, "fish food granula")
    wrap.sprite.set_angle(g, random.randint(0, 360))
    perc = random.randint(10, 30)
    wrap.sprite.set_size_percent(g, perc, perc)
    granulas.append(g)

def place():
    wrap.sprite.move_to(food, 730, 80)
    wrap.sprite.set_angle(food, 90)
    wrap.sprite.move_to(molot, 640, 80)
    wrap.sprite.set_angle(molot, 90)

@wrap.always(25)
def swim():
    for f in fishes:
        if len(granulas)==0:
            wrap.sprite.move_at_angle_dir(f, 3)
        else:
            g = granulas[len(granulas)-1]
            if wrap.sprite.get_x(g)>wrap.sprite.get_x(f):
                wrap.sprite.set_reverse_x(f, False)
            else:
                wrap.sprite.set_reverse_x(f, True)
            wrap.sprite.set_angle_to_point(f, wrap.sprite.get_x(g), wrap.sprite.get_y(g))
            wrap.sprite.move_at_angle_point(f, wrap.sprite.get_x(g), wrap.sprite.get_y(g), 6)

        g = wrap.sprite.is_collide_any_sprite(f, granulas)
        if g != None:
            granulas.remove(g)
            wrap.sprite.remove(g)
            wrap.sprite.set_width_proportionally(f, wrap.sprite.get_width(f)+1)
            print(wrap.sprite.get_width_percent(f))
            if wrap.sprite.get_width_percent(f)>120:
                wrap.sprite.set_size_percent(f, 80, 80)
                add_fish(random.choice(all_fishes))

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
            wrap.sprite.move_bottom_to(f, 600)
            if wrap.sprite.get_reverse_x(f):
                wrap.sprite.set_angle(f, random.randint(-100, -65))
            else:
                wrap.sprite.set_angle(f, random.randint(65, 100))

        if top<190:
            wrap.sprite.move_top_to(f, 190)
            if wrap.sprite.get_reverse_x(f):
                wrap.sprite.set_angle(f, random.randint(-115, -100))
            else:
                wrap.sprite.set_angle(f, random.randint(100, 115))

@wrap.always(25)
def fly():
    for g in granulas:
        bottom = wrap.sprite.get_bottom(g)
        if bottom <200:
            wrap.sprite.move(g, 0, 6)
        if bottom<600:
            wrap.sprite.move(g, 0, random.randint(1, 3))

        if bottom>=600:
            wrap.sprite.move_bottom_to(g, 600)
            granulas.remove(g)


@wrap.on_mouse_down(wrap.BUTTON_MIDDLE)
def click(pos_x, pos_y):
    if mode=="food":
        wrap.sprite.set_angle(food, -135)
        for i in range(1, 100):
            add_granula(wrap.sprite.get_right(food)+random.randint(-30, 30), wrap.sprite.get_bottom(food)+random.randint(1, 10))


@wrap.on_mouse_down(wrap.BUTTON_LEFT)
def click(pos_x, pos_y):
    global mode
    if mode!="food" and wrap.sprite.is_collide_point(food, pos_x, pos_y):
        place()
        mode="food"
        return

    if mode != "molot" and wrap.sprite.is_collide_point(molot, pos_x, pos_y):
        place()
        mode = "molot"
        return

    if mode=="food":
        wrap.sprite.set_angle(food, -135)
        add_granula(wrap.sprite.get_right(food), wrap.sprite.get_bottom(food))
        add_granula(wrap.sprite.get_right(food)-10, wrap.sprite.get_bottom(food))
        add_granula(wrap.sprite.get_right(food), wrap.sprite.get_bottom(food)-10)

    if mode == "molot":
        wrap.sprite.set_angle(molot, -15)
        for f in fishes:
            wrap.sprite.set_angle(f, random.randint(0, 360))


@wrap.on_key_down(wrap.K_ESCAPE)
def nomode():
    global mode
    place()
    mode="empty"

@wrap.on_mouse_up(wrap.BUTTON_LEFT, wrap.BUTTON_MIDDLE)
def unclick():
    if mode=="food":
        wrap.sprite.set_angle(food, 90)
    if mode=="molot":
        wrap.sprite.set_angle(molot, 90)

@wrap.on_mouse_move
def motion(pos_x, pos_y):
    if mode=="food":
        wrap.sprite.move_to(food, pos_x, pos_y)
        bottom = wrap.sprite.get_bottom(food)
        if bottom>200:
            wrap.sprite.move_bottom_to(food, 200)

    if mode=="molot":
        wrap.sprite.move_to(molot, pos_x, pos_y)


all_fishes = ["fish blue1", "fish colored1", "fish colored2", "fish colored3"]
add_fish(random.choice(all_fishes))

import wrap_py
wrap_py.app.start()