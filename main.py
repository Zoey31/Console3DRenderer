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


def render_frame(A, B):
    cos_A = np.cos(A)
    sin_A = np.sin(A)
    cos_B = np.cos(B)
    sin_B = np.sin(B)

    output = np.chararray((screen_width, screen_height))
    output[:] = 'y'
    z_buffer = np.zeros((screen_width, screen_height))

    for theta in np.arange(0, 2 * np.pi, theta_spacing):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        for phi in np.arange(0, 2 * np.pi, phi_spacing):
            cos_phi = np.cos(phi)
            sin_phi = np.sin(phi)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta

            x = circle_x * (cos_B * cos_phi + sin_A * sin_B * sin_phi) - circle_y * cos_A * sin_B
            y = circle_x * (sin_B * cos_phi - sin_A * cos_B * sin_phi) + circle_y * cos_A * cos_B
            z = K2 + cos_A * circle_x * sin_phi + circle_y * sin_A
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 + K1 * ooz * y)

            L = cos_phi * cos_theta * sin_B - cos_A * cos_theta * sin_phi - sin_A * sin_theta * cos_B * (
                    cos_A * sin_theta - cos_theta * sin_A * sin_phi)

            if L > 0:
                if ooz > z_buffer[xp,yp]:
                    z_buffer[xp, yp] = ooz
                    luminance_index = L * 8
                    output[xp, yp] = ".,-~:;=!*#$@"[int(luminance_index)]

    clear_screen()
    print(print_chararray(output))


while True:
    for angle in np.arange(0, np.pi, np.pi/12):
        render_frame(np.pi/2 + angle, np.pi/2 + angle/2)
