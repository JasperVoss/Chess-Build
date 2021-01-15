import math
import time
import motors
import RPi.GPIO as gpio

magnet_pin = 4
sleeptime = 0.0001

gpio.setmode(gpio.BCM)
gpio.setup(magnet_pin, gpio.OUT)


def magnet_on():
    gpio.output(magnet_pin, 1)


def magnet_off():
    gpio.output(magnet_pin, 0)


def get_board_vars():
    file = open("board_vars.txt", 'r')
    text = file.read()
    file.close()
    var = []
    curr_string = ""
    for v in text:
        if v == "\n":
            var.append(curr_string)
            curr_string = ""
        else:
            curr_string = curr_string + v
    for i in range(len(var)):
        var[i] = float(var[i])

    return var


def get_curr_step():
    file = open("curr_steps.txt", "r")
    steps = ["", "", "", ""]
    index = 0

    for s in file.read():
        if s == "\n":
            index += 1
        else:
            steps[index] = steps[index] + s

    file.close()
    for i in range(4):
        steps[i] = int(steps[i])

    return steps


def save_curr_steps():
    steps = [a_motors.get_steps()[0], a_motors.get_steps()[1],
                                b_motors.get_steps()[0], b_motors.get_steps()[1]]
    file = open("curr_steps.txt", "w")
    for s in steps:
        file.write(str(s)+"\n")
    file.close()


def hard_calibrate():
    pass


def calibrate():
    file = open("calibration.txt", "r")
    steps = ["", "", "", "", "", ""]
    index = 0
    for s in file.read():
        if s == "\n":
            index += 1
        else:
            steps[index] = steps[index] + s
    file.close()
    for i in range(6):
        steps[i] = int(steps[i])

    final_pos = [steps[4], steps[5]]

    move([580, 30])
    for i in range(4):
        off(i)
    manual(3, -150)
    for i in range(3):
        manual(i, -8)
    save_steps(get_radii(final_pos))
    move([500, 100])

    for i in range(4):
        manual(i, steps[i])


a_motors = motors.Motor('A')
b_motors = motors.Motor('B')

current_step = get_curr_step()
a_motors.set_curr_step(current_step[0], current_step[1])
b_motors.set_curr_step(current_step[2], current_step[3])

board_vars = get_board_vars()
width = board_vars[0]
height = board_vars[1]

mm_per_step_0 = board_vars[2]
mm_per_step_1 = board_vars[3]
mm_per_step_2 = board_vars[4]
mm_per_step_3 = board_vars[5]

corner_coords = [[board_vars[6], board_vars[7]], [board_vars[8], board_vars[9]], [board_vars[10], board_vars[11]], [
    board_vars[12], board_vars[13]]]  # coordinates of the center of each corner square
overshoot = board_vars[14]

square_coords = [[[0, 0] for _ in range(10)] for _ in range(8)]

for i in range(len(square_coords)):
    square_coords[i][0][0] = corner_coords[1][0] - \
        i*(corner_coords[1][0]-corner_coords[0][0])/7
    square_coords[i][0][1] = corner_coords[1][1] - \
        i*(corner_coords[1][1]-corner_coords[0][1])/7

    square_coords[i][9][0] = corner_coords[2][0] - \
        i*(corner_coords[2][0]-corner_coords[3][0])/7
    square_coords[i][9][1] = corner_coords[2][1] - \
        i*(corner_coords[2][1]-corner_coords[3][1])/7

    for j in range(len(square_coords[i])):
        square_coords[i][j][0] = round(
            square_coords[i][0][0]+j*(square_coords[i][9][0]-square_coords[i][0][0])/9, 2)
        square_coords[i][j][1] = round(
            square_coords[i][0][1]+j*(square_coords[i][9][1]-square_coords[i][0][1])/9, 2)


def move_piece(i, j):
    steps = get_steps()

    y0 = ((steps[0]*mm_per_step_0)**2 -
          (steps[1]*mm_per_step_1)**2+height**2)/2/height
    x0 = math.sqrt((mm_per_step_0*steps[0])**2-y0**2)

    if i%1 == 0:
        if j%1 == 0:
            xfinal = square_coords[i][j][0]
            yfinal = square_coords[i][j][1]
        else:
            xfinal = (square_coords[i][int(j+.5)][0]+square_coords[i][int(j-.5)][0])/2
            yfinal = square_coords[i][int(j-.5)][1]
    else:
        if j%1 == 0:
            xfinal = square_coords[int(i-.5)][j][0]
            yfinal = (square_coords[int(i+.5)][j][1]+square_coords[int(i-.5)][j][1])/2
        else:
            xfinal = (square_coords[int(i-.5)][int(j+.5)][0]+square_coords[int(i-.5)][int(j-.5)][0])/2
            yfinal = (square_coords[int(i+.5)][int(j-.5)][1]+square_coords[int(i-.5)][int(j-.5)][1])/2

    dx = xfinal-x0
    dy = yfinal-y0

    if dx != 0:
        x_over = math.copysign(math.sqrt(overshoot**2/((dy**2)/(dx**2)+1)), dx)
    else:
        x_over = 0
    y_over = math.copysign(math.sqrt(overshoot**2-x_over**2), dy)
    move([xfinal+x_over, yfinal+y_over])


