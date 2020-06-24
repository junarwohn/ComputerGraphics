import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def drawFrame(): 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([0.,1.,0.])) 
    glColor3ub(0, 0, 255) 
    glVertex3fv(np.array([0.,0.,0])) 
    glVertex3fv(np.array([0.,0.,1.])) 
    glEnd()

def drawUnitCube(): 
    glBegin(GL_QUADS) 
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    
    glVertex3f( 0.5,-0.5, 0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f( 0.5,-0.5,-0.5)

    glVertex3f( 0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5) 
    glVertex3f( 0.5,-0.5, 0.5) 
    glVertex3f( 0.5,-0.5,-0.5) 
    glEnd()

def drawCubeArray(): 
    for i in range(5): 
        for j in range(5): 
            for k in range(5): 
                glPushMatrix() 
                glTranslatef(i,j,-k-1) 
                glScalef(.5,.5,.5) 
                drawUnitCube() 
                glPopMatrix()

def myOrtho(left, right, bottom, top, near, far):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    orthoM =  np.array([
        [2 / (right - left), 0, 0,  (right + left) / (right - left)],
        [0, 2 / (top - bottom), 0,  (top + bottom) / (top - bottom)],
        [0, 0, -2 / (far - near),  (far + near) / (far - near)],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(orthoM.T)

def myLookAt(eye, at, up):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    vb = at - eye
    vu = np.cross(vb, up)
    vu = vu / np.sqrt(vu @ vu)
    vv = np.cross(vu, vb)
    vv = vv / np.sqrt(vv @ vv)
    vw = np.cross(vu, vv)
    vw = vw / np.sqrt(vw @ vw)
    viewM = np.array([
        np.concatenate((vu, [-1 * vu@eye])),
        np.concatenate((vv, [-1 * vv@eye])),
        np.concatenate((vw, [-1 * vw@eye])),
        [0, 0, 0, 1]
    ])
    glMultMatrixf(viewM.T)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    gluPerspective(45, 1, 1,10) 

    glRotatef(-45, 0, 1, 0)
    glRotatef(-36.264, -1, 0, 1)
    glTranslatef(-3, -3, -3)
 
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCubeArray()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(
        480, 480, "CG_weekly_practice_05-2_", None, None)

    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
