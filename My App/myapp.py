

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video
from kivy.uix.screenmanager import NoTransition
from kivy.uix.spinner import Spinner
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import time
from kivy.uix.widget import Widget
#from backend_kivyagg import FigureCanvasKivyAgg
#from matplotlib.backends.backend_kivyagg import FigureCanvasKivyAgg
#import tkinter as tk
import numpy as np
import io
from PIL import Image as PILImage
import csv

from qiskit.quantum_info import Operator
from qiskit.circuit.library import UnitaryGate
import numpy as np
from qiskit import transpile 
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.layout import Layout
#from qiskit_ibm_runtime import JobStatus
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


import random

import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

bg_image_path = resource_path("assets/bg.png")

def binary_increment(x):
    i=-1
    while True:
        if sum(x)==len(x):
            return 'error maximum state reached'
        if x[i]==0:
            x[i]=1
            break
        elif x[i]==1:
            x[i]=0
        i=i-1
    
    return x

def states_set(n):
    st0 = [0]*n

    states =[st0]

    for i in range(2**n-1):
        states.append(binary_increment(states[-1][:]))
    
    return states


def f(x, half_num):
    n = len(x)
    states = states_set(n)

    for i in half_num:
        bol = True
        for j in range(n):
            if x[j]!=states[i][j]:
                bol = False
        
        if bol:
            return 1
    
    return 0

def fs(x, s):
    S=0
    for i in range(len(x)):
        S= S+ x[i]*s[i]
    return S%2

""""""
s1 =0
s2 =0
score_result=[]

hs1 =0
hs2 =0
hscore_result=[]

qs1 = 0
qs2 =0
qscore_result=[]

bvs1 =0
bvs2 =0
bvscore_result=[]

hbvs1 =0
hbvs2 =0
hbvscore_result=[]

qbvs1 =0
qbvs2 =0
qbvscore_result=[]
""""""
def complete_result():
    global s1, s2, score_result, hs1, hs2, hscore_result, qs1, qs2, qscore_result, bvs1, bvs2, bvscore_result, hbvs1, hbvs2, hbvscore_result, qbvs1, qbvs2, qbvscore_result
    s1 =0
    s2 =0
    score_result=[]

    hs1 =0
    hs2 =0
    hscore_result=[]

    qs1 = 0
    qs2 =0
    qscore_result=[]

    bvs1 =0
    bvs2 =0
    bvscore_result=[]

    hbvs1 =0
    hbvs2 =0
    hbvscore_result=[]

    qbvs1 =0
    qbvs2 =0
    qbvscore_result=[]


"""
class MPL_Widget(Widget):
    def __init__(self, fig, **kwargs):
        super(MPL_Widget, self).__init__(**kwargs)
        self.canvas = FigureCanvasTkAgg(fig, master=tk.Tk())
        self.canvas.draw()
"""

class MatplotlibImage(Image):
    def __init__(self, figure, size = None, size_hint =None, pos = None, pos_hint =None, **kwargs):
        super(MatplotlibImage, self).__init__(**kwargs)
        self.figure = figure
        self.figure = figure
        self.size_hint = size_hint
        self.pos_hint = pos_hint
        self.update_plot()

    def update_plot(self):
        # Save the figure to a BytesIO buffer
        buf = io.BytesIO()
        self.figure.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        # Use PIL to open the image and get its size
        pil_image = PILImage.open(buf)
        width, height = pil_image.size
        
        # Flip the image vertically
        pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)
        
        # Convert PIL image to RGB
        pil_image = pil_image.convert('RGB')
        image_data = pil_image.tobytes()
        
        # Create Kivy Texture
        texture = Texture.create(size=(width, height), colorfmt='rgb')
        texture.blit_buffer(image_data, colorfmt='rgb', bufferfmt='ubyte')
        
        # Update Kivy Image widget with the texture
        
        self.texture = texture

        buf.close()

class DualStateImage(ButtonBehavior, Image):
    def __init__(self, image1, image2, **kwargs):
        super(DualStateImage, self).__init__(**kwargs)
        self.image1 = image1
        self.image2 = image2
        self.current_state = True  # Start with the first image
        self.source = self.image1  # Set the initial image

    def on_press(self):
        # Toggle between the two images
        if self.current_state:
            self.source = self.image2
        else:
            self.source = self.image1
        self.current_state = not self.current_state

    def get_state(self):
        # Returns the current state (True for image1, False for image2)
        return (not self.current_state)

class ConditionBasedImage(ButtonBehavior, Image):
    def __init__(self, image1, image2, **kwargs):
        super(ConditionBasedImage, self).__init__(**kwargs)
        self.image1 = image1
        self.image2 = image2
        self.current_image = self.image1
        self.source = self.current_image

    def set_image(self, condition):
        if condition:
            self.current_image = self.image1
        else:
            self.current_image = self.image2
        self.source = self.current_image
    
    def on_press(self):
        pass  
"""
class Counter(ButtonBehavior, Image):
    def __init__(self, image1, **kwargs):
        super(Counter, self).__init__(**kwargs)
        self.image1 = image1
        self.current_image = self.image1
        self.source = self.current_image

    def set_image(self, condition):
        if condition:
            self.current_image = self.image1
        else:
            self.current_image = self.image2
        self.source = self.current_image 
"""
class WrappedLabel(Label):
    def __init__(self, text, hmar=100, font_size = 25, **kwargs):
        super().__init__(text=text, size_hint=(None, None), font_size= font_size, halign='justify', valign='middle', **kwargs)
        self.hmar = hmar

        # Bind the size update to window resizing
        Window.bind(on_resize=self.update_label_size)

        # Initial size update
        self.update_label_size()

    def update_label_size(self, *args):
        # Calculate the available width considering the padding
        available_width = Window.width - 2 * self.hmar
        self.width = available_width
        self.text_size = (available_width, None)

class TableWidget(GridLayout):
    def __init__(self, score_result, H1 = 'Number of Batsmen:', H2 = 'Nunmber of Attempts:', H3 = 'Nunmber of Attempts:', **kwargs):
        super(TableWidget, self).__init__(**kwargs)

        if len(score_result)==0:

            #self.cols = 2
            self.cols = 1
            self.size_hint = (0.8, 0.4)
            self.height =20
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

            #NA = Label(text = 'NA', font_size = 50, size_hint_y = None, height = 50)

            h1 = Label(text = H1, font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h1)

            #self.add_widget(NA)

            for i in range(2):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)
            
            h2 = Label(text = H2, font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h2)


            #self.add_widget(NA)

            for i in range(2):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)
            
            h3 = Label(text = H3, font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h3)

            #self.add_widget(NA)

            for i in range(2):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)

        else:    
        
            self.cols = len(score_result) + 1
            self.size_hint = (0.8, 0.4)
            self.height =20
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

            h1 = Label(text = 'Number of Batsmen:', font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h1)

            for i in range(len(score_result)):
                batnum = Label(text = str(score_result[i][0]), font_size = 50, color = (1, 0, 0, 1), size_hint_y = None, height =50)
                self.add_widget(batnum)

            for i in range(len(score_result)+1):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)
            
            h2 = Label(text = 'Nunmber of Attempts:', font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h2)


            for i in range(len(score_result)):
                attnum = Label(text = str(score_result[i][1]), font_size = 50, color = (0, 1, 0, 1), size_hint_y = None, height =50)
                self.add_widget(attnum)

            for i in range(len(score_result)+1):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)
            
            h3 = Label(text = 'Result: ', font_size = 30, size_hint_y = None, height =50, halign = 'left')
            self.add_widget(h3)



            for i in range(len(score_result)):
                if score_result[i][2]:
                    x = 'Correct'
                else:
                    x = 'False'
                sco = Label(text = x, font_size = 30, color = (0, 0, 1, 1), size_hint_y = None, height =50)
                self.add_widget(sco)

            for i in range(len(score_result)+1):
                spacer = Widget(size_hint_y=None, height=50)
                self.add_widget(spacer)

class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

        home_layout = FloatLayout(size_hint=(1, 1), pos_hint = {'center_x':0.5, 'center_y':0.5})  
        self.add_widget(home_layout)

        title = Label(text="Welcome", font_size=130, size_hint_y=None, height=50, pos_hint = {'center_x':0.5, 'center_y':0.9})
        home_layout.add_widget(title)

        button_grid = GridLayout(cols=1, size_hint=(0.5, 0.5), spacing = 30)
        button_grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(button_grid)

        DJ_but = Button(text="Play Deustch-Jousza Game", size_hint=(0.8, 0.2), font_size = 50)
        DJ_but.bind(on_press=self.DJsc)
        button_grid.add_widget(DJ_but)

        BV_but = Button(text="Play Bersntien-Vazarani Game", size_hint=(0.8, 0.2), font_size = 50)
        BV_but.bind(on_press=self.BVsc)
        button_grid.add_widget(BV_but)

        R_but = Button(text="Use Real Quantum Computer!", size_hint=(0.8, 0.2), font_size = 50)
        R_but.bind(on_press=self.Rsc)
        button_grid.add_widget(R_but)

    def DJsc(self, instance):
        self.manager.current = 'article1'
    
    def BVsc(self, instance):
        self.manager.current = 'article5'
    
    def Rsc(self,instance):
        self.manager.current = 'Real_DJ'






         

