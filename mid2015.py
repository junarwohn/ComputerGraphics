import glfw
from OpenGL.GL import *
import numpy as np

PRIMITIVE_TYPE = 2


def render(points):
    # Clear color buffer
    glOrtho(-1, 1, -1, 1, -1, 1)
    glViewport(0, 0, 300, 300)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3ub(255, 255, 255)
    glLoadIdentity()
    glTranslate(0.5, -0.5, 0)
    glRotatef(45, 0, 0, 1)
    w = np.sqrt(2*0.5*0.5) * 0.5
    glBegin(GL_POLYGON)
    glVertex3f(w,w,0)
    glVertex3f(-w,w,0)
    glVertex3f(-w,-w,0)
    glVertex3f(w,-w,0)

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
    points = np.array((np.cos(v * np.pi / 180), np.sin(v * np.pi / 180))).T

    if not glfw.init():
        return

    window = glfw.create_window(300, 300, "CG_weekly_practice_03-1_", None, None)

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
