import os
import numpy as np

theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5

screen_width = 50
screen_height = 50
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))


def print_chararray(char_arr):
    pretty = str(b"x".join([b"".join(s) for s in char_arr]))[2:-2]
    return pretty.replace("x", "\n").replace("y", " ")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def calc_cos_n_sin(value):
    return np.cos(value), np.sin(value)


def calc_luminance(cos_a, cos_b, cos_phi, cos_theta, sin_a, sin_b, sin_phi, sin_theta):
    return cos_phi * cos_theta * sin_b - cos_a * cos_theta * sin_phi - sin_a * sin_theta * cos_b * (
            cos_a * sin_theta - cos_theta * sin_a * sin_phi)


def calc_3d_coordinates(circle_x, circle_y, cos_a, cos_b, cos_phi, sin_a, sin_b, sin_phi):
    x = circle_x * (cos_b * cos_phi + sin_a * sin_b * sin_phi) - circle_y * cos_a * sin_b
    y = circle_x * (sin_b * cos_phi - sin_a * cos_b * sin_phi) + circle_y * cos_a * cos_b
    z = K2 + cos_a * circle_x * sin_phi + circle_y * sin_a
    return x, y, z


def render_frame(a, b):
    cos_a, sin_a = calc_cos_n_sin(a)
    cos_b, sin_b = calc_cos_n_sin(b)

    output = np.chararray((screen_width, screen_height))
    output[:] = 'y'
    z_buffer = np.zeros((screen_width, screen_height))

    for theta in np.arange(0, 2 * np.pi, theta_spacing):
        cos_theta, sin_theta = calc_cos_n_sin(theta)

        for phi in np.arange(0, 2 * np.pi, phi_spacing):
            cos_phi, sin_phi = calc_cos_n_sin(phi)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta

            x, y, z = calc_3d_coordinates(circle_x, circle_y, cos_a, cos_b, cos_phi, sin_a, sin_b, sin_phi)
            ooz = 1 / z

            xp, yp = calc_screen_coordinates(ooz, x, y)

            L = calc_luminance(cos_a, cos_b, cos_phi, cos_theta, sin_a, sin_b, sin_phi, sin_theta)

            if L > 0:
                if ooz > z_buffer[xp, yp]:
                    z_buffer[xp, yp] = ooz
                    luminance_index = L * 8
                    output[xp, yp] = ".,-~:;=!*#$@"[int(luminance_index)]

    clear_screen()
    print(print_chararray(output))


def calc_screen_coordinates(ooz, x, y):
    xp = int(screen_width / 2 + K1 * ooz * x)
    yp = int(screen_height / 2 + K1 * ooz * y)
    return xp, yp


while True:
    for angle in np.arange(0, np.pi, np.pi / 12):
        render_frame(np.pi / 2 + angle, np.pi / 2 + angle / 2)