class Article1(Screen):
    def  __init__(self, **kwargs):
        super(Article1, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        # Add a title
        title = Label(text="Lesson 1.1: The Deutsch-Jousza Problem", font_size=70, size_hint_y=None, height=80, valign = 'bottom')
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="The Problem:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "Now we come to one of the first problems where Quantum Computers have a substantial advantage over classical computers: The Deustch-Jousza Problem. Here we have created an analogy to simplify the Deutsch-Jousza Problem: so Let’s get ready to play some cricket! ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        paragraph2 = WrappedLabel(text = "The problem goes as follows: there are 5 batsmen on a cricket pitch, each of whom are going to get bolled a ball. Each of these batsmen will either score ‘0’ runs, or ‘6’ runs. As each batsmen can either score 0 or 6 runs and there are 5 batsmen, this means there are 2^5 or 32 possible run combinations that can occur. Keep note of this, it will be important later! ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        # Add an image
        image1 = Image(source=resource_path('assets/Batsmen.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)

        paragraph3 = WrappedLabel(text =  "Moving on, there are currently two Umpires who are working at the Stadium, one of them is a fair and unbiased Umpire. This means that no matter what runs the batsmen hit this umpire will show no reaction and just continue to monitor the game.", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph3)

        image2 = Image(source=resource_path('assets/Fair U.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image2)

        paragraph4 = WrappedLabel(text =  "The other Umpire is a biased Umpire, but the catch is we don’t know how exactly he’s biased. All we know is that for exactly half of the run combinations (that is the combinations of 0’s and 6’s), the Umpire will start dancing. Which half is this? We have no clue.", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph4)

        image3 = Image(source=resource_path('assets/Biased U.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image3)

        sp1 = Label(text= "")
        self.article_layout.add_widget(sp1)

        paragraph5 = WrappedLabel(text =  "Now, we don’t know whether the Umpire who is currently monitoring the game is fair or biased, so the Cricket Authorities have entrusted you with determining this. You can do this by selecting a certain combination of 0 and 6 runs for the batsmen to hit, and then observing the Umpire’s reaction. Your goal is to correctly determine which Umpire is monitoring the match, while observing the Umpire’s reaction as little as possible. Remember, the biased Umpire will only dance for half of the possible combinations of runs, so just because the umpire doesn’t dance, doesn’t necessarily mean that he’s the fair umpire.", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph5)

        sp2 = Label(text= "")
        self.article_layout.add_widget(sp2)

        next_button = Button(text = "Next Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)
    
        self.add_widget(self.scroll_view)

    def next_screen(self, instance):
        self.manager.current = 'article2'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article2(Screen):
    def  __init__(self, **kwargs):
        super(Article2, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)        

        title = Label(text="Lesson 1.1: The Deutsch-Jousza Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="How to Play:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "You can see whether a batsman is going to hit 0 or 6 runs by the number above their head, and you can change it by clicking on the batsman. ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        paragraphg = WrappedLabel(text = "", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraphg)

        

        paragraph2 = WrappedLabel(text = "Once you’re happy with the combination of 0 and 6 runs you have chosen, you can observe the Umpire’s reaction by pressing the ‘Check Reaction’ Button. ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        # Add an image
        image1 = Image(source=resource_path('assets/Check Reaction.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)

        paragraph3 = WrappedLabel(text =  "If you’re confident you’ve found whether the Umpire is biased or not, select your guess by clicking either the ‘Fair Umpire’ or ‘Biased Umpire’ Buttons. ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph3)

        image2 = Image(source=resource_path('assets/Fair Biased Buttons.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image2)

        paragraph4 = WrappedLabel(text =  "The green counter on the top-right of the screen will count out how many times you have checked the Umpire’s reaction",
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph4)

        image3 = Image(source=resource_path('assets/query counter.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image3)

        paragraph5 = WrappedLabel(text =  "To play the game again just click the restart button in the bottom-right corner. This will reset whether the Umpire is fair or biased so you can play the game again. ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        self.article_layout.add_widget(paragraph5)
        
        paragraph6 = WrappedLabel(text =  "It’s a good idea to play the game at least 5-10 times to get a feel for it, you’ll be able to see your results once you finish with the game, but for now let’s get to playing some Cricket! ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        
        self.article_layout.add_widget(paragraph6)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'article1'
    
    def next_screen(self, instance):
        #self.manager.current = 'DJ_game'

        sm = self.manager

        sm.remove_widget(sm.get_screen('DJ_game'))
            
        new_dj_game = DJ_game(name='DJ_game')
        sm.add_widget(new_dj_game)
            
        sm.current = 'DJ_game'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article3(Screen):
    def  __init__(self, **kwargs):
        super(Article3, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Lesson 1.2: The Deutsch-Jousza Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="Now Play Against a Quantum Computer!:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "You are now going to get to play against a Quantum Computer!! You still play the game as usual, expect after you’ve finished your turn the quantum computer will give it a go, and keep an eye out for how many times it checks the umpire and how often it gets the right Answer! ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        image1 = Image(source=resource_path('assets/QC Pic.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)

        paragraph2 = WrappedLabel(text = "To play again just click the restart button ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        # Add an image
        image2 = Image(source=resource_path('assets/Restart Button.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image2)

        paragraph3 = WrappedLabel(text =  "Good Luck! ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph3)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'DJ_Summary'
    
    def next_screen(self, instance):
        self.manager.current = 'DJ_Quantum_New'
        """
        sm = self.manager

        sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
        new_dj_game = DJ_Quantum_New(name='DJ_Quantum_new')
        sm.add_widget(new_dj_game)
            
        sm.current = 'DJ_Quantum_New'
        """
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article4(Screen):
    def  __init__(self, **kwargs):
        super(Article4, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Lesson 2.1: The Bernstein-Vazarani Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="How to Play:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "Here we look at a slightly more complex problem, the Bernstein Vazarin problem. Here our goal is to determine a secret string of 1’s and 0’s (e.g 110110, 010100). We don't know what this string is, but the umpire does, and in front of him are an equal number of batsmen to the length of the string, one for each digit. Each batsman can either score a 0 or a 1, and depending on what the batsmen score, the Umpire will use a special rule to determine whether to stay still or to dance. ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        paragraph2 = WrappedLabel(text = "This rule is not too complicated, the umpire lines up each batsman with his corresponding digit and he counts the number of cases where both the digit is 1 and the corresponding batsman scored a 1, and if the resulting number is even he does nothing, if it's odd he dances. See two examples below: ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        # Add an image
        image1 = Image(source=resource_path('assets/string eg1.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)

        image1x = Image(source=resource_path('assets/string eg2.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1x)

        paragraph3 = WrappedLabel(text =  "You need to find the secret string of 0’s and 1’s and type it into the text box on the right. In the next activity you’ll get a chance to get used to this", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph3)

        image2 = Image(source=resource_path('assets/Fair Biased Buttons.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image2)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'DJ_Quantum_Summary'
    
    def next_screen(self, instance):
        self.manager.current = 'article5'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article5(Screen):
    def  __init__(self, **kwargs):
        super(Article5, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Lesson 2.1: The Deutsch-Jousza Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="Get A Feel For It:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "In this activity you have an opportunity to get a feel for the rule the umpire uses to dance or not. You can choose a string of 0’s and 1’s to create your own secret string, and then change the batsmen's runs to see how the umpire will react. Once again the umpire counts the number times both the digit and the corresponding run is 1, and if it's even he does nothing, and if it's odd he dances. To change a 1 to a zero just click on it! ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        image1 = Image(source=resource_path('assets/string eg1.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'article4'
    
    def next_screen(self, instance):
        sm = self.manager

        sm.remove_widget(sm.get_screen('BV_demo'))
            
        new_dj_game = BV_demo(name='BV_demo')
        sm.add_widget(new_dj_game)
            
        sm.current = 'BV_demo'

    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article6(Screen):
    def  __init__(self, **kwargs):
        super(Article6, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Lesson 2.2: The Bernstein-Vazarani Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="Get Ready to Play:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "Now that you have a feel for the way it works, lets move on to the game, here you wont have the string in front of you, so you’ll have to figure it out based on the umpires reactions to different run sequences. Once you've figured it out, you can input your answer into the text box on the right to see if you’ve got it right.", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        image1x = Image(source=resource_path('assets/bv setup.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1x)

        image1y = Image(source=resource_path('assets/s text box.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1y)


        paragraph4 = WrappedLabel(text =  "The green counter on the top-right of the screen will count out how many times you have checked the Umpire’s reaction",
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph4)

        image3 = Image(source=resource_path('assets/query counter.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image3)

        paragraph5 = WrappedLabel(text =  "This game may seem very hard at first but there is actually a simple strategy that allows you to find the string really quickly, see if you can find it!", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        self.article_layout.add_widget(paragraph5)


        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'BV_demo'
    
    def next_screen(self, instance):
        sm = self.manager

        sm.remove_widget(sm.get_screen('BV_game'))
            
        new_dj_game = BV_game(name='BV_game')
        sm.add_widget(new_dj_game)
            
        sm.current = 'BV_game'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article7(Screen):
    def  __init__(self, **kwargs):
        super(Article7, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Lesson 2.3: The Bernstein Vazarani Problem", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="Play Against a Quantum Computer:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph
        paragraph1 = WrappedLabel(text = "Now you get to play against a Quantum Computer. Same as last time you can check the umpire as many times as you want and check if your answer is right, then the quantum computer will give it a go and see how many times it needs to check the umpire and how often it gets the right answer.  ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        image1 = Image(source=resource_path('assets/QC Pic.png'), size_hint_y=None, height=200)
        self.article_layout.add_widget(image1)

        paragraph2 = WrappedLabel(text = "\n \n \n \n \nTo give you the best chance, the best strategy you should use to determine the string is as follows. First set just the first batsman to 1 and the rest to zero. Then if the first digit is zero then there are no cases in which both the batsmen scores a 1 and the digit is a 1, so the umpire does nothing. But if the first digit is a 1 then there will be exactly 1 case where both the batsman’s runs and the digit is 1 and hence the umpire will dance. Thus with just one check of the Umpire you can determine the first digit! If he dances it's a 1 if not it is zero. You can then repeat the same process for the other digits, just set all other batsmen to zero and just the desired digit’s batsman to 1, and if the umpire dances it's a 1 and if not it's a zero. Using this strategy you should be able to reliably determine the string of 0’s and 1’s by checking the umpire once for each batsman present. Good Luck! \n \n ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        paragraph3 = WrappedLabel(text = "\n \n \n ", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph3)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'BV_Summary'
    
    def next_screen(self, instance):
        sm = self.manager

        sm.remove_widget(sm.get_screen('BV_Quantum'))
            
        new_dj_game = BV_Quantum(name='BV_Quantum')
        sm.add_widget(new_dj_game)
            
        sm.current = 'BV_Quantum'

    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class Article8(Screen):
    def  __init__(self, **kwargs):
        super(Article8, self).__init__(**kwargs)
        # Create a ScrollView
        self.scroll_view = ScrollView()

        self.hmar = 100
        vmar = 30

        # Create a BoxLayout to contain the article content
        self.article_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = [self.hmar, vmar, self.hmar, vmar])
        self.article_layout.bind(minimum_height=self.article_layout.setter('height'))

        # Add the layout to the scroll view
        self.scroll_view.add_widget(self.article_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        back_button.bind(on_press = self.hsc)
        self.article_layout.add_widget(back_button)

        title = Label(text="Conclusion: Real Quantum Computers", font_size=70, size_hint_y=None, height=50)
        self.article_layout.add_widget(title)

        # Add a heading
        heading = Label(text="Play with a real Quantum Computer:", font_size=40, size_hint_y=None, height=40, halign = 'left', text_size=(None, None))
        heading.bind(size=lambda s, w: s.setter('text_size')(s, (s.width, None)))
        self.article_layout.add_widget(heading)

        # Add a paragraph

        paragraph1y = WrappedLabel(text = "\n \n \n \n  ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1y)

        paragraph1 = WrappedLabel(text = "\n \n \n \n So now you’ve seen that for the Deutsch-Jousza problem you usually need 3-4 checks of the umpire to usually get the right answer, but a quantum computer can always get it right 100% of the time in just one query or one check of the umpire. More impressively for the Bernstein- Vazarani Problem you need to check the umpire at least once per batsman present or number of digits in the string, but no matter the number of batsmen a quantum number can always predict the entire string in just one check of the empire. This means if you had a 1000000 digit string it would take you or a classical computer 1000000 checks of the umpire to determine it, but a quantum computer would still be able to do it in just one query. ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1)

        paragraph1x = WrappedLabel(text = "\n \n \n \n  ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1x)

        paragraph2 = WrappedLabel(text = "Now that you understand the power of quantum computers, are you ready to use a real one? So far we have only been using simulated quantum computers, but in the next activity you can use a real one!! You can play the Deutsch-Jousza Game, we will tell you whether the umpire is fair or biased, and then you can send a request to run the problem to IMB’s real operational quantum computers. You will get a job_id, and after it has finished running, which usually takes a couple of hours, you can just input your job_id to see what the quantum computer predicted and whether it was correct. You should get a job_id keep it with you and then check back after a couple of hours, and shutting the app in between makes no difference. Have fun!", 
                                  hmar = self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph2)

        paragraph1z = WrappedLabel(text = "\n \n \n \n  ", 
                                  hmar =self.hmar,
                                  font_size=30
                                  )
        
        self.article_layout.add_widget(paragraph1z)



        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.1})
        prev_button.bind(on_press = self.prev_screen)
        self.article_layout.add_widget(prev_button)

        next_button = Button(text = "Lets Play!", size = (250, 100), size_hint = (None, None), pos_hint = {'center_x': 0.9})
        next_button.bind(on_press = self.next_screen)
        self.article_layout.add_widget(next_button)

        self.add_widget(self.scroll_view)

    
    def prev_screen(self, instance):
        self.manager.current = 'BV_Quantum_Summary'
    
    def next_screen(self, instance):
        self.manager.current = 'Real_DJ'

    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'


     
    


class DJ_game(Screen):
    def __init__(self, n=5, gm = 'Easy', **kwargs):
        super(DJ_game, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bol = random.choice([True, False])
        self.snum = 0
        self.pressed = False

        self.bits = n

        self.gmc = gm

        states = states_set(n)
        
        self.half_num =[]

        while True:
            i = random.randint(0, len(states)-1)
            if not (i in self.half_num):
                self.half_num.append(i)
            if len(self.half_num)==2**(n-1):
                break


        # Horizontal GridLayout for images
        #image_grid = GridLayout(cols=5, size_hint_y=None, height=700)
        #self.add_widget(image_grid)
        image_grid = GridLayout(cols=n, size_hint_y=None, height=700)
        image_grid.size_hint = (0.55, 0.6)
        #image_grid.width = 1000  # Adjust width as needed
        image_grid.pos_hint = {'x': 0.05, 'top': 0.7}
        self.add_widget(image_grid)

        # Create images and add them to the image grid layout
        self.Bs = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs.append(dual_state_image)
            image_grid.add_widget(dual_state_image)

        #condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        #self.add_widget(condition_layout)

        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.6, 'center_y': 0.5}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check Reaction", size=(230, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        #button_grid = GridLayout(cols=1, size_hint_y=None, height=500)
        #self.add_widget(button_grid)

        button_grid = GridLayout(cols=1, size_hint_y=None, height=350, spacing = 20)
        button_grid.size_hint = (0.15, 0.3)
        button_grid.width = 300
        button_grid.pos_hint = {'x': 0.85, 'y': 0.23}
        self.add_widget(button_grid)

        self.result_label = Label(text="", font_size=48, color=(1, 0, 0, 1), size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.fair = Button(text="Fair Umpire", size_hint=(None, None), size=(200, 100))
        self.fair.bind(on_press=self.Fair_check)
        button_grid.add_widget(self.fair)

        self.biased = Button(text="Biased Umpire", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Biased_check)
        button_grid.add_widget(self.biased)

        self.restart_button = Button(text="Play Again", size_hint=(None, None), size=(200, 100))
        self.restart_button.bind(on_press=self.restart)
        button_grid.add_widget(self.restart_button)

        corner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        corner_image_layout.pos_hint = {'right': 1, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(corner_image_layout)

        corner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        corner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        corner_image_layout.add_widget(corner_image)

        self.corner_label = Label(text="0", font_size=100, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.corner_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        corner_image_layout.add_widget(self.corner_label)

        corner_title = Label(text = "Number of Attempts:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        corner_title.pos_hint = {'center_x': 0.5, 'y': 0.7}  
        corner_image_layout.add_widget(corner_title)
        """
        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.5, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source='red circle.png', size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = 'Down Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = 'Up Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)
        """

       
        score_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        score_layout.pos_hint = {'right': 1, 'top': 0.8}  # Position layout in the upper right-hand corner
        self.add_widget(score_layout)

        score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        score_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        score_layout.add_widget(score_image)

        self.score_label = Label(text=str(s2) + '/' + str(s1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.score_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        score_layout.add_widget(self.score_label)

        score_title = Label(text = "Overall Score:", font_size = 40, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        score_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        score_layout.add_widget(score_title)

        mode_layout = FloatLayout(size_hint=(None, None), size=(300, 200))
        mode_layout.pos_hint = {'center_x': 0.3, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(mode_layout)

        mode_title = Label(text = 'Select Game Mode:', font_size = 30)
        mode_title.pos_hint = {'center_x': 0.5, 'center_y':0.75}
        mode_layout.add_widget(mode_title)

        self.mode_sel = Spinner(text =gm, values = ('Easy', 'Medium', 'Hard'), size_hint=(None, None), size=(200, 44))
        self.mode_sel.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        self.mode_sel.bind(text=self.mode_select)  
        mode_layout.add_widget(self.mode_sel) 

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)


        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "See Summary", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)


        self.res_layout = FloatLayout(size_hint = (0.8, 0.8))
        self.res_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.res_layout)




        

       
    def check_state(self, instance):
        bin=[]
        for ds in self.Bs:
            s = ds.get_state()
            if s:
                bin.append(1)
            else:
                bin.append(0)

        if self.bol:
            output = f(bin, self.half_num)
        else:
            output = 0
    
        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))
        if not self.pressed:
            self.snum = self.snum + 1
            self.corner_label.text = str(self.snum)
        #return output
        
    def splash_remove(self, splash, block):
        self.remove_widget(block)
        self.res_layout.remove_widget(splash)

    def Fair_check(self, instance):
        global s1, s2, score_result
        if not self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                score_result.append([self.bits, att, res])
                s1 = s1 +1
                s2 = s2 +1
                self.score_label.text = str(s2) + '/' + str(s1)

                self.pressed= True

        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                score_result.append([self.bits, att, res])
                s1 = s1 +1
                self.score_label.text = str(s2) + '/' + str(s1)

                self.pressed= True

        
    def Biased_check(self, instance):
        global s1, s2, score_result
        if self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                score_result.append([self.bits, att, res])
                s1 = s1 +1
                s2 = s2 +1
                self.score_label.text = str(s2) + '/' + str(s1)

                self.pressed= True
        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                score_result.append([self.bits, att, res])
                s1 = s1 +1
                self.score_label.text = str(s2) + '/' + str(s1)

                self.pressed= True

    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('DJ_game'))
                
        new_dj_game = DJ_game(name='DJ_game', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'DJ_game'

        sm.transition = original_transition
    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_game'))
                
            new_dj_game = DJ_game(name='DJ_game', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'DJ_game'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_game'))
            
            new_dj_game = DJ_game(name='DJ_game', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_game'

            sm.transition = original_transition

    def mode_select(self, mode_sel, text):
        global s1, s2, score_result
        if text == 'Easy' and (self.gmc != 'Easy'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_game'))
            
            new_dj_game = DJ_game(name='DJ_game', n=5)
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_game'

            sm.transition = original_transition
        
        if text == 'Medium' and (self.gmc != 'Medium'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_game'))
            
            new_dj_game = DJ_game(name='DJ_game', n=8, gm='Medium')
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_game'

            sm.transition = original_transition
        
        if text == 'Hard' and (self.gmc != 'Hard'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_game'))
            
            new_dj_game = DJ_game(name='DJ_game', n=12, gm ='Hard')
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_game'

            sm.transition = original_transition
        s1 =0
        s2 =0
        score_result=[]

    def prev_screen(self, instance):
        global s1, s2, score_result
        s1 =0
        s2 =0
        score_result=[]
        self.manager.current = 'article2'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.remove_widget(sm.get_screen('DJ_Summary'))
            
        new_dj_sum = DJ_Summary(name='DJ_Summary')
        sm.add_widget(new_dj_sum)
            
        sm.current = 'DJ_Summary'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'




class DJ_Summary(Screen):
    def __init__(self, **kwargs):
        super(DJ_Summary, self).__init__(**kwargs)

        global score_result
        
        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)
        
        

        sum_layout = BoxLayout(orientation='vertical', size_hint = (1, 1), spacing = 50, padding = [40, 30, 40, 30])
        self.add_widget(sum_layout)

        Title = Label(text = 'Summary of Results: ', font_size=70, size_hint_y=None, height=100)
        sum_layout.add_widget(Title)

        Num_layout = GridLayout(cols=2, size_hint_y=0.1)
        sum_layout.add_widget(Num_layout)

        score_layout = FloatLayout(size_hint=(1, 1))
        score_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(score_layout)

        Score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        Score_image.pos_hint = {'center_x': 0.8, 'center_y': 0.05}  # Center the image within its layout
        score_layout.add_widget(Score_image)

        if s1==0:
            P =0
        else:
            P = int((s2/s1)*100)

        Perscore = Label(text=str(P) + '%', font_size=80, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        Perscore.pos_hint = {'center_x': 0.8, 'center_y': 0.02}  # Position the label just above the image
        score_layout.add_widget(Perscore)

        Perscore_title = Label(text = "Total Accuracy Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Perscore_title.pos_hint = {'center_x': 0.3, 'y': 0.05}  
        score_layout.add_widget(Perscore_title)

        Bitnum_layout = FloatLayout(size_hint=(1, 1))
        Bitnum_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(200, 200))
        Bitnum_image.pos_hint = {'center_x': 0.8, 'center_y': 0.05}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        if len(score_result)==0:
            B=0
        else:
            B = score_result[0][0]

        self.Bitnum = Label(text=str(B), font_size=70, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.8, 'center_y': 0.02}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0.35, 'y': 0.05}  
        Bitnum_layout.add_widget(Bitnum_title)

        
        sno = [str(x) for x in range(1, len(score_result)+1)]
        att = []
        col =[]
        for x in score_result:
            att.append(x[1])
            if x[2]:
                col.append('green')
            else:
                col.append('red')
        
        att_c =[]
        for x in score_result:
            if x[2]:
                att_c.append(x[1])

        if len(att_c)>0:
            att_avg = sum(att_c)/len(att_c)
        
        fig, ax = plt.subplots()

        ax.bar(sno, att, color = col)
        ax.set_title('Number of Attempts Taken')
        ax.set_ylabel('Number of Attempts Taken')
        ax.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(att_c)>0:
            avgline = ax.axhline(y=att_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax.legend(handles=legend_patches)
        if len(att)>0:
            ax.set_ylim(0, 1.2*max(att))
            ax.set_yticks(range(max(att)+1))
        
        
        img = MatplotlibImage(fig, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        sum_layout.add_widget(img)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)

        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Play Again", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

    def prev_screen(self, instance):
        global s1, s2, score_result
        s1 =0
        s2 =0
        score_result=[]
        sm = self.manager 

        sm.remove_widget(sm.get_screen('DJ_game'))
            
        new_dj_game = DJ_game(name='DJ_game')
        sm.add_widget(new_dj_game)
        
        sm.current = 'DJ_game'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.current = 'article3'

    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class DJ_Quantum(Screen):
    def __init__(self, n=5, **kwargs):
        super(DJ_Quantum, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bol = random.choice([True, False])
        self.snum = 0
        self.pressed = False

        self.bits = n

        states = states_set(n)
        
        self.half_num =[]

        while True:
            i = random.randint(0, len(states)-1)
            if not (i in self.half_num):
                self.half_num.append(i)
            if len(self.half_num)==2**(n-1):
                break

        # Horizontal GridLayout for images
        #image_grid = GridLayout(cols=5, size_hint_y=None, height=700)
        #self.add_widget(image_grid)
        image_grid = GridLayout(cols=n, size_hint_y=None, height=700)
        image_grid.size_hint = (0.45, 0.6)
        #image_grid.width = 1000  # Adjust width as needed
        image_grid.pos_hint = {'x': 0.05, 'y': 0.05}
        self.add_widget(image_grid)

        # Create images and add them to the image grid layout
        self.Bs = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs.append(dual_state_image)
            image_grid.add_widget(dual_state_image)

        #condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        #self.add_widget(condition_layout)

        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.5, 'center_y': 0.5}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check State", size=(200, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        Q_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        Q_layout.size_hint = (0.15, 0.7)
        #Q_layout.height = 1000
        Q_layout.pos_hint = {'x': 0.7, 'center_y': 0.5}
        self.add_widget(Q_layout)


        self.QC_image = Image(source = resource_path('assets/QC image1.png'))
        Q_layout.add_widget(self.QC_image)

        self.QC_button = Button(text="Use \n Quantum \n Computer", size=(200, 100), size_hint=(None, None), pos_hint={'center_x': 0.5}, halign='center', valign='middle')
        self.QC_button.bind(on_press=self.QC_run)
        Q_layout.add_widget(self.QC_button)

        self.QC_label = Label(text="", font_size=48, color=(0, 0, 1, 1), size_hint_y=None, height=100)
        Q_layout.add_widget(self.QC_label)

        button_grid = GridLayout(cols=1, size_hint_y=None, height=350, spacing = 20)
        button_grid.size_hint = (0.15, 0.3)
        button_grid.width = 300
        button_grid.pos_hint = {'x': 0.85, 'y': 0.23}
        self.add_widget(button_grid)

        self.result_label = Label(text="", font_size=48, color=(1, 0, 0, 1), size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.fair = Button(text="Fair Umpire", size_hint=(None, None), size=(200, 100))
        self.fair.bind(on_press=self.Fair_check)
        button_grid.add_widget(self.fair)

        self.biased = Button(text="Biased Umpire", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Biased_check)
        button_grid.add_widget(self.biased)

        corner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        corner_image_layout.pos_hint = {'right': 1, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(corner_image_layout)

        corner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        corner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        corner_image_layout.add_widget(corner_image)

        self.corner_label = Label(text="0", font_size=100, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.corner_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        corner_image_layout.add_widget(self.corner_label)

        corner_title = Label(text = "Number of Attempts:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        corner_title.pos_hint = {'center_x': 0.5, 'y': 0.7}  
        corner_image_layout.add_widget(corner_title)

        self.restart_button = Button(text="Restart", size_hint=(None, None), size=(200, 100))
        self.restart_button.bind(on_press=self.restart)
        button_grid.add_widget(self.restart_button)

        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.5, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = resource_path('assets/Down Button.png'), size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = resource_path('assets/Up Button.png'), size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)


       
        score_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        score_layout.pos_hint = {'right': 1, 'top': 0.8}  # Position layout in the upper right-hand corner
        self.add_widget(score_layout)

        score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        score_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        score_layout.add_widget(score_image)

        self.score_label = Label(text=str(s2) + '/' + str(s1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.score_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        score_layout.add_widget(self.score_label)

        score_title = Label(text = "Overall Score:", font_size = 40, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        score_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        score_layout.add_widget(score_title)
        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "See Summary", size = (250, 100), size_hint = (None, None))
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)


        self.res_layout = FloatLayout(size_hint = (0.8, 0.8))
        self.res_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.res_layout)

        

    def check_state(self, instance):
        bin=[]
        for ds in self.Bs:
            s = ds.get_state()
            if s:
                bin.append(1)
            else:
                bin.append(0)

        if self.bol:
            output = f(bin, self.half_num)
        else:
            output = 0
    
        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))

        self.snum = self.snum + 1
        self.corner_label.text = str(self.snum)
        #return output

    def Fair_check(self, instance):
        global qs1, qs2, qscore_result
        if not self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Cor), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                qscore_result.append([self.bits, att, res])
                qs1 = qs1 +1
                qs2 = qs2 +1
                self.score_label.text = str(qs2) + '/' + str(qs1)

                self.pressed= True

        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Fal), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                qscore_result.append([self.bits, att, res])
                qs1 = qs1 +1
                self.score_label.text = str(qs2) + '/' + str(qs1)

                self.pressed= True
        
    def Biased_check(self, instance):
        global qs1, qs2, qscore_result
        if self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Cor), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                qscore_result.append([self.bits, att, res])
                qs1 = qs1 +1
                qs2 = qs2 +1
                self.score_label.text = str(s2) + '/' + str(s1)

                self.pressed= True
        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Fal), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                qscore_result.append([self.bits, att, res])
                qs1 = qs1 +1
                self.score_label.text = str(qs2) + '/' + str(qs1)

                self.pressed= True

    def QC_run(self, instance):
        def g(x):
            if self.bol:
                return f(x, self.half_num)
            else:
                return 0

        def Uf_man(state_list, n):
            Uf = QuantumCircuit(n+1)
            for bs in state_list:
                Uf.barrier()
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.mcx(list(range(n)), n)
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.barrier()
            return Uf
        
        def Uf(n):
    
            states_set=[[0]*(n+1)]


            for i in range((2**(n+1))-1):
                temp = states_set[-1].copy() 
                states_set.append(binary_increment(temp))

            Uf_array=[]

            for i in range(2**(n+1)):
                Uf_array.append([0]*(2**(n+1)))
        
            for i in range(len(states_set)):
            
                w = g(states_set[i][1:len(states_set)-1])

                if w==0:
                    Uf_array[i][i]=1
                if w==1:
                    if states_set[i][0]==0:
                        Uf_array[i][i+2**(n)]=1
                    if states_set[i][0]==1:
                        Uf_array[i][i-2**(n)]=1
                
            Uf_array = np.array(Uf_array)
            Uf_gate = Operator(Uf_array)
            
            return Uf_gate


        def Deutsch_J(n):
            dj = QuantumCircuit(n+1, n)
            dj.x(n)
            for i in range(n+1):
                dj.h(i)
            
            dj.barrier()
            dj.unitary(Uf(n), range(n+1))
            #dj.cx(0, 1)
            dj.barrier()

            for i in range(n):
                dj.h(i)
            
            return dj

        DJ = Deutsch_J(5)
        DJ.measure([i for i in range(5)], [i for i in range(5)])


        backend = AerSimulator()
        DJ_compiled = transpile(DJ, backend)

        job_sim = backend.run(DJ_compiled, shots=1024)

        result_sim = job_sim.result()

        counts = result_sim.get_counts(DJ_compiled)

        print(counts)

        c=1

        if '00000' in counts:
            c=0

        if c==0:
            self.QC_label.text = "Fair!"
        if c==1:
            self.QC_label.text = "Biased!"

        


    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('DJ_Quantum'))
                
        new_dj_game = DJ_Quantum(name='DJ_Quantum', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'DJ_Quantum'

        sm.transition = original_transition
    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum'))
                
            new_dj_game = DJ_Quantum(name='DJ_Quantum', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'DJ_Quantum'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum'))
            
            new_dj_game = DJ_Quantum(name='DJ_Quantum', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_Quantum'

            sm.transition = original_transition

    def prev_screen(self, instance):
        global qs1, qs2, qscore_result
        qs1 =0
        qs2 =0
        qscore_result=[]
        self.manager.current = 'article'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.remove_widget(sm.get_screen('DJ_Summary'))
            
        new_dj_sum = DJ_Summary(name='DJ_Summary')
        sm.add_widget(new_dj_sum)
            
        sm.current = 'DJ_Summary'

        

class DJ_Quantum_New(Screen):
    def __init__(self, n=5, gm = 'Easy', **kwargs):
        super(DJ_Quantum_New, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (0.82, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bol = random.choice([True, False])
        self.snum = 0
        self.qnum = 0
        self.pressed = False

        self.bits = n

        self.gmc = gm

        states = states_set(n)

        quips = [resource_path('assets/quip 1.png'), resource_path('assets/quip 2.png'), resource_path('assets/quip 3.png'), resource_path('assets/quip 4.png')]
        self.quip = random.choice(quips)
        
        self.half_num =[]

        while True:
            i = random.randint(0, len(states)-1)
            if not (i in self.half_num):
                self.half_num.append(i)
            if len(self.half_num)==2**(n-1):
                break

        # Horizontal GridLayout for images
        #image_grid = GridLayout(cols=5, size_hint_y=None, height=700)
        #self.add_widget(image_grid)
        image_grid = GridLayout(cols=n, size_hint_y=None, height=700)
        image_grid.size_hint = (0.45, 0.6)
        #image_grid.width = 1000  # Adjust width as needed
        image_grid.pos_hint = {'x': 0.05, 'y': 0.05}
        self.add_widget(image_grid)

        # Create images and add them to the image grid layout
        self.Bs = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs.append(dual_state_image)
            image_grid.add_widget(dual_state_image)

        #condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        #self.add_widget(condition_layout)

        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.5, 'center_y': 0.5}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check State", size=(200, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        Q_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        Q_layout.size_hint = (0.15, 0.5)
        #Q_layout.height = 1000
        Q_layout.pos_hint = {'x': 0.85, 'center_y': 0.35}
        self.add_widget(Q_layout)


        self.QC_image = Image(source=resource_path('assets/QC image1.png'))
        Q_layout.add_widget(self.QC_image)

        self.QC_label = Label(text="", font_size=48, color=(0, 0, 1, 1), size_hint_y=None, height=100)
        Q_layout.add_widget(self.QC_label)

        button_grid = GridLayout(cols=1, size_hint_y=None, height=350, spacing = 20)
        button_grid.size_hint = (0.15, 0.3)
        button_grid.width = 300
        button_grid.pos_hint = {'x': 0.67, 'y': 0.23}
        self.add_widget(button_grid)

        self.result_label = Label(text="", font_size=48, color=(1, 0, 0, 1), size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.fair = Button(text="Fair Umpire", size_hint=(None, None), size=(200, 100))
        self.fair.bind(on_press=self.Fair_check)
        button_grid.add_widget(self.fair)

        self.biased = Button(text="Biased Umpire", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Biased_check)
        button_grid.add_widget(self.biased)

        corner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        corner_image_layout.pos_hint = {'center_x': 0.75, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(corner_image_layout)

        corner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        corner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Center the image within its layout
        corner_image_layout.add_widget(corner_image)

        self.corner_label = Label(text="0", font_size=80, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.corner_label.pos_hint = {'center_x': 0.5, 'y': 0.34}  # Position the label just above the image
        corner_image_layout.add_widget(self.corner_label)

        corner_title = Label(text = "Your Attempts:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        corner_title.pos_hint = {'center_x': 0.5, 'y': 0.75}  
        corner_image_layout.add_widget(corner_title)

        self.restart_button = Button(text="Restart", size_hint=(None, None), size=(200, 100))
        self.restart_button.bind(on_press=self.restart)
        button_grid.add_widget(self.restart_button)

        qcorner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        qcorner_image_layout.pos_hint = {'center_x': 0.91, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(qcorner_image_layout)

        qcorner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qcorner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Center the image within its layout
        qcorner_image_layout.add_widget(qcorner_image)

        self.qcorner_label = Label(text="0", font_size=80, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.qcorner_label.pos_hint = {'center_x': 0.5, 'y': 0.34}  # Position the label just above the image
        qcorner_image_layout.add_widget(self.qcorner_label)

        qcorner_title = Label(text = "Quantum Computer \n Attempts:", font_size = 25, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        qcorner_title.pos_hint = {'center_x': 0.5, 'y': 0.75}  
        qcorner_image_layout.add_widget(qcorner_title)


        """

        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.4, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source='red circle.png', size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = 'Down Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = 'Up Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)

        """
       
        score_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        score_layout.pos_hint = {'center_x': 0.75, 'top': 0.82}  # Position layout in the upper right-hand corner
        self.add_widget(score_layout)

        score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        score_image.pos_hint = {'center_x': 0.5, 'center_y': 0.25}  # Center the image within its layout
        score_layout.add_widget(score_image)

        self.score_label = Label(text=str(hs2) + '/' + str(hs1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.score_label.pos_hint = {'center_x': 0.5, 'y': 0.2}  # Position the label just above the image
        score_layout.add_widget(self.score_label)

        score_title = Label(text = "Your Score:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        score_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        score_layout.add_widget(score_title)

        qscore_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        qscore_layout.pos_hint = {'center_x': 0.91, 'top': 0.82}  # Position layout in the upper right-hand corner
        self.add_widget(qscore_layout)

        qscore_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qscore_image.pos_hint = {'center_x': 0.5, 'center_y': 0.25}  # Center the image within its layout
        qscore_layout.add_widget(qscore_image)

        self.qscore_label = Label(text=str(qs2) + '/' + str(qs1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.qscore_label.pos_hint = {'center_x': 0.5, 'y': 0.2}  # Position the label just above the image
        qscore_layout.add_widget(self.qscore_label)

        qscore_title = Label(text = "Quantum Computer \n Score:", font_size = 25, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        qscore_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        qscore_layout.add_widget(qscore_title)

        mode_layout = FloatLayout(size_hint=(None, None), size=(300, 200))
        mode_layout.pos_hint = {'center_x': 0.3, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(mode_layout)

        mode_title = Label(text = 'Select Game Mode:', font_size = 30)
        mode_title.pos_hint = {'center_x': 0.5, 'center_y':0.75}
        mode_layout.add_widget(mode_title)

        self.mode_sel = Spinner(text =gm, values = ('Easy', 'Medium', 'Hard'), size_hint=(None, None), size=(200, 44))
        self.mode_sel.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        self.mode_sel.bind(text=self.mode_select)  
        mode_layout.add_widget(self.mode_sel) 

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)
        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.83, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "See Summary", size = (250, 100), size_hint = (None, None))
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

        self.quip_layout = FloatLayout(size_hint = (1, 1))
        self.quip_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.quip_layout)
        
        self.res_layout = FloatLayout(size_hint = (0.8, 0.8))
        self.res_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.res_layout)

        

    

    def check_state(self, instance):
        bin=[]
        for ds in self.Bs:
            s = ds.get_state()
            if s:
                bin.append(1)
            else:
                bin.append(0)

        if self.bol:
            output = f(bin, self.half_num)
        else:
            output = 0
    
        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))
        self.snum = self.snum +1
        self.corner_label.text = str(self.snum)

    def splash_remove(self, splash, block):
        self.remove_widget(block)
        self.res_layout.remove_widget(splash)

    def Fair_check(self, instance):
        global hs1, hs2, hscore_result
        if not self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                hscore_result.append([self.bits, att, res])
                hs1 = hs1 +1
                hs2 = hs2 +1
                self.score_label.text = str(hs2) + '/' + str(hs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)

                self.pressed= True

        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                hscore_result.append([self.bits, att, res])
                hs1 = hs1 +1
                self.score_label.text = str(hs2) + '/' + str(hs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)

                self.pressed= True
        
    def Biased_check(self, instance):
        global hs1, hs2, hscore_result
        if self.bol:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)



            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                hscore_result.append([self.bits, att, res])
                hs1 = hs1 +1
                hs2 = hs2 +1
                self.score_label.text = str(hs2) + '/' + str(hs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)
                
                self.pressed= True
        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                hscore_result.append([self.bits, att, res])
                hs1 = hs1 +1
                self.score_label.text = str(hs2) + '/' + str(hs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)

                self.pressed= True

    def QC_run(self):
        def g(x):
            if self.bol:
                return f(x, self.half_num)
            else:
                return 0

        def Uf_man(state_list, n):
            Uf = QuantumCircuit(n+1)
            for bs in state_list:
                Uf.barrier()
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.mcx(list(range(n)), n)
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.barrier()
            return Uf
        
        def Uf(n):
    
            states_set=[[0]*(n+1)]


            for i in range((2**(n+1))-1):
                temp = states_set[-1].copy() 
                states_set.append(binary_increment(temp))

            Uf_array=[]

            for i in range(2**(n+1)):
                Uf_array.append([0]*(2**(n+1)))
        
            for i in range(len(states_set)):
            
                w = g(states_set[i][1:len(states_set)-1])

                if w==0:
                    Uf_array[i][i]=1
                if w==1:
                    if states_set[i][0]==0:
                        Uf_array[i][i+2**(n)]=1
                    if states_set[i][0]==1:
                        Uf_array[i][i-2**(n)]=1
                
            Uf_array = np.array(Uf_array)
            Uf_gate = Operator(Uf_array)
            
            return Uf_gate


        def Deutsch_J(n):
            dj = QuantumCircuit(n+1, n)
            dj.x(n)
            for i in range(n+1):
                dj.h(i)
            
            dj.barrier()
            dj.unitary(Uf(n), range(n+1))
            #dj.cx(0, 1)
            dj.barrier()

            for i in range(n):
                dj.h(i)
            
            return dj

        DJ = Deutsch_J(self.bits)
        DJ.measure([i for i in range(self.bits)], [i for i in range(self.bits)])


        backend = AerSimulator()
        DJ_compiled = transpile(DJ, backend)

        job_sim = backend.run(DJ_compiled, shots=1024)

        result_sim = job_sim.result()

        counts = result_sim.get_counts(DJ_compiled)

        print(counts)

        c=1

        zer = ''
        for i in range(self.bits):
            zer = zer + '0'

        if zer in counts:
            c=0

        if c==0:
            self.QC_label.text = "Output: \n Fair!"
        if c==1:
            self.QC_label.text = "Output: \n Biased!"
        

        self.qnum = self.qnum + 1
        self.qcorner_label.text = str(self.qnum)

    def QC_res(self):
        global qs1, qs2, qscore_result
        if not self.bol:
            if  self.QC_label.text == "Output: \n Fair!":
                Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
                Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
                self.res_layout.add_widget(Cor)
                overlay = Widget(size=self.size, pos=self.pos, opacity=0)
                overlay.bind(on_touch_down=lambda *args: None)
                self.add_widget(overlay)

                Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)

                qatt = int(self.qcorner_label.text)
                qres = True
                qscore_result.append([self.bits, qatt, qres])
                qs1 = qs1 +1
                qs2 = qs2 +1
                self.qscore_label.text = str(qs2) + '/' + str(qs1)

            else:
                Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
                Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
                self.res_layout.add_widget(Fal)
                overlay = Widget(size=self.size, pos=self.pos, opacity=0)
                overlay.bind(on_touch_down=lambda *args: None)
                self.add_widget(overlay)

                Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

                qatt = int(self.qcorner_label.text)
                qres = False
                qscore_result.append([self.bits, qatt, qres])
                qs1 = qs1 +1
                self.qscore_label.text = str(qs2) + '/' + str(qs1)
        else:
            if  self.QC_label.text == "Output: \n Biased!":
                Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
                Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
                self.res_layout.add_widget(Cor)
                overlay = Widget(size=self.size, pos=self.pos, opacity=0)
                overlay.bind(on_touch_down=lambda *args: None)
                self.add_widget(overlay)

                Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)

                qatt = int(self.qcorner_label.text)
                qres = True
                qscore_result.append([self.bits, qatt, qres])
                qs1 = qs1 +1
                qs2 = qs2 +1
                self.qscore_label.text = str(qs2) + '/' + str(qs1)

            else:
                Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
                Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
                self.res_layout.add_widget(Fal)
                overlay = Widget(size=self.size, pos=self.pos, opacity=0)
                overlay.bind(on_touch_down=lambda *args: None)
                self.add_widget(overlay)

                Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

                qatt = int(self.qcorner_label.text)
                qres = False
                qscore_result.append([self.bits, qatt, qres])
                qs1 = qs1 +1
                self.qscore_label.text = str(qs2) + '/' + str(qs1)

    def Empty_Qtext(self):
        self.QC_label.text = ""
        
    def QC_turn(self):
        overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
        overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
        self.add_widget(overlay)
    

        quipimg = Image(source = self.quip, size_hint = (None, None), size = (300, 200), pos_hint = {'center_x':0.8, 'center_y':0.5})
        self.quip_layout.add_widget(quipimg)

        Clock.schedule_once(lambda dt: self.QC_run(), 2)
        Clock.schedule_once(lambda dt: self.QC_res(), 3)
        Clock.schedule_once(lambda dt: self.quip_layout.remove_widget(quipimg), 4)
        Clock.schedule_once(lambda dt: self.Empty_Qtext(), 4)
        Clock.schedule_once(lambda dt: self.remove_widget(overlay), 4)

    def mode_select(self, mode_sel, text):
        global hs1, hs2, hscore_result, qs1, qs2, qscore_result

        hs1 =0
        hs2 =0
        hscore_result=[]

        qs1 =0
        qs2 =0
        qscore_result=[]

        if text == 'Easy' and (self.gmc != 'Easy'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
            new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=5)
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_Quantum_New'

            sm.transition = original_transition
        
        if text == 'Medium' and (self.gmc != 'Medium'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
            new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=8, gm='Medium')
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_Quantum_New'

            sm.transition = original_transition
        
        if text == 'Hard' and (self.gmc != 'Hard'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
            new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=12, gm ='Hard')
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_Quantum_New'

            sm.transition = original_transition
        
    

    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
                
        new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'DJ_Quantum_New'

        sm.transition = original_transition
    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
                
            new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'DJ_Quantum_New'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
            new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'DJ_Quantum_New'

            sm.transition = original_transition

    def prev_screen(self, instance):
        global qs1, qs2, qscore_result
        qs1 =0
        qs2 =0
        qscore_result=[]
        self.manager.current = 'article3'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.remove_widget(sm.get_screen('DJ_Quantum_Summary'))
            
        new_dj_sum = DJ_Quantum_Summary(name='DJ_Quantum_Summary')
        sm.add_widget(new_dj_sum)
            
        sm.current = 'DJ_Quantum_Summary'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'



class DJ_Quantum_Summary(Screen):
    def __init__(self, **kwargs):
        super(DJ_Quantum_Summary, self).__init__(**kwargs)

        global qscore_result
        print(qscore_result)
        
        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)
        
        

        sum_layout = BoxLayout(orientation='vertical', size_hint = (1, 1), spacing = 50, padding = [40, 30, 40, 30])
        self.add_widget(sum_layout)

        Title = Label(text = 'Summary of Results: ', font_size=70, size_hint_y=None, height=100)
        sum_layout.add_widget(Title)

        
        Num_layout = GridLayout(cols=2, size_hint_y=0.12)
        sum_layout.add_widget(Num_layout)

        score_layout = FloatLayout(size_hint=(1, 1))
        score_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(score_layout)

        Score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        Score_image.pos_hint = {'center_x': 0.8, 'center_y': 0.35}  # Center the image within its layout
        score_layout.add_widget(Score_image)

        if hs1==0:
            P =0
        else:
            P = int((hs2/hs1)*100)

        Perscore = Label(text=str(P) + '%', font_size=60, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        Perscore.pos_hint = {'center_x': 0.8, 'center_y': 0.32}  # Position the label just above the image
        score_layout.add_widget(Perscore)

        Perscore_title = Label(text = "Your Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Perscore_title.pos_hint = {'center_x': 0.3, 'y': 0.35}  
        score_layout.add_widget(Perscore_title)

        qscore_layout = FloatLayout(size_hint=(1, 1))
        qscore_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(qscore_layout)

        qScore_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qScore_image.pos_hint = {'center_x': 0.8, 'center_y': 0.35}  # Center the image within its layout
        qscore_layout.add_widget(qScore_image)

        if qs1==0:
            qP =0
        else:
            qP = int((qs2/qs1)*100)

        qPerscore = Label(text=str(qP) + '%', font_size=60, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        qPerscore.pos_hint = {'center_x': 0.8, 'center_y': 0.32}  # Position the label just above the image
        qscore_layout.add_widget(qPerscore)

        qPerscore_title = Label(text = "Qunatum Computer Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        qPerscore_title.pos_hint = {'center_x': 0.3, 'y': 0.35}  
        qscore_layout.add_widget(qPerscore_title)

        Grp_layout = GridLayout(cols=2, size_hint_y=0.4)
        sum_layout.add_widget(Grp_layout)

        hsno = [str(x) for x in range(1, len(hscore_result)+1)]
        hatt = []
        hcol =[]
        for x in hscore_result:
            hatt.append(x[1])
            if x[2]:
                hcol.append('green')
            else:
                hcol.append('red')
        
        hatt_c =[]
        for x in hscore_result:
            if x[2]:
                hatt_c.append(x[1])

        if len(hatt_c)>0:
            hatt_avg = sum(hatt_c)/len(hatt_c)
        
        fig, ax = plt.subplots()

        ax.bar(hsno, hatt, color = hcol)
        ax.set_title('Your Attempts')
        ax.set_ylabel('Number of Attempts Taken')
        ax.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(hatt_c)>0:
            avgline = ax.axhline(y=hatt_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax.legend(handles=legend_patches)
        if len(hatt)>0:
            ax.set_ylim(0, 1.2*max(hatt))
            ax.set_yticks(range(max(hatt)+1))
        
        
        himg = MatplotlibImage(fig, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        Grp_layout.add_widget(himg)

        qsno = [str(x) for x in range(1, len(qscore_result)+1)]
        qatt = []
        qcol =[]
        for x in qscore_result:
            qatt.append(x[1])
            if x[2]:
                qcol.append('green')
            else:
                qcol.append('red')
        
        qatt_c =[]
        for x in qscore_result:
            if x[2]:
                qatt_c.append(x[1])

        if len(qatt_c)>0:
            qatt_avg = sum(qatt_c)/len(qatt_c)
        
        fig1, ax1 = plt.subplots()

        ax1.bar(qsno, qatt, color = qcol)
        ax1.set_title('Quantum Computer Attempts')
        ax1.set_ylabel('Number of Attempts Taken')
        ax1.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(qatt_c)>0:
            avgline = ax1.axhline(y=qatt_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax1.legend(handles=legend_patches)
        if len(qatt)>0:
            ax1.set_ylim(0, 1.2*max(hatt))
            ax1.set_yticks(range(max(hatt)+1))

        qimg = MatplotlibImage(fig1, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        Grp_layout.add_widget(qimg)

        Bgrid = GridLayout(cols = 1, size_hint_y =0.15)
        sum_layout.add_widget(Bgrid)

        Bitnum_layout = FloatLayout(size_hint=(1, 0.5))
        Bitnum_layout.pos_hint = {'center_x':0.5, 'center_y': 0.75}  # Position layout in the upper right-hand corner
        Bgrid.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(150, 150))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.85}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        if len(hscore_result)==0:
            B=0
        else:
            B = hscore_result[0][0]

        self.Bitnum = Label(text=str(B), font_size=70, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'center_y': 0.82}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0.35, 'y': 0.85}  
        Bitnum_layout.add_widget(Bitnum_title)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)
        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Play Again", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

    def prev_screen(self, instance):
        global qs1, qs2, qscore_result, hs1, hs2, hscore_result
        qs1 =0
        qs2 =0
        qscore_result=[]
        hs1 =0
        hs2 =0
        hscore_result=[]
        sm = self.manager 

        sm.remove_widget(sm.get_screen('DJ_Quantum_New'))
            
        new_dj_game = DJ_Quantum_New(name='DJ_Quantum_New')
        sm.add_widget(new_dj_game)
        
        sm.current = 'DJ_Quantum_New'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.current = 'article4'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class BV_game(Screen):
    def __init__(self, n=5, gm = 'Easy', **kwargs):
        super(BV_game, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bits = n

        self.gmc =gm

        self.s = random.choice(states_set(n))
        self.snum = 0
        self.pressed = False

        



        # Horizontal GridLayout for images
        #image_grid = GridLayout(cols=5, size_hint_y=None, height=700)
        #self.add_widget(image_grid)
        image_grid = GridLayout(cols=n, size_hint_y=None, height=700)
        image_grid.size_hint = (0.55, 0.6)
        #image_grid.width = 1000  # Adjust width as needed
        image_grid.pos_hint = {'x': 0.05, 'top': 0.7}
        self.add_widget(image_grid)

        # Create images and add them to the image grid layout
        self.Bs = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs.append(dual_state_image)
            image_grid.add_widget(dual_state_image)

        #condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        #self.add_widget(condition_layout)

        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.6, 'center_y': 0.5}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check Reaction", size=(230, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        #button_grid = GridLayout(cols=1, size_hint_y=None, height=500)
        #self.add_widget(button_grid)

        button_grid = GridLayout(cols=1, size_hint_y=None, height=350, spacing = 20)
        button_grid.size_hint = (0.15, 0.25)
        button_grid.width = 300
        button_grid.pos_hint = {'x': 0.85, 'y': 0.23}
        self.add_widget(button_grid)

        self.result_label = Label(text="", font_size=48, color=(1, 0, 0, 1), size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.text_input = TextInput(
            hint_text="Guess of s",  # Placeholder text
            font_size=20,  # Font size
            size_hint=(None, None),  # Set fixed size
            width=200,
            height=50,
            multiline=False  # Single-line text input
        )
        button_grid.add_widget(self.text_input)

        self.biased = Button(text="Check Answer", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Biased_check)
        button_grid.add_widget(self.biased)

        self.restart_button = Button(text="Play Again", size_hint=(None, None), size=(200, 100))
        self.restart_button.bind(on_press=self.restart)
        button_grid.add_widget(self.restart_button)

        corner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        corner_image_layout.pos_hint = {'right': 1, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(corner_image_layout)

        corner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        corner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        corner_image_layout.add_widget(corner_image)

        self.corner_label = Label(text="0", font_size=100, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.corner_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        corner_image_layout.add_widget(self.corner_label)

        corner_title = Label(text = "Number of Attempts:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        corner_title.pos_hint = {'center_x': 0.5, 'y': 0.7}  
        corner_image_layout.add_widget(corner_title)
        """
        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.5, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source='red circle.png', size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = 'Down Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = 'Up Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)
        """

       
        score_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        score_layout.pos_hint = {'right': 1, 'top': 0.8}  # Position layout in the upper right-hand corner
        self.add_widget(score_layout)

        score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        score_image.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Center the image within its layout
        score_layout.add_widget(score_image)

        self.score_label = Label(text=str(s2) + '/' + str(s1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.score_label.pos_hint = {'center_x': 0.5, 'y': 0.24}  # Position the label just above the image
        score_layout.add_widget(self.score_label)

        score_title = Label(text = "Overall Score:", font_size = 40, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        score_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        score_layout.add_widget(score_title)
        
        mode_layout = FloatLayout(size_hint=(None, None), size=(300, 200))
        mode_layout.pos_hint = {'center_x': 0.3, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(mode_layout)

        mode_title = Label(text = 'Select Game Mode:', font_size = 30)
        mode_title.pos_hint = {'center_x': 0.5, 'center_y':0.75}
        mode_layout.add_widget(mode_title)

        self.mode_sel = Spinner(text =gm, values = ('Easy', 'Medium', 'Hard'), size_hint=(None, None), size=(200, 44))
        self.mode_sel.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        self.mode_sel.bind(text=self.mode_select)  
        mode_layout.add_widget(self.mode_sel) 

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)


        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "See Summary", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)


        self.res_layout = FloatLayout(size_hint = (0.8, 0.8))
        self.res_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.res_layout)




        

       
    def check_state(self, instance):
        bin=[]
        for ds in self.Bs:
            s = ds.get_state()
            if s:
                bin.append(1)
            else:
                bin.append(0)

        output = fs(bin, self.s)

        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))

        self.snum = self.snum + 1
        self.corner_label.text = str(self.snum)
        #return output

        
    def Biased_check(self, instance):
        global bvs1, bvs2, bvscore_result

        sg = self.text_input.text
        ss = ''
        for i in range(len(self.s)):
            ss = ss + str(self.s[i])

        if sg==ss:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Cor), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                bvscore_result.append([self.bits, att, res])
                bvs1 = bvs1 +1
                bvs2 = bvs2 +1
                self.score_label.text = str(bvs2) + '/' + str(bvs1)

                self.pressed= True
        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)

            Clock.schedule_once(lambda dt: self.res_layout.remove_widget(Fal), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                bvscore_result.append([self.bits, att, res])
                bvs1 = bvs1 +1
                self.score_label.text = str(bvs2) + '/' + str(bvs1)

                self.pressed= True

    def mode_select(self, mode_sel,  text):
        global bvs1, bvs2, bvscore_result
        if (text == 'Easy') and (self.gmc != 'Easy'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_game'))
            
            new_dj_game = BV_game(name='BV_game', n=5)
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_game'

            sm.transition = original_transition
        
        if (text == 'Medium') and (self.gmc != 'Medium'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_game'))
            
            new_dj_game = BV_game(name='BV_game', n=8, gm='Medium')
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_game'

            sm.transition = original_transition
        
        if text == 'Hard'and (self.gmc != 'Hard'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_game'))
            
            new_dj_game = BV_game(name='BV_game', n=12, gm ='Hard')
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_game'

            sm.transition = original_transition
        bvs1 =0
        bvs2 =0
        bvscore_result=[]

    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('BV_game'))
                
        new_dj_game = BV_game(name='BV_game', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'BV_game'

        sm.transition = original_transition
    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_game'))
                
            new_dj_game = BV_game(name='BV_game', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'BV_game'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_game'))
            
            new_dj_game = BV_game(name='BV_game', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_game'

            sm.transition = original_transition

    def prev_screen(self, instance):
        global bvs1, bvs2, bvscore_result
        bvs1 =0
        bvs2 =0
        bvscore_result=[]
        self.manager.current = 'article6'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.remove_widget(sm.get_screen('BV_Summary'))
            
        new_dj_sum = BV_Summary(name='BV_Summary')
        sm.add_widget(new_dj_sum)
            
        sm.current = 'BV_Summary'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class BV_Summary(Screen):
    def __init__(self, **kwargs):
        super(BV_Summary, self).__init__(**kwargs)

        global bvscore_result
        
        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)
        
        

        sum_layout = BoxLayout(orientation='vertical', size_hint = (1, 1), spacing = 50, padding = [40, 30, 40, 30])
        self.add_widget(sum_layout)

        Title = Label(text = 'Summary of Results: ', font_size=70, size_hint_y=None, height=100)
        sum_layout.add_widget(Title)

        
        Num_layout = GridLayout(cols=2, size_hint_y=0.1)
        sum_layout.add_widget(Num_layout)

        score_layout = FloatLayout(size_hint=(1, 1))
        score_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(score_layout)

        Score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(200, 200))
        Score_image.pos_hint = {'center_x': 0.8, 'center_y': 0.05}  # Center the image within its layout
        score_layout.add_widget(Score_image)

        if bvs1==0:
            P =0
        else:
            P = int((bvs2/bvs1)*100)

        Perscore = Label(text=str(P) + '%', font_size=80, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        Perscore.pos_hint = {'center_x': 0.8, 'center_y': 0.02}  # Position the label just above the image
        score_layout.add_widget(Perscore)

        Perscore_title = Label(text = "Total Accuracy Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Perscore_title.pos_hint = {'center_x': 0.3, 'y': 0.05}  
        score_layout.add_widget(Perscore_title)

        Bitnum_layout = FloatLayout(size_hint=(1, 1))
        Bitnum_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(200, 200))
        Bitnum_image.pos_hint = {'center_x': 0.8, 'center_y': 0.05}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        if len(bvscore_result)==0:
            B=0
        else:
            B = bvscore_result[0][0]

        self.Bitnum = Label(text=str(B), font_size=70, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.8, 'center_y': 0.02}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0.35, 'y': 0.05}  
        Bitnum_layout.add_widget(Bitnum_title)

        
        sno = [str(x) for x in range(1, len(bvscore_result)+1)]
        att = []
        col =[]
        for x in bvscore_result:
            att.append(x[1])
            if x[2]:
                col.append('green')
            else:
                col.append('red')
        
        att_c =[]
        for x in bvscore_result:
            if x[2]:
                att_c.append(x[1])

        if len(att_c)>0:
            att_avg = sum(att_c)/len(att_c)
        
        fig, ax = plt.subplots()

        ax.bar(sno, att, color = col)
        ax.set_title('Number of Attempts Taken')
        ax.set_ylabel('Number of Attempts Taken')
        ax.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(att_c)>0:
            avgline = ax.axhline(y=att_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax.legend(handles=legend_patches)
        if len(att)>0:
            ax.set_ylim(0, 1.2*max(att))
            ax.set_yticks(range(max(att)+1))
        
        
        img = MatplotlibImage(fig, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        sum_layout.add_widget(img)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)

        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Play Again", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

    def prev_screen(self, instance):
        global bvs1, bvs2, bvscore_result
        bvs1 =0
        bvs2 =0
        bvscore_result=[]
        sm = self.manager 

        sm.remove_widget(sm.get_screen('BV_game'))
            
        new_dj_game = BV_game(name='BV_game')
        sm.add_widget(new_dj_game)
        
        sm.current = 'BV_game'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.current = 'article7'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

    

class BV_Quantum(Screen):
    def __init__(self, n=5, gm = 'Easy', **kwargs):
        super(BV_Quantum, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (0.82, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bits = n

        self.s = random.choice(states_set(n))
        self.snum = 0
        self.qnum =0
        self.pressed = False

        self.gmc = gm

        quips = [resource_path('assets/quip 1.png'), resource_path('assets/quip 2.png'), resource_path('assets/quip 3.png'), resource_path('assets/quip 4.png')]
        self.quip = random.choice(quips)

        # Horizontal GridLayout for images
        #image_grid = GridLayout(cols=5, size_hint_y=None, height=700)
        #self.add_widget(image_grid)
        image_grid = GridLayout(cols=n, size_hint_y=None, height=700)
        image_grid.size_hint = (0.45, 0.6)
        #image_grid.width = 1000  # Adjust width as needed
        image_grid.pos_hint = {'x': 0.05, 'y': 0.05}
        self.add_widget(image_grid)

        # Create images and add them to the image grid layout
        self.Bs = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs.append(dual_state_image)
            image_grid.add_widget(dual_state_image)

        #condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        #self.add_widget(condition_layout)

        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.5, 'center_y': 0.5}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check State", size=(200, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        Q_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        Q_layout.size_hint = (0.15, 0.5)
        #Q_layout.height = 1000
        Q_layout.pos_hint = {'x': 0.85, 'center_y': 0.35}
        self.add_widget(Q_layout)


        self.QC_image = Image(source=resource_path('assets/QC image1.png'))
        Q_layout.add_widget(self.QC_image)

        self.QC_label = Label(text="", font_size=48, color=(0, 0, 1, 1), size_hint_y=None, height=100)
        Q_layout.add_widget(self.QC_label)

        button_grid = GridLayout(cols=1, size_hint_y=None, height=350, spacing = 20)
        button_grid.size_hint = (0.15, 0.3)
        button_grid.width = 300
        button_grid.pos_hint = {'x': 0.67, 'y': 0.23}
        self.add_widget(button_grid)

        self.result_label = Label(text="", font_size=48, color=(1, 0, 0, 1), size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.text_input = TextInput(
            hint_text="Guess of s",  # Placeholder text
            font_size=20,  # Font size
            size_hint=(None, None),  # Set fixed size
            width=200,
            height=50,
            multiline=False  # Single-line text input
        )
        button_grid.add_widget(self.text_input)

        self.biased = Button(text="Check Answer", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Biased_check)
        button_grid.add_widget(self.biased)

        self.restart_button = Button(text="Play Again", size_hint=(None, None), size=(200, 100))
        self.restart_button.bind(on_press=self.restart)
        button_grid.add_widget(self.restart_button)

        corner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        corner_image_layout.pos_hint = {'center_x': 0.75, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(corner_image_layout)

        corner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        corner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Center the image within its layout
        corner_image_layout.add_widget(corner_image)

        self.corner_label = Label(text="0", font_size=80, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.corner_label.pos_hint = {'center_x': 0.5, 'y': 0.34}  # Position the label just above the image
        corner_image_layout.add_widget(self.corner_label)

        corner_title = Label(text = "Your Attempts:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        corner_title.pos_hint = {'center_x': 0.5, 'y': 0.75}  
        corner_image_layout.add_widget(corner_title)

        qcorner_image_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        qcorner_image_layout.pos_hint = {'center_x': 0.91, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(qcorner_image_layout)

        qcorner_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qcorner_image.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Center the image within its layout
        qcorner_image_layout.add_widget(qcorner_image)

        self.qcorner_label = Label(text="0", font_size=80, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.qcorner_label.pos_hint = {'center_x': 0.5, 'y': 0.34}  # Position the label just above the image
        qcorner_image_layout.add_widget(self.qcorner_label)

        qcorner_title = Label(text = "Quantum Computer \n Attempts:", font_size = 25, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        qcorner_title.pos_hint = {'center_x': 0.5, 'y': 0.75}  
        qcorner_image_layout.add_widget(qcorner_title)


        """

        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.4, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source='red circle.png', size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = 'Down Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = 'Up Button.png', size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)

        """
       
        score_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        score_layout.pos_hint = {'center_x': 0.75, 'top': 0.82}  # Position layout in the upper right-hand corner
        self.add_widget(score_layout)

        score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        score_image.pos_hint = {'center_x': 0.5, 'center_y': 0.25}  # Center the image within its layout
        score_layout.add_widget(score_image)

        self.score_label = Label(text=str(hbvs2) + '/' + str(hbvs1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.score_label.pos_hint = {'center_x': 0.5, 'y': 0.2}  # Position the label just above the image
        score_layout.add_widget(self.score_label)

        score_title = Label(text = "Your Score:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        score_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        score_layout.add_widget(score_title)

        qscore_layout = FloatLayout(size_hint=(None, None), size=(300, 300))
        qscore_layout.pos_hint = {'center_x': 0.91, 'top': 0.82}  # Position layout in the upper right-hand corner
        self.add_widget(qscore_layout)

        qscore_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qscore_image.pos_hint = {'center_x': 0.5, 'center_y': 0.25}  # Center the image within its layout
        qscore_layout.add_widget(qscore_image)

        self.qscore_label = Label(text=str(qbvs2) + '/' + str(qbvs1), font_size=70, color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 50))
        self.qscore_label.pos_hint = {'center_x': 0.5, 'y': 0.2}  # Position the label just above the image
        qscore_layout.add_widget(self.qscore_label)

        qscore_title = Label(text = "Quantum Computer \n Score:", font_size = 25, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50), halign = 'center')
        qscore_title.pos_hint = {'center_x': 0.5, 'y': 0.6}  
        qscore_layout.add_widget(qscore_title)

        mode_layout = FloatLayout(size_hint=(None, None), size=(300, 200))
        mode_layout.pos_hint = {'center_x': 0.3, 'top': 1}  # Position layout in the upper right-hand corner
        self.add_widget(mode_layout)

        mode_title = Label(text = 'Select Game Mode:', font_size = 30)
        mode_title.pos_hint = {'center_x': 0.5, 'center_y':0.75}
        mode_layout.add_widget(mode_title)

        self.mode_sel = Spinner(text =gm, values = ('Easy', 'Medium', 'Hard'), size_hint=(None, None), size=(200, 44))
        self.mode_sel.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        self.mode_sel.bind(text=self.mode_select)  
        mode_layout.add_widget(self.mode_sel) 

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)

        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "See Summary", size = (250, 100), size_hint = (None, None))
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

        self.quip_layout = FloatLayout(size_hint = (1, 1))
        self.quip_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.quip_layout)

        self.res_layout = FloatLayout(size_hint = (0.8, 0.8))
        self.res_layout.pos_hint={'center_x':0.5, 'center_y':0.5}
        self.add_widget(self.res_layout)

        

    def check_state(self, instance):
        bin=[]
        for ds in self.Bs:
            s = ds.get_state()
            if s:
                bin.append(1)
            else:
                bin.append(0)

        output = fs(bin, self.s)

        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))
        self.snum = self.snum +1
        self.corner_label.text = str(self.snum)

        #return output

    def splash_remove(self, splash, cover):
        self.remove_widget(cover)
        self.res_layout.remove_widget(splash)
        
    def Biased_check(self, instance):
        global hbvs1, hbvs2, hbvscore_result

        sg = self.text_input.text
        ss = ''
        for i in range(len(self.s)):
            ss = ss + str(self.s[i])

        if sg==ss:
            
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)


            if not self.pressed:
                att = int(self.corner_label.text)
                res = True
                hbvscore_result.append([self.bits, att, res])
                hbvs1 = hbvs1 +1
                hbvs2 = hbvs2 +1
                self.score_label.text = str(hbvs2) + '/' + str(hbvs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)

                self.pressed= True
        else: 
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
            overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

            if not self.pressed:
                att = int(self.corner_label.text)
                res = False
                hbvscore_result.append([self.bits, att, res])
                hbvs1 = hbvs1 +1
                self.score_label.text = str(hbvs2) + '/' + str(hbvs1)

                Clock.schedule_once(lambda dt: self.QC_turn(), 1.2)

                self.pressed= True

    def QC_run(self):

        def Uf_man(state_list, n):
            Uf = QuantumCircuit(n+1)
            for bs in state_list:
                Uf.barrier()
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.mcx(list(range(n)), n)
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.barrier()
            return Uf
        
        def Uf(n):
    
            states_set=[[0]*(n+1)]


            for i in range((2**(n+1))-1):
                temp = states_set[-1].copy() 
                states_set.append(binary_increment(temp))

            Uf_array=[]

            for i in range(2**(n+1)):
                Uf_array.append([0]*(2**(n+1)))
        
            for i in range(len(states_set)):
            
                w = fs(states_set[i][1:len(states_set)-1], self.s)

                if w==0:
                    Uf_array[i][i]=1
                if w==1:
                    if states_set[i][0]==0:
                        Uf_array[i][i+2**(n)]=1
                    if states_set[i][0]==1:
                        Uf_array[i][i-2**(n)]=1
                
            Uf_array = np.array(Uf_array)
            Uf_gate = Operator(Uf_array)
            
            return Uf_gate


        def Deutsch_J(n):
            dj = QuantumCircuit(n+1, n)
            dj.x(n)
            for i in range(n+1):
                dj.h(i)
            
            dj.barrier()
            dj.unitary(Uf(n), range(n+1))
            #dj.cx(0, 1)
            dj.barrier()

            for i in range(n):
                dj.h(i)
            
            return dj

        DJ = Deutsch_J(self.bits)
        DJ.measure([i for i in range(self.bits)], [i for i in range(self.bits)])


        backend = AerSimulator()
        DJ_compiled = transpile(DJ, backend)

        job_sim = backend.run(DJ_compiled, shots=1024)

        result_sim = job_sim.result()

        counts = result_sim.get_counts(DJ_compiled)

        s = list(counts.keys())[0]

        self.QC_label.text = 'Output: \n' + str(s)

        self.qnum = self.qnum + 1
        self.qcorner_label.text = str(self.qnum)
        
    def QC_res(self):
        global qbvs1, qbvs2, qbvscore_result
        ss = ''
        for i in range(len(self.s)):
            ss = ss + str(self.s[i])

        if  self.QC_label.text == "Output: \n" + str(ss):
            Cor = Image(source=resource_path('assets/correct splash.png'), size_hint=(1, 1))
            Cor.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Cor)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Cor, overlay), 1)

            qatt = int(self.qcorner_label.text)
            qres = True
            qbvscore_result.append([self.bits, qatt, qres])
            qbvs1 = qbvs1 +1
            qbvs2 = qbvs2 +1
            self.qscore_label.text = str(qbvs2) + '/' + str(qbvs1)

        else:
            Fal = Image(source=resource_path('assets/false splash.png'), size_hint=(1, 1))
            Fal.pos_hint= {'center_x':0.5, 'center_y':0.5}
            self.res_layout.add_widget(Fal)
            overlay = Widget(size=self.size, pos=self.pos, opacity=0)
            overlay.bind(on_touch_down=lambda *args: None)
            self.add_widget(overlay)

            Clock.schedule_once(lambda dt: self.splash_remove(Fal, overlay), 1)

            qatt = int(self.qcorner_label.text)
            qres = False
            qbvscore_result.append([self.bits, qatt, qres])
            qbvs1 = qbvs1 +1
            self.qscore_label.text = str(qbvs2) + '/' + str(qbvs1)
        

    def Empty_Qtext(self):
        self.QC_label.text = ""
        
    def QC_turn(self):
        overlay = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, opacity=0)
        overlay.bind(on_touch_down=lambda *args: True)  # Block all touches
        self.add_widget(overlay)
    

        quipimg = Image(source = self.quip, size_hint = (None, None), size = (300, 200), pos_hint = {'center_x':0.8, 'center_y':0.5})
        self.quip_layout.add_widget(quipimg)

        Clock.schedule_once(lambda dt: self.QC_run(), 2)
        Clock.schedule_once(lambda dt: self.QC_res(), 3)
        Clock.schedule_once(lambda dt: self.quip_layout.remove_widget(quipimg), 4)
        Clock.schedule_once(lambda dt: self.Empty_Qtext(), 4)
        Clock.schedule_once(lambda dt: self.remove_widget(overlay), 4)

    def mode_select(self, mode_sel, text):
        global hs1, hs2, hscore_result, qs1, qs2, qscore_result

        hs1 =0
        hs2 =0
        hscore_result=[]

        qs1 =0
        qs2 =0
        qscore_result=[]

        if text == 'Easy' and (self.gmc != 'Easy'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_Quantum'))
            
            new_dj_game =BV_Quantum(name='BV_Quantum', n=5)
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_Quantum'

            sm.transition = original_transition
        
        if text == 'Medium' and (self.gmc != 'Medium'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_Quantum'))
            
            new_dj_game = BV_Quantum(name='BV_Quantum', n=8, gm='Medium')
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_Quantum'

            sm.transition = original_transition
        
        if text == 'Hard' and (self.gmc != 'Hard'):

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_Quantum'))
            
            new_dj_game = BV_Quantum(name='BV_Quantum', n=12, gm ='Hard')
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_Quantum'

            sm.transition = original_transition

    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('BV_Quantum'))
                
        new_dj_game = BV_Quantum(name='BV_Quantum', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'BV_Quantum'

        sm.transition = original_transition
    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_Quantum'))
                
            new_dj_game = BV_Quantum(name='BV_Quantum', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'BV_Quantum'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_Quantum'))
            
            new_dj_game = BV_Quantum(name='BV_Quantum', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_Quantum'

            sm.transition = original_transition

    def prev_screen(self, instance):
        global qbvs1, qbvs2, qbvscore_result, hbvs1, hbvs2, hbvscore_result
        qbvs1 =0
        qbvs2 =0
        qbvscore_result=[]
        hbvs1 =0
        hbvs2 =0
        hbvscore_result=[]
        self.manager.current = 'article7'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.remove_widget(sm.get_screen('BV_Quantum_Summary'))
            
        new_dj_sum = BV_Quantum_Summary(name='BV_Quantum_Summary')
        sm.add_widget(new_dj_sum)
            
        sm.current = 'BV_Quantum_Summary'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'

class BV_Quantum_Summary(Screen):
    def __init__(self, **kwargs):
        super(BV_Quantum_Summary, self).__init__(**kwargs)

        global qbvscore_result
        
        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)
        
        

        sum_layout = BoxLayout(orientation='vertical', size_hint = (1, 1), spacing = 50, padding = [40, 30, 40, 30])
        self.add_widget(sum_layout)

        Title = Label(text = 'Summary of Results: ', font_size=70, size_hint_y=None, height=100)
        sum_layout.add_widget(Title)

        
        Num_layout = GridLayout(cols=2, size_hint_y=0.12)
        sum_layout.add_widget(Num_layout)

        score_layout = FloatLayout(size_hint=(1, 1))
        score_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(score_layout)

        Score_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        Score_image.pos_hint = {'center_x': 0.8, 'center_y': 0.35}  # Center the image within its layout
        score_layout.add_widget(Score_image)

        if hbvs1==0:
            P =0
        else:
            P = int((hbvs2/hbvs1)*100)

        Perscore = Label(text=str(P) + '%', font_size=60, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        Perscore.pos_hint = {'center_x': 0.8, 'center_y': 0.32}  # Position the label just above the image
        score_layout.add_widget(Perscore)

        Perscore_title = Label(text = "Your Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Perscore_title.pos_hint = {'center_x': 0.3, 'y': 0.35}  
        score_layout.add_widget(Perscore_title)

        qscore_layout = FloatLayout(size_hint=(1, 1))
        qscore_layout.pos_hint = {'center_x':0.5, 'center_y': 0.5}  # Position layout in the upper right-hand corner
        Num_layout.add_widget(qscore_layout)

        qScore_image = Image(source=resource_path('assets/Green Circile.png'), size_hint=(None, None), size=(150, 150))
        qScore_image.pos_hint = {'center_x': 0.8, 'center_y': 0.35}  # Center the image within its layout
        qscore_layout.add_widget(qScore_image)

        if qbvs1==0:
            qP =0
        else:
            qP = int((qbvs2/qbvs1)*100)

        qPerscore = Label(text=str(qP) + '%', font_size=60, color=(0, 0.7, 0, 1), size_hint=(None, None), size=(100, 100))
        qPerscore.pos_hint = {'center_x': 0.8, 'center_y': 0.32}  # Position the label just above the image
        qscore_layout.add_widget(qPerscore)

        qPerscore_title = Label(text = "Qunatum Computer Score:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        qPerscore_title.pos_hint = {'center_x': 0.3, 'y': 0.35}  
        qscore_layout.add_widget(qPerscore_title)

        Grp_layout = GridLayout(cols=2, size_hint_y=0.4)
        sum_layout.add_widget(Grp_layout)

        hsno = [str(x) for x in range(1, len(hbvscore_result)+1)]
        hatt = []
        hcol =[]
        for x in hbvscore_result:
            hatt.append(x[1])
            if x[2]:
                hcol.append('green')
            else:
                hcol.append('red')
        
        hatt_c =[]
        for x in hbvscore_result:
            if x[2]:
                hatt_c.append(x[1])

        if len(hatt_c)>0:
            hatt_avg = sum(hatt_c)/len(hatt_c)
        
        fig, ax = plt.subplots()

        ax.bar(hsno, hatt, color = hcol)
        ax.set_title('Your Attempts')
        ax.set_ylabel('Number of Attempts Taken')
        ax.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(hatt_c)>0:
            avgline = ax.axhline(y=hatt_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax.legend(handles=legend_patches)
        if len(hatt)>0:
            ax.set_ylim(0, 1.2*max(hatt))
            ax.set_yticks(range(max(hatt)+1))
        
        
        himg = MatplotlibImage(fig, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        Grp_layout.add_widget(himg)

        qsno = [str(x) for x in range(1, len(qbvscore_result)+1)]
        qatt = []
        qcol =[]
        for x in qbvscore_result:
            qatt.append(x[1])
            if x[2]:
                qcol.append('green')
            else:
                qcol.append('red')
        
        qatt_c =[]
        for x in qbvscore_result:
            if x[2]:
                qatt_c.append(x[1])

        if len(qatt_c)>0:
            qatt_avg = sum(qatt_c)/len(qatt_c)
        
        fig1, ax1 = plt.subplots()

        ax1.bar(qsno, qatt, color = qcol)
        ax1.set_title('Quantum Computer Attempts')
        ax1.set_ylabel('Number of Attempts Taken')
        ax1.set_xlabel('Game Number')
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(['green', 'red'], ['Correct Answer', 'False Answer'])]
        if len(qatt_c)>0:
            avgline = ax1.axhline(y=qatt_avg, color='b', linestyle='--', label = 'Average No. of Attempts \nfor Correct Answers')
            legend_patches.append(avgline)
        
        ax1.legend(handles=legend_patches)
        if len(qatt)>0:
            ax1.set_ylim(0, 1.2*max(hatt))
            ax1.set_yticks(range(max(hatt)+1))

        qimg = MatplotlibImage(fig1, size_hint=(1, 1), pos_hint= {'center_x': 0.5, 'y': 0.5})
        Grp_layout.add_widget(qimg)

        Bgrid = GridLayout(cols = 1, size_hint_y =0.15)
        sum_layout.add_widget(Bgrid)

        Bitnum_layout = FloatLayout(size_hint=(1, 0.5))
        Bitnum_layout.pos_hint = {'center_x':0.5, 'center_y': 0.75}  # Position layout in the upper right-hand corner
        Bgrid.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(150, 150))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.85}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        if len(hbvscore_result)==0:
            B=0
        else:
            B = hbvscore_result[0][0]

        self.Bitnum = Label(text=str(B), font_size=70, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'center_y': 0.82}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 45, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0.35, 'y': 0.85}  
        Bitnum_layout.add_widget(Bitnum_title)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)
        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Play Again", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None))
                            #pos_hint = {'center_x': 0.5, 'centre_y': 0.5})
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

    def prev_screen(self, instance):
        global qbvs1,qbvs2, qbvscore_result
        qbvs1 =0
        qbvs2 =0
        qbvscore_result=[]
        sm = self.manager 

        sm.remove_widget(sm.get_screen('BV_Quantum'))
            
        new_dj_game = BV_Quantum(name='BV_Quantum')
        sm.add_widget(new_dj_game)
        
        sm.current = 'BV_Quantum'

    def next_screen(self, instance):
        #self.manager.current = 'DJ_Summary'

        sm = self.manager

        sm.current = 'article8'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'



class BV_demo(Screen):
    def __init__(self, n=5, **kwargs):
        super(BV_demo, self).__init__(**kwargs)

        background_image = Image(source=resource_path('assets/Background 1.jpg'), allow_stretch=True, keep_ratio=False)
        background_image.size_hint = (1, 1)
        background_image.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(background_image)

        self.cols = 1  # One column to stack elements vertically
        self.spacing = 10
        self.padding = [50, 50, 50, 50]

        self.bits = n

        self.s = random.choice(states_set(n))
        self.snum = 0
        self.pressed = False

        

        image_grid1 = GridLayout(cols=n+1, size_hint_y=0.3)
        image_grid1.size_hint = (0.7, 0.6)
        image_grid1.pos_hint = {'x': 0.05, 'top': 0.8}
        self.add_widget(image_grid1)

        t1 = Label(text = 'Batsmens \n Runs: ', font_size = 30, halign = 'center')
        image_grid1.add_widget(t1)

        self.Bs1 = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero wbm.png'), resource_path('assets/one wbm.png'))
            self.Bs1.append(dual_state_image)
            image_grid1.add_widget(dual_state_image)

        t2 = Label(text = 'Secret \n Sequence: ', font_size = 30, halign = 'center')
        image_grid1.add_widget(t2)

        self.Bs2 = []
        for i in range(n):
            dual_state_image = DualStateImage(resource_path('assets/zero button.png'), resource_path('assets/one button.png'))
            self.Bs2.append(dual_state_image)
            image_grid1.add_widget(dual_state_image)



        condition_layout = GridLayout(cols=1, size_hint_x=None, width=300)
        condition_layout.size_hint = (0.2, 0.7)
        #condition_layout.height = 1000
        condition_layout.pos_hint = {'x': 0.75, 'center_y': 0.6}
        self.add_widget(condition_layout)


        self.condition_image = ConditionBasedImage(resource_path('assets/Normal Umpire.png'), resource_path('assets/Dancing Umpire.png'))
        condition_layout.add_widget(self.condition_image)

        self.check_button = Button(text="Check Reaction", size=(230, 100), size_hint=(None, None))
        self.check_button.bind(on_press=self.check_state)
        condition_layout.add_widget(self.check_button)

        #button_grid = GridLayout(cols=1, size_hint_y=None, height=500)
        #self.add_widget(button_grid)

        Bitnum_layout = FloatLayout(size_hint=(None, None), size=(350, 150))
        Bitnum_layout.pos_hint = {'right': 0.5, 'top': 0.2}  # Position layout in the upper right-hand corner
        self.add_widget(Bitnum_layout)

        Bitnum_image = Image(source=resource_path('assets/red circle.png'), size_hint=(None, None), size=(100, 100))
        Bitnum_image.pos_hint = {'center_x': 0.6, 'center_y': 0.75}  # Center the image within its layout
        Bitnum_layout.add_widget(Bitnum_image)

        self.Bitnum = Label(text=str(self.bits), font_size=45, color=(0.7, 0, 0, 1), size_hint=(None, None), size=(100, 100))
        self.Bitnum.pos_hint = {'center_x': 0.6, 'y': 0.45}  # Position the label just above the image
        Bitnum_layout.add_widget(self.Bitnum)

        Bitnum_title = Label(text = "Number of Batsmen:", font_size = 30, color = (1, 1, 1, 1), size_hint = (None, None), size = (300, 50))
        Bitnum_title.pos_hint = {'center_x': 0, 'y': 0.6}  
        Bitnum_layout.add_widget(Bitnum_title)

        Bitnum_Up = Button(text="", background_normal = resource_path('assets/Down Button.png'), size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.85})
        Bitnum_Up.bind(on_press = self.bitup)
        Bitnum_layout.add_widget(Bitnum_Up)

        Bitnum_Down = Button(text="", background_normal = resource_path('assets/Up Button.png'), size_hint=(None, None), size=(50, 25), pos_hint = {'center_x': 0.9, 'center_y':0.63})
        Bitnum_Down.bind(on_press = self.bitdown)
        Bitnum_layout.add_widget(Bitnum_Down)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)
        
        prev_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        prev_layout.size_hint = (0.1, 0.1)
        prev_layout.width = 300
        prev_layout.pos_hint = {'x': 0.03, 'y': 0}
        self.add_widget(prev_layout)

        prev_button = Button(text = "Previous Page", size = (250, 100), size_hint = (None, None))
        prev_button.bind(on_press = self.prev_screen)
        prev_layout.add_widget(prev_button)

        next_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        next_layout.size_hint = (0.1, 0.1)
        next_layout.width = 300
        next_layout.pos_hint = {'x': 0.82, 'y': 0}
        self.add_widget(next_layout)

        next_button = Button(text = "Next", size = (250, 100), size_hint = (None, None))
        next_button.bind(on_press = self.next_screen)
        next_layout.add_widget(next_button)

    def check_state(self, instance):
        bin1=[]
        for ds in self.Bs1:
            s = ds.get_state()
            if s:
                bin1.append(1)
            else:
                bin1.append(0)
        
        bin2=[]
        for ds in self.Bs2:
            s = ds.get_state()
            if s:
                bin2.append(1)
            else:
                bin2.append(0)

        output = fs(bin1, bin2)

        bol2 = False

        if output ==1:
            bol2 = True
        
        print(output)
        self.condition_image.set_image((not bol2))
        #return output


    
    def bitup(self, instance):
        n = self.bits +1
        if n<15:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_demo'))
                
            new_dj_game = BV_demo(name='BV_demo', n=n)
            sm.add_widget(new_dj_game)
                
            sm.current = 'BV_demo'

            sm.transition = original_transition

    def bitdown(self, instance):
        n = self.bits - 1
        if n>0:
            self.Bitnum.text = str(n)

            sm = self.manager

            original_transition = sm.transition

            sm.transition = NoTransition()


            sm.remove_widget(sm.get_screen('BV_demo'))
            
            new_dj_game = BV_demo(name='BV_demo', n=n)
            sm.add_widget(new_dj_game)
            
            sm.current = 'BV_demo'

            sm.transition = original_transition

    def prev_screen(self, instance):
        global bvs1, bvs2, bvscore_result
        bvs1 =0
        bvs2 =0
        bvscore_result=[]
        self.manager.current = 'article5'

    def next_screen(self, instance):
        self.manager.current = 'article6'
    
    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'


class Real_DJ(Screen):
    def __init__(self,  n=5, gm='Easy', **kwargs):
        super(Real_DJ, self).__init__(**kwargs)

        self.bol = random.choice([True, False])

        self.bits = n

        self.gmc = gm

        states = states_set(n)
        
        self.half_num =[]

        while True:
            i = random.randint(0, len(states)-1)
            if not (i in self.half_num):
                self.half_num.append(i)
            if len(self.half_num)==2**(n-1):
                break

        Ov = BoxLayout(orientation = 'vertical', size_hint = (1, 1), spacing = 20)
        self.add_widget(Ov)

        T = Label(text = 'Use Real Quantum Hardware!', font_size = 60, size_hint_y =0.1)
        Ov.add_widget(T)

        Subtitle_layout = GridLayout(cols = 2, size_hint_y = 0.1)
        Ov.add_widget(Subtitle_layout)

        t1 = Label(text = 'Send A Job Out: ', font_size = 50)
        Subtitle_layout.add_widget(t1)

        t2 = Label(text = 'See Job Data: ', font_size = 50)
        Subtitle_layout.add_widget(t2)

        if not self.bol:
            u = 'Fair'
        else:
            u = 'Biased'
        
        sc_layout = GridLayout(cols = 1, size_hint = (0.5, 0.05))
        Ov.add_widget(sc_layout)

        tu = Label(text ='This Umpire is ' + u + ':', font_size = 40)
        sc_layout.add_widget(tu)

        Q_layout = GridLayout(cols=2, size_hint = (0.5, 0.35))
        Ov.add_widget(Q_layout)

        if u=='Fair':
            uimg = resource_path('assets/Normal Umpire.png')
        else:
            uimg = resource_path('assets/Dancing Umpire.png')
        
        Uimg = Image(source = uimg)
        Q_layout.add_widget(Uimg)
        Qimg = Image(source = resource_path('assets/QC image1.png'))
        Q_layout.add_widget(Qimg)

        send_layout = BoxLayout(orientation = 'vertical', size_hint = (0.5, 0.3), spacing = 20)
        Ov.add_widget(send_layout)
        
        QC_button = Button(text="Use \n Quantum \n Computer", size=(200, 100), size_hint=(None, None), pos_hint={'center_x': 0.5}, halign='center', valign='middle')
        QC_button.bind(on_press=self.QC_run)
        send_layout.add_widget(QC_button)

        self.job_titl = Label(text = '', font_size = 30)
        send_layout.add_widget(self.job_titl)

        self.job_lab = Label(text = '', font_size = 30)
        send_layout.add_widget(self.job_lab)

        restart_but = Button(text = 'Restart', size_hint=(None, None), size = (250, 100), pos_hint={'center_x': 0.5})
        restart_but.bind(on_press=self.restart)
        send_layout.add_widget(restart_but)

        spacer = Label(text ='')
        send_layout.add_widget(spacer)

        button_grid = GridLayout(cols=1, size_hint=(0.5, 0.6), spacing = 20)
        button_grid.pos_hint = {'center_x': 0.75, 'center_y': 0.3}
        self.add_widget(button_grid)

        self.result_label = Label(text="See the Results of a Job: ", font_size=48, size_hint_y=None, height=100)
        button_grid.add_widget(self.result_label)

        self.text_input = TextInput(
            hint_text="Job_id",  # Placeholder text
            font_size=20,  # Font size
            size_hint=(0.35, 0.02),  # Set fixed size
            multiline=False  # Single-line text input
        )
        button_grid.add_widget(self.text_input)

        self.biased = Button(text="Fetch Answer", size_hint=(None, None), size=(200, 100))
        self.biased.bind(on_press=self.Q_check)
        button_grid.add_widget(self.biased)

        self.corans = Label(text="", font_size =30, size_hint_y = 0.1)
        button_grid.add_widget(self.corans)

        self.qans = Label(text ="", font_size =30, size_hint_y = 0.1)
        button_grid.add_widget(self.qans)

        back_layout = GridLayout(cols = 1, size_hint_y=None, height=250, spacing = 20)
        back_layout.size_hint = (0.1, 0.1)
        back_layout.width = 300
        back_layout.pos_hint = {'x': 0.03, 'top': 0.97}
        self.add_widget(back_layout)

        back_button = Button(text = "Back to Home", size = (250, 100), size_hint = (None, None))
        back_button.bind(on_press = self.hsc)
        back_layout.add_widget(back_button)


    def QC_run(self, instance):
        def g(x):
            if self.bol:
                return f(x, self.half_num)
            else:
                return 0

        def Uf_man(state_list, n):
            Uf = QuantumCircuit(n+1)
            for bs in state_list:
                Uf.barrier()
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.mcx(list(range(n)), n)
                for i in range(len(bs)):
                    if bs[i]==0:
                        Uf.x(i)
                Uf.barrier()
            return Uf
        
        def Uf(n):
    
            states_set=[[0]*(n+1)]


            for i in range((2**(n+1))-1):
                temp = states_set[-1].copy() 
                states_set.append(binary_increment(temp))

            Uf_array=[]

            for i in range(2**(n+1)):
                Uf_array.append([0]*(2**(n+1)))
        
            for i in range(len(states_set)):
            
                w = g(states_set[i][1:len(states_set)-1])

                if w==0:
                    Uf_array[i][i]=1
                if w==1:
                    if states_set[i][0]==0:
                        Uf_array[i][i+2**(n)]=1
                    if states_set[i][0]==1:
                        Uf_array[i][i-2**(n)]=1
                
            Uf_array = np.array(Uf_array)
            Uf_gate = Operator(Uf_array)
            
            return Uf_gate


        def Deutsch_J(n):
            dj = QuantumCircuit(n+1, n)
            dj.x(n)
            for i in range(n+1):
                dj.h(i)
            
            dj.barrier()
            dj.unitary(Uf(n), range(n+1))
            #dj.cx(0, 1)
            dj.barrier()

            for i in range(n):
                dj.h(i)
            
            return dj

        DJ = Deutsch_J(self.bits)
        DJ.measure([i for i in range(self.bits)], [i for i in range(self.bits)])

        self.job_titl.text = 'Loading....'

        service = QiskitRuntimeService(channel="ibm_quantum", token="bc25f314dc2d91146c04783f66884d495f3e4c7e369370ef5b1ff240320b38e962f00de74aa57f60e8fd153e17733ac5ef523e8216c20372552d322afc1d8adf")
        backend = service.backend("ibm_brisbane")
        pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)

        DJ_trans = pass_manager.run(DJ)
        sampler = Sampler(mode=backend)
        job = sampler.run([DJ_trans], shots = 256)

        job_id = job.job_id()

        self.job_titl.text = 'Here is Your Job ID: '
        self.job_lab.text = str(job_id)     

        if not self.bol:
            u = 'Fair'
        else:
            u = 'Biased'

        with open('/Users/Agastyaa/Documents/STUFF/Python/Internship/JR_Index.csv', 'a', newline='') as file:
            file.write('')
            writer = csv.writer(file)
            writer.writerow([job_id, u])

    def Q_check(self, instance):
        
        service = QiskitRuntimeService(
            channel='ibm_quantum',
            instance='ibm-q/open/main',
            token='bc25f314dc2d91146c04783f66884d495f3e4c7e369370ef5b1ff240320b38e962f00de74aa57f60e8fd153e17733ac5ef523e8216c20372552d322afc1d8adf'
        )
        job_id = self.text_input.text

        #service = QiskitRuntimeService(channel="ibm_quantum", token='bc25f314dc2d91146c04783f66884d495f3e4c7e369370ef5b1ff240320b38e962f00de74aa57f60e8fd153e17733ac5ef523e8216c20372552d322afc1d8adf')
        
        try:
            job = service.job(job_id)
            result = job.result()
            

            if job.status()=="QUEUED" or job.status == "RUNNING":
                self.corans.text = 'Your Job is On the Way'
            
            elif job.status()=="DONE": 
                counts = result[0].data.c.get_counts()

                c=1

                zer = ''
                for i in range(self.bits):
                    zer = zer + '0'

                if int(counts['00000'])>128:
                    c=0

                data =[]
            
                with open('/Users/Agastyaa/Documents/STUFF/Python/Internship/JR_Index.csv', newline = '') as file:
                    red = csv.reader(file)
                    for row in red:
                        data.append(row)
                
                w = 'Nan'

                for i in range(len(data)):
                    if job_id == data[i][0]:
                        w = i
                        break
                
                if w == 'Nan':
                    self.corans.text = 'Sorry, Job has not \n been run before'
                else:
                    self.corans.text = "Correct Answer: \n " + str(data[w][1]) + ' Umpire'

                    if c==0:
                        self.qans.text = 'Quantum Answer: \n Fair Umpire'
                    else:
                        self.qans.text = 'Quantum Answer: \n Biased Umpire'
                print(counts)
            else:
                self.corans.text= 'Sorry, There seems to be an Error'
        except:
            self.corans.text= 'Sorry, There seems to be an Error1'
        


    
    def restart(self, instance):
        sm = self.manager

        original_transition = sm.transition

        sm.transition = NoTransition()


        sm.remove_widget(sm.get_screen('Real_DJ'))
                
        new_dj_game = Real_DJ(name='Real_DJ', n=self.bits)
        sm.add_widget(new_dj_game)
                
        sm.current = 'Real_DJ'

        sm.transition = original_transition

    def hsc(self, instance):
        complete_result()
        self.manager.current = 'Home'
        
        


        

       
    
    



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Article1(name='article1'))
        sm.add_widget(Article2(name='article2'))
        sm.add_widget(Article3(name='article3'))
        sm.add_widget(Article4(name='article4'))
        sm.add_widget(Article5(name='article5'))
        sm.add_widget(Article6(name='article6'))
        sm.add_widget(Article7(name='article7'))
        sm.add_widget(Article8(name='article8'))
        sm.add_widget(DJ_game(name = 'DJ_game'))
        sm.add_widget(DJ_Summary(name = 'DJ_Summary'))
        #sm.add_widget(DJ_Quantum(name = 'DJ_Quantum'))
        sm.add_widget(DJ_Quantum_New(name = 'DJ_Quantum_New')) 
        sm.add_widget(DJ_Quantum_Summary(name = 'DJ_Quantum_Summary'))
        sm.add_widget(BV_game(name= 'BV_game'))
        sm.add_widget(BV_Summary(name= 'BV_Summary'))
        sm.add_widget(BV_Quantum(name = 'BV_Quantum'))
        sm.add_widget(BV_Quantum_Summary(name = 'BV_Quantum_Summary'))
        sm.add_widget(BV_demo(name = 'BV_demo'))
        sm.add_widget(Home(name = 'Home'))
        sm.add_widget(Real_DJ(name = 'Real_DJ'))

        sm.current = 'Home'
        #sm.current = 'Real_DJ'
        return sm

if __name__ == '__main__':
    MyApp().run()

print(score_result)