def move_square(i, j):
    if i%1 == 0:
        if j%1 == 0:
            move(square_coords[i][j])
        else:
            move([(square_coords[i][int(j+.5)][0]+square_coords[i][int(j-.5)][0])/2, square_coords[i][int(j-.5)][1]])
    else:
        if j%1 == 0:
            move([square_coords[int(i-.5)][j][0], (square_coords[int(i+.5)][j][1]+square_coords[int(i-.5)][j][1])/2])
        else:
            move([(square_coords[int(i-.5)][int(j+.5)][0]+square_coords[int(i-.5)][int(j-.5)][0])/2, (square_coords[int(i+.5)][int(j-.5)][1]+square_coords[int(i-.5)][int(j-.5)][1])/2])




def tension():
    num_steps = 4
    for i in range(num_steps):
        for j in range(4):
            manual(j, -1)


def release_tension():
    num_steps = 4
    for i in range(num_steps):
        for j in range(4):
            manual(j, 1)


def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)


def get_radii(pos):
    return [
    round(distance([0, 0], pos)/mm_per_step_0),
    round(distance([0, height], pos)/mm_per_step_1),
    round(distance([width, height], pos)/mm_per_step_2),
    round(distance([width, 0], pos)/mm_per_step_3)
    ]


def get_position(radii):
    y = (radii[0]**2+height**2-radii[1]**2)/(2*height)
    x = math.sqrt(radii[0]**2-y**2)
    return [x, y]


def get_steps():
    step_file = open("steps.txt", "r")
    steps = ["", "", "", ""]
    index = 0

    for s in step_file.read():
        if s == "\n":
            index += 1
        else:
            steps[index] = steps[index] + s

    step_file.close()
    for i in range(4):
        steps[i] = int(steps[i])

    return steps


def save_steps(steps):
    step_file = open("steps.txt", "w")
    for s in steps:
        step_file.write(str(s)+"\n")
    step_file.close()


def manual(motor, steps):
    if motor == 0:
        for i in range(abs(steps)):
            a_motors.move_step0(abs(steps)/steps)
            time.sleep(.004)
    if motor == 1:
        for i in range(abs(steps)):
            a_motors.move_step1(abs(steps)/steps)
            time.sleep(.004)
    if motor == 2:
        for i in range(abs(steps)):
            b_motors.move_step0(abs(steps)/steps)  # was -abs
            time.sleep(.004)
    if motor == 3:
        for i in range(abs(steps)):
            b_motors.move_step1(abs(steps)/steps)
            time.sleep(.004)
    save_curr_steps()


def off(motor):
    if motor == 0:
        a_motors.off0()
    if motor == 1:
        a_motors.off1()
    if motor == 2:
        b_motors.off0()
    if motor == 3:
        b_motors.off1()


def on(motor):
    if motor == 0:
        a_motors.on0()
    if motor == 1:
        a_motors.on1()
    if motor == 2:
        b_motors.on0()
    if motor == 3:
        b_motors.on1()


def move(coords):
    steps = get_steps()
    final = [
    round(distance([0, 0], coords)/mm_per_step_0),
    round(distance([0, height], coords)/mm_per_step_1),
    round(distance([width, height], coords)/mm_per_step_2),
    round(distance([width, 0], coords)/mm_per_step_3),
    ]

    y0 = ((steps[0]*mm_per_step_0)**2 - (steps[1]*mm_per_step_1)**2+height**2)/2/height
    x0 = math.sqrt((mm_per_step_0*steps[0])**2-y0**2)

    dx = coords[0]-x0
    dy = coords[1]-y0

    dsteps = [final[i]-steps[i] for i in range(4)]  # change in steps

    most_steps_motor = 0
    most_steps = 0
    for i in range(4):
        if dsteps[i] > most_steps:
            most_steps = dsteps[i]
            most_steps_motor = i

    num_targets = most_steps
    target_coords = []

    for i in range(num_targets):
        target_coords.append([
            round(x0+dx*i/num_targets, 2),
            round(y0+dy*i/num_targets, 2)
            ])
    target_steps = []
    for t in target_coords:
        target_steps.append(get_radii(t))
    target_steps.append(final)

    for t in target_steps:
        d0 = t[0]-steps[0]
        d1 = t[1]-steps[1]
        d2 = t[2]-steps[2]
        d3 = t[3]-steps[3]

        for i in range(abs(d0)):
            a_motors.move_step0(abs(d0)/d0)
            steps[0] += int(abs(d0)/d0)
            time.sleep(sleeptime)
        for i in range(abs(d1)):
            a_motors.move_step1(abs(d1)/d1)
            steps[1] += int(abs(d1)/d1)
            time.sleep(sleeptime)
        for i in range(abs(d2)):
            b_motors.move_step0(abs(d2)/d2)
            steps[2] += int(abs(d2)/d2)
            time.sleep(sleeptime)
        for i in range(abs(d3)):
            b_motors.move_step1(abs(d3)/d3)
            steps[3] += int(abs(d3)/d3)
            time.sleep(sleeptime)

    save_steps(steps)
    save_curr_steps()

