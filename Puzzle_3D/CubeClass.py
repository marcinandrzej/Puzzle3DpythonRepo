from OpenGL.GL import *

class CubeClass():


    def __init__(self, id_row, id_col, offset):

        self.rotation = 0
        self.rotation_change = 0
        self.rotation_current = 0

        self.x = (-2*offset + id_col*offset)
        self.y = (2*offset - id_row*offset)
        self.z = 0

        self.id_row = id_row
        self.id_col = id_col

        self.tex_x_begin = (self.x + (2.0 * offset))/(5.0 * offset)
        self.tex_x_end = (self.x + (2.0 * offset))/(5.0 * offset) + 0.2
        self.tex_y_begin = (self.y + (2.0 * offset))/(5.0 * offset)
        self.tex_y_end = (self.y + (2.0 * offset))/(5.0 * offset) + 0.2

        self.active_color = 0.2
        self.color = (1 * self.active_color, 1 * self.active_color, 1 * self.active_color)

        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )

        self.faces = (
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (4, 5, 1, 0),
            (6, 7, 5, 4),
            (1, 5, 7, 2),
            (4, 0 , 3, 6)
        )

    def colorUpdate(self):
        self.color = (1 * self.active_color, 1 * self.active_color, 1 * self.active_color)

    def rotateRight(self):
        self.rotation = (self.rotation + 90)%360
        self.rotation_change = 10

    def rotateLeft(self):
        self.rotation = (self.rotation - 90)%360
        self.rotation_change = -10

    def push(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def activate(self):
        self.active_color = 1
        self.colorUpdate()

    def deactivate(self):
        self.active_color = 0.2
        self.colorUpdate()

    def activateNeighbour(self):
        self.active_color = 0.55
        self.colorUpdate()

    def draw(self, texture):

        glPushMatrix()
        glTranslate(self.x,self.y, self.z)
        if self.rotation_current != self.rotation:
            self.rotation_current = (self.rotation_current + self.rotation_change)%360
        glRotatef(self.rotation_current, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            glColor3fv(self.color)
            glTexCoord2f(self.tex_x_begin, self.tex_y_begin);
            glVertex3fv(self.vertices[face[0]])
            glTexCoord2f(self.tex_x_begin, self.tex_y_end);
            glVertex3fv(self.vertices[face[1]])
            glTexCoord2f(self.tex_x_end, self.tex_y_begin);
            glVertex3fv(self.vertices[face[3]])

            glTexCoord2f(self.tex_x_end, self.tex_y_end);
            glVertex3fv(self.vertices[face[2]])
            glTexCoord2f(self.tex_x_end, self.tex_y_begin);
            glVertex3fv(self.vertices[face[3]])
            glTexCoord2f(self.tex_x_begin, self.tex_y_end);
            glVertex3fv(self.vertices[face[1]])
        glEnd()
        glPopMatrix()