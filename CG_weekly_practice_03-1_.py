import glfw
from OpenGL.GL import *
import numpy as np

PRIMITIVE_TYPE = 2

def render(points):
    # Clear color buffer
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(PRIMITIVE_TYPE)
    glColor3ub(255, 255, 255)
    for i in points:
        glVertex2fv(i)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    key -= glfw.KEY_0 
    global PRIMITIVE_TYPE 
    if 0 <= key <= 9:
        PRIMITIVE_TYPE = (9 + key) % 10
    else:
        return


def main():
    v = np.linspace(0, 360, 13)[:-1]
    points = np.array((np.cos(v * np.pi/180), np.sin(v * np.pi/180))).T

    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "CG_weekly_practice_03-1_", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(points)
        glfw.swap_buffers(window)

    glfw.terminate()
    

if __name__ == "__main__":
    main()
