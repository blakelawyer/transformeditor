import numpy as np
from kivy.app import App
from kivy.core.image import Texture
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import random
import cv2
import os

image = ""
img_bool = False
theyta = 0
ex = 0
why = 0
ex_2 = 0
why_2 = 0
spin_mode = False
spin_dir = []


class TransformEditorGrid(GridLayout):

    def random_rotation(self, theta, point, width, height):
        global ex
        global why
        global ex_2
        global why_2
        global theyta

        x = point[0]
        y = point[1]

        px = width // 2
        py = height // 2

        x_y = np.matrix([[x - px], [y - py]])

        rotation = np.matrix([[np.cos(np.radians(theta)), -np.sin(np.radians(theta))],
                            [np.sin(np.radians(theta)), np.cos(np.radians(theta))]])

        new_point = np.matmul(rotation, x_y)

        ex = x
        why = y
        ex_2 = int(new_point[0] + px)
        why_2 = int(new_point[1] + py)
        theyta = theta
        self.ids.matrix_2.text = str(ex)

        return int(new_point[0] + px), int(new_point[1] + py)

    def import_image(self):
        self.ids.filechooser.size_hint[0] = 1
        self.ids.filechooser.size_hint[1] = 1
        self.ids.my_image.size_hint[0] = 0
        self.ids.my_image.size_hint[1] = 0

    def selected(self, filename):
        global image
        global img_bool
        self.ids.my_image.source = filename[0]
        self.ids.my_image.size_hint[0] = 1
        self.ids.my_image.size_hint[1] = 1
        self.ids.filechooser.size_hint[0] = 0
        self.ids.filechooser.size_hint[1] = 0
        image = self.ids.my_image.source
        img_bool = True

    def clear_canvas(self):
        global image
        global img_bool
        self.ids.my_image.source = "C:/Users/Blake Lawyer/Desktop/Python/ComputerVision/images/black.png"
        image = ""
        img_bool = False

    def rotate_image(self):
        global img_bool
        global image
        if img_bool:
            t = random.randint(1, 360)
            pic = cv2.imread(image)
            rotated_pic = np.zeros(pic.shape, dtype='u1')
            indices = np.where(np.all(pic != (0, 0, 0), axis=-1))
            coords = list(zip(indices[0], indices[1]))
            for coord in coords:
                x, y = self.random_rotation(t, coord, pic.shape[1], pic.shape[0])
                rotated_pic[x][y] = pic[coord[0]][coord[1]]

            texture = Texture.create(size=(rotated_pic.shape[1], rotated_pic.shape[0]), colorfmt='bgr')
            texture.blit_buffer(rotated_pic.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
            texture.flip_vertical()
            self.ids.my_image.texture = texture
        else:
            pass

    def spin_wheel(self):
        global img_bool
        global image
        global spin_mode
        spin_mode = True
        print("Spin the wheel!")
        spin_dir = os.listdir("images/spin")
        if len(spin_dir) == 0 and img_bool:
            print("No spin images found. Spinning the wheel...")
            for i in range(0, 360):
                print(f"{i}/361")
                pic = cv2.imread(image)
                rotated_pic = np.zeros(pic.shape, dtype='u1')
                indices = np.where(np.all(pic != (0, 0, 0), axis=-1))
                coords = list(zip(indices[0], indices[1]))
                for coord in coords:
                    x, y = self.random_rotation(i, coord, pic.shape[1], pic.shape[0])
                    rotated_pic[x][y] = pic[coord[0]][coord[1]]
                cv2.imwrite(f"images/spin/{i}.png", rotated_pic)
        else:
            pass


class TransformEditorScroll(ScrollView):
    pass


class TransformEditorStack(StackLayout):
    pass


class TransformEditor(App):

    def on_start(self):
        global spin_dir
        spin_dir = os.listdir("images/spin")
        spin_dir = sorted(spin_dir, key=lambda fname: int(fname.split('.')[0]))
        Clock.schedule_interval(self.update_label, .01)

    def update_label(self, *args):
        global spin_dir
        print(len(spin_dir))
        rotation_matrix = f"\n[cos({theyta}), -sin({theyta})] [{ex}] = [{ex_2}]\n" \
                          f" [sin({theyta}), cos({theyta})] [{why}] = [{why_2}]\n"

        if spin_mode:
            if len(spin_dir) > 1:
                image = spin_dir.pop(0)
                print(image)
                self.root.ids.my_image.source = "images/spin/" + spin_dir.pop(0)
            else:
                spin_dir = os.listdir("images/spin")
                spin_dir = sorted(spin_dir, key=lambda fname: int(fname.split('.')[0]))
                self.root.ids.my_image.source = "images/spin/" + spin_dir.pop(0)

        self.root.ids.matrix_2.text = rotation_matrix


TransformEditor().run()

