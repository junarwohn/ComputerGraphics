import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    # Clear color buffer
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(T @ np.array([0.0, 0.5]))
    glVertex2fv(T @ np.array([0.0, 0.0]))
    glVertex2fv(T @ np.array([0.5, 0.0]))
    glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 640, "2D Trans", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        # non uniform scale
        s = np.sin(t)
        US = np.array([[s, 0.],
                    [0., s]])

        # rotate
        th = t
        R = np.array([
            [np.cos(th), -np.sin(th)],
            [np.sin(th), np.cos(th)]
        ])

        # shear
        a = np.sin(t)
        S = np.array([
            [1., a],
            [0., 1.]
        ])

        # identity matrix
        I = np.identity(2)

        #render(R @ S)
        render(S @ R)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

