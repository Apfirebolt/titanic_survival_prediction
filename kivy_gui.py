import pandas as pd
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput

class TableApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Menu options
        menu_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        load_button = Button(text='Load Data')
        save_button = Button(text='Save Data')
        menu_layout.add_widget(load_button)
        menu_layout.add_widget(save_button)
        main_layout.add_widget(menu_layout)

        # Table layout
        table_layout = GridLayout(cols=3, size_hint_y=None, padding=10, spacing=10)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # Adding headers
        headers = ['Name', 'Age', 'Survived']
        for header in headers:
            table_layout.add_widget(Label(text=header, bold=True, size_hint_y=None, height=40, padding=(10, 10)))

        # Reading data from CSV
        df = pd.read_csv('/Users/amit/Projects/Machine Learning/Titanic Survivor/titanic.csv')

        # Adding data to the table
        for index, row in df.head(50).iterrows():
            table_layout.add_widget(Label(text=str(row['Name']), size_hint_y=None, height=30, padding=(10, 10)))
            table_layout.add_widget(Label(text=str(row['Age']), size_hint_y=None, height=30, padding=(10, 10)))
            table_layout.add_widget(Label(text=str(row['Survived']), size_hint_y=None, height=30, padding=(10, 10)))

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(table_layout)
        main_layout.add_widget(root)

        return main_layout

if __name__ == '__main__':
    from kivy.core.window import Window
    TableApp().run()