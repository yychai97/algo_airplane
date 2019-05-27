from kivy.garden.cefpython import CEFBrowser
from kivy.graphics.context_instructions import Translate, Scale
from kivy.graphics.transformation import Matrix
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, AliasProperty, BooleanProperty, StringProperty
import random
from math import *
from bestflight import graph

from kivy.core.window import Window
Window. size = (1000, 600)

from geopy.distance import geodesic

# from kivy.garden.mapview import MapView, MapMarker, MapLayer#, MIN_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, MAX_LONGITUDE
#from mapview.utils import clamp


#from lineMap import LineMapLayer
#from distance import *
#from distance import MapGraph

locations = {}
locations['kul'] = { 'lat': 2.7456, 'lon': 101.7072 }
locations['braz'] = { 'lat': -15.8697, 'lon': -47.9172 }
locations['jpn'] = { 'lat': 35.5494, 'lon': 139.7798 }
locations['uk'] = { 'lat': 51.5048, 'lon': 0.0495 }
locations['usa'] = { 'lat': 47.7510, 'lon': -120.7401 }
locations['thai'] = { 'lat': 13.6900, 'lon': 100.7501 }
locations['aus'] = { 'lat': -35.4735, 'lon': 149.0124 }
locations['nz'] = { 'lat': -36.8485, 'lon': 174.7633 }
locations['ger'] = { 'lat': 52.5200, 'lon': 13.4049 }
locations['haw'] = { 'lat': 21.3156, 'lon': -157.8580 }
locations['hk'] = { 'lat': 22.2855, 'lon': 114.1576 }
locations['sgp'] = { 'lat': 1.2903, 'lon': 103.8519 }
destinations = ['Kuala Lumpur', 'Brazil', 'Japan','United Kingdom', 'United States of America', 'Thailand', 'Australia','New Zealand','Germany','Hawaii','Hong Kong','Singapore']
cities = {}
cities['Kuala Lumpur'] = 'kul'
cities['Brazil'] = 'braz'
cities['Japan'] = 'jpn'
cities['United Kingdom'] = 'uk'
cities['United States of America'] = 'usa'
cities['Thailand'] = 'thai'
cities['Australia'] = 'aus'
cities['New Zealand'] = 'nz'
cities['Germany'] = 'ger'
cities['Hawaii'] = 'haw'
cities['Hong Kong'] = 'hk'
cities['Singapore'] = 'sgp'
#graph = Graph()


class MainScreen(BoxLayout):

    def choose_destination_poli(self, instance):
        self.destination = instance.text

        e = graph.remove_edge('kul', cities[instance.text])
        
        p = graph.dijkstra_with_weight('kul', cities[instance.text])
        if e != None:
            graph.add_edge('kul', cities[instance.text], getattr(e, 'cost'))
        #paths = graph.getPaths(instance.text)
        #print(str(len(paths)) + ' paths prepared')
        
        self.path = ""
        while len(p) > 0:
            self.path += str(p.popleft())+','
        self.path = self.path[0:-1]
        self.path = self.path.replace(' ', '+')
        print(self.path)
        # self.left_label.remove_widget(self.label)
        # self.label = Label(text='From Kuala Lumpur\nTo {}'.format(self.destination))
        # self.left_label.add_widget(self.label)
        self.webview.url = "https://tkchui.github.io/algomap/map1.html?path="+self.path
        #self.webview.reload()
        pass

    def choose_destination(self, instance):
        self.destination = instance.text

        e = graph.remove_edge('kul', cities[instance.text])
        
        p = graph.dijkstra('kul', cities[instance.text])
        if e != None:
            graph.add_edge('kul', cities[instance.text], getattr(e, 'cost'))
        #paths = graph.getPaths(instance.text)
        #print(str(len(paths)) + ' paths prepared')
        
        self.path = ""
        while len(p) > 0:
            self.path += str(p.popleft())+','
        self.path = self.path[0:-1]
        self.path = self.path.replace(' ', '+')
        print(self.path)
        # self.left_label.remove_widget(self.label)
        # self.label = Label(text='From Kuala Lumpur\nTo {}'.format(self.destination))
        # self.left_label.add_widget(self.label)
        self.webview.url = "https://tkchui.github.io/algomap/map1.html?path="+self.path
        #self.webview.reload()
        pass

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.destination = 'Tokyo'
        self.path = "kul,jpn"

        left_layout = BoxLayout(orientation='vertical')
        # self.left_label = BoxLayout()
        # self.label = Label(text='From Kuala Lumpur\nTo {}'.format(self.destination))
        # self.left_label.add_widget(self.label)
        # left_layout.add_widget(self.left_label)
        buttonHolder = BoxLayout(size_hint=(1, 4))
        left_layout.add_widget(buttonHolder)
        leftButtons = BoxLayout(orientation='vertical')
        rightButtons = BoxLayout(orientation='vertical')
        buttonHolder.add_widget(leftButtons)
        buttonHolder.add_widget(rightButtons)
        for d in destinations:
            btn1 = Button(text=d)
            btn2 = Button(text=d)
            # btn.bind(state=self.choose_destination)
            btn1.bind(on_press=self.choose_destination)
            btn2.bind(on_press=self.choose_destination_poli)
            leftButtons.add_widget(btn1)
            rightButtons.add_widget(btn2)
        #b = BoxLayout(orientation='horizontal',height='32dp',size_hint_y=None)
        #b.add_widget(Button(text="Zoom in",on_press=lambda a: setattr(self.mapview,'zoom',clamp(self.mapview.zoom+1, 3, 10))))
        #b.add_widget(Button(text="Zoom out",on_press=lambda a: setattr(self.mapview,'zoom',clamp(self.mapview.zoom-1, 3, 10))))
        # left_layout.add_widget(b)
        self.add_widget(left_layout)

        #self.mapview = MapView(zoom=8, lat=2.7456, lon=101.7072, size_hint=(1.8, 1))
        #self.mapview.add_widget(MapMarker(lat=2.7456, lon=101.7072))
        # self.addMaker()
        # "./map.html?path=Kuala+Lumpur,Tokyo,New+York&id=1234"
        self.webview = CEFBrowser(
            url="https://tkchui.github.io/algomap/map1.html?path="+self.path+"&id=1234", size_hint=(1.8, 1))
        self.add_widget(self.webview)
        # self.line.reposition()
        #self.line.coordinates=[[2.7456, 101.7072], [2.7456, 101.7072]]

    # def addMaker(self):
    #     for l in locations.keys():
    #         self.mapview.add_widget(MapMarker(lat=locations[l]['lat'], lon=locations[l]['lon']))
    #     self.line = LineMapLayer()
    #     self.mapview.add_layer(self.line, mode="scatter")


class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
