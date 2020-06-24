import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

def trans_x(v):
    return np.array([
        [1, 0, v],
        [0, 1, 0],
        [0, 0, 1]
    ])

def rotate(v):
    return np.array([
        [np.cos(v), -np.sin(v), 0],
        [np.sin(v), np.cos(v), 0],
        [0, 0, 1]
    ])

def scale(v):
    return np.array([
        [v, 0, 0],
        [0, v, 0],
        [0, 0, 1]
    ])

def render(T):     
    glClear(GL_COLOR_BUFFER_BIT)     
    glLoadIdentity()     # draw cooridnate
    glBegin(GL_LINES)     
    glColor3ub(255, 0, 0)     
    glVertex2fv(np.array([0.,0.]))     
    glVertex2fv(np.array([1.,0.]))     
    glColor3ub(0, 255, 0)     
    glVertex2fv(np.array([0.,0.]))     
    glVertex2fv(np.array([0.,1.]))     
    glEnd()     # draw triangle 
    glBegin(GL_TRIANGLES)     
    glColor3ub(255, 255, 255)     
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )     
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )     
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )     
    glEnd()

def key_callback(window, key, scanconde, action, mods):
    global gComposedM
    if key == glfw.KEY_Q:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = trans_x(-0.1) @ gComposedM

    elif key == glfw.KEY_E:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = trans_x(0.1) @ gComposedM

    elif key == glfw.KEY_A:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = gComposedM @ rotate(np.math.pi * (10) / 180)
            
    elif key == glfw.KEY_D:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = gComposedM @ rotate(np.math.pi * (-10) / 180)
    
    elif key == glfw.KEY_1:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])

    elif key == glfw.KEY_W:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = gComposedM @ scale(0.9)

    elif key == glfw.KEY_S:
        if action == glfw.PRESS or action == glfw.REPEAT:
            gComposedM = rotate(np.math.pi * (10) / 180) @ gComposedM 

def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        480, 480, "CG_weekly_practice_04_", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()