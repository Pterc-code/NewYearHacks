# Imports
import configparser
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import (FadeTransition, Screen, ScreenManager)
from settingsjson import settings_json
from input import Inputs
from gateway import get
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

# Reading Settings
read_config = configparser.ConfigParser()
read_config.read('my.ini')
tutorial_status = read_config.get('tutorial', 'tutorial_status')

# Global Vars
TaskObject = Inputs()
current_info = ''


class TaskWidget(Widget):

    def __init__(self, text, **kwargs):
        super(TaskWidget, self).__init__(**kwargs)
        self.text = Label(text=text, font_size='20',
                          color=(0, 0, 0, 1),
                          font_name='Roboto-Thin.ttf', size_hint=(1.0, 1.0),
                          halign="left", valign="middle")
        self.text.bind(size=self.text.setter('text_size'))

        self.main_btn = Button(text='=', font_size='20', size_hint=(.1, .1),
                               background_color=(0, 0, 0, 0),
                               font_name='Roboto-Thin.ttf', color=(0, 0, 0, 1),
                               on_release=lambda number: self.method())

    def method(self):
        global current_info
        current_info = self.text.text


class TitleWindow(Screen):

    def __init__(self, **kwargs):
        super(TitleWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.change_screen, 2)

    def change_screen(self, *kwargs):
        ScreenManager.transition = FadeTransition()
        self.manager.current = 'main'


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        if touch.oy - touch.y > 50:
            ScreenManager.transition = FadeTransition()
            MyApp.get_running_app().change_screen(screen_name="task")

    def on_touch_move(self, touch):
        if touch.y - touch.oy > 50:
            MyApp.get_running_app().open_settings()

    def change_screen(self, args):
        ScreenManager.transition = FadeTransition()
        self.manager.current = 'edit'

    def update(self):
        self.ids.grid.clear_widgets()
        for i in get():
            task = TaskWidget(i[0])
            text = task.text
            main_btn = task.main_btn
            main_btn.bind(on_release=self.change_screen)

            self.ids.grid.add_widget(Label(text=' ', size_hint=(0.1, 0.1)))
            self.ids.grid.add_widget(text)
            self.ids.grid.add_widget(main_btn)

    def show_tutorial(self):
        if tutorial_status == '1':
            self.ids.float.add_widget(
                Label(text='SCROLL UP TO ADD MORE TASKS', font_size='20',
                      color=(0, 0, 0, 1),
                      font_name='Roboto-Thin.ttf',
                      size_hint=(1.0, 1.0),
                      pos_hint={'center_x': 0.5, 'center_y': 0.2}))
            self.ids.float.add_widget(
                Label(text='SCROLL DOWN TO ACCESS SETTINGS', font_size='20',
                      color=(0, 0, 0, 1),
                      font_name='Roboto-Thin.ttf',
                      size_hint=(1.0, 1.0),
                      pos_hint={'center_x': 0.5, 'center_y': 0.1}))
            self.ids.float.add_widget(
                Label(text='CLICK = TO EDIT THE TASK', font_size='20',
                      color=(0, 0, 0, 1),
                      font_name='Roboto-Thin.ttf',
                      size_hint=(1.0, 1.0),
                      pos_hint={'center_x': 0.5, 'center_y': 0.3}))

    def on_enter(self, *args):
        self.update()
        self.show_tutorial()


class AddTask(Screen):
    input = ObjectProperty(None)

    def on_touch_move(self, touch):
        if touch.y - touch.oy > 50:
            ScreenManager.transition = FadeTransition()
            MyApp.get_running_app().change_screen(screen_name="main")

    def change_screen(self, *kwargs):
        ScreenManager.transition = FadeTransition()
        self.manager.current = 'main'

    def add(self, msg):
        TaskObject.add(msg)
        self.input.text = ''


class TaskEdit(Screen):

    def change_screen(self, *kwargs):
        ScreenManager.transition = FadeTransition()
        self.manager.current = 'main'

    def show_pop(self):
        fl = FloatLayout()

        popupwindow = Popup(title=" ", content=fl, size_hint=(None, None),
                            size=(300, 200),
                            background_color=(255, 248, 231, 1),
                            separator_height=0)
        no_btn = Button(text='NO', on_release=popupwindow.dismiss,
                        font_name='Roboto-Thin.ttf', color=(0, 0, 0, 1),
                        size_hint=(0.4, 0.2),
                        background_color=(0, 0, 0, 0),
                        pos_hint={"x": 0.5, "y": 0.1})

        yes_btn = Button(text='YES', on_release=self.delete,
                         font_name='Roboto-Thin.ttf', color=(0, 0, 0, 1),
                         size_hint=(0.4, 0.2),
                         background_color=(0, 0, 0, 0),
                         pos_hint={"x": 0.1, "y": 0.1})
        yes_btn.bind(on_release=popupwindow.dismiss)
        yes_btn.bind(on_release=self.change_screen)
        fl.add_widget(no_btn)
        fl.add_widget(yes_btn)
        fl.add_widget(Label(text='Are you sure you want to delete this task?',
                            color=(0, 0, 0, 1), font_name='Roboto-Thin.ttf',
                            size_hint=(0.6, 0.2),
                            pos_hint={"x": 0.2, "top": 0.9}))
        popupwindow.open()

    def delete(self, args):
        TaskObject.delete(current_info)

    def edit(self, new_content):
        TaskObject.edit(current_info, new_content)

    def on_enter(self):
        self.ids.input.text = current_info


kv = Builder.load_file("my.kv")


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        Window.size = (375, 812)
        return kv

    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name

    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.add_json_panel('App Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        MyApp.get_running_app().stop()


if __name__ == "__main__":
    MyApp().run()
