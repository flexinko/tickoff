from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import json
from kivy.clock import Clock
from kivy.uix.popup import Popup
from datetime import datetime, timedelta
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior 
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.core.image import Image as CoreImage

class ImageButton(ButtonBehavior, Image):
    pass

class TickOffApp(App):
    def __init__(self, **kwargs):
        super(TickOffApp, self).__init__(**kwargs)
        self.tickstreak = 0
        Clock.schedule_once(self.schedule_daily_check)

    def build(self):

        self.icon = 'logo.jpg'



        main_layout = FloatLayout()

        LabelBase.register(name='NeueFont', fn_regular='Neue.ttf')



        input_layout = FloatLayout(size_hint=(1, None), height=50, pos_hint={'y': 0})
        margin = 10 / Window.size[0]
        #pozadie
        background = Image(source='pozadie.jpg', allow_stretch=True, keep_ratio=False)
        main_layout.add_widget(background)

    


    

        self.tasks = []
        self.tasks_scrollview = ScrollView(size_hint=(0.8, 0.6), pos_hint={'x': 0.1, 'top': 0.6})

       
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.tasks_scrollview.add_widget(self.tasks_layout)

        #Input box pre pridanie úlohy
        input_layout = FloatLayout(size_hint=(1, None), height=50, pos_hint={'y': 0})
        self.text_input = TextInput(
            hint_text='Enter a task', 
            size_hint=(0.7, None), 
            height=30, 
            pos_hint={'x': margin, 'center_y': 0.5}
        )
        #tlacidlo pridania úlohy
        add_button = ImageButton(
            source = "addbutton.jpg",
            size_hint=(0.2, None), 
            height=40, 
            pos_hint={'right': 1 - margin, 'center_y': 0.5}
        )
        
        sign_label1 = Label(
            text='Tick ',
            font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
            font_size='40sp',  # Veľkosť fontu, 'sp' je jednotka nezávislá na hustote obrazovky
            color=get_color_from_hex('#FFFAFF'),  # Biela farba textu
            size_hint=(None, None),  # Vypnutie size_hint, aby sme mohli použiť pevnú šírku a výšku
            width=120,  # Pevná šírka pre label
            height=20,  # Pevná výška pre label
            pos_hint={'x': 0.01, 'top': 0.87},  # Umiestnenie v ľavom hornom rohu s malým odstupom
            halign='left',  # Zarovnanie textu vľavo
            valign='top',  # Zarovnanie textu hore
        )
        sign_label2 = Label(
            text='Off ® ',
            font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
            font_size='40sp',  # Veľkosť fontu, 'sp' je jednotka nezávislá na hustote obrazovky
            color=get_color_from_hex('#FC5130'),  # Biela farba textu
            size_hint=(None, None),  # Vypnutie size_hint, aby sme mohli použiť pevnú šírku a výšku
            width=350,  # Pevná šírka pre label
            height=20,  # Pevná výška pre label
            pos_hint={'x': 0, 'top': 0.87},  # Umiestnenie v ľavom hornom rohu s malým odstupom
            halign='left',  # Zarovnanie textu vľavo
            valign='top',  # Zarovnanie textu hore
        )

        flame_image = Image(
            source='flame-icon.png',  # Nastavte cestu k vášmu PNG obrázku
            size_hint=(None, None),
            size=('35sp', '35sp'),  # Nastavte požadovanú veľkosť obrázku
            pos_hint={'right': 0.96, 'top': 0.89}  # Umiestnenie obrázku v pravom hornom rohu
        )
        add_button.bind(on_press=self.add_task)

        input_layout.add_widget(self.text_input)
        input_layout.add_widget(add_button)

        self.tickstreak_label = Label(
            text=f" {self.tickstreak}", 
            font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
            font_size='40sp',  # Veľkosť fontu
            color=get_color_from_hex('#FFFAFF'),  # Biela farba textu
            size_hint=(None, None),  # Vypnutie size_hint pre šírku a výšku
            text_size=(75, None),  # Ohraničenie textu pevnou šírkou
            halign='right',  # Horizontálne zarovnanie textu vpravo
            valign='middle',  # Vertikálne zarovnanie textu v strede
            pos_hint={'right': 0.90, 'top': 0.92},  
        )

        main_layout.add_widget(self.tasks_scrollview)
        main_layout.add_widget(self.tickstreak_label)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(sign_label1)
        main_layout.add_widget(sign_label2)
        main_layout.add_widget(flame_image)

        

        self.load_tasks()
        return main_layout

    def add_task(self, instance):
        task_text = self.text_input.text
        if task_text:
            self.create_task(task_text, False)
            self.text_input.text = ''
            self.save_tasks()

    def delete_task(self, task_layout, task_text):
        self.tasks_layout.remove_widget(task_layout)
        self.tasks = [task for task in self.tasks if task['text'] != task_text]
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", 'w') as file:
            tasks_data = {
                'tasks': [{'text': task['text'], 'completed': task['check'].active} for task in self.tasks],
                'tickstreak': self.tickstreak
            }
            json.dump(tasks_data, file)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                data = json.load(file)
                self.tasks_layout.clear_widgets()
                self.tasks = []
                for task in data.get('tasks', []):
                    self.create_task(task['text'], task['completed'])
                self.tickstreak = data.get('tickstreak', 0)
                self.tickstreak_label.text = f"{self.tickstreak}"
        except FileNotFoundError:
            self.tickstreak = 0
            self.tickstreak_label.text = f" {self.tickstreak}"
        except json.JSONDecodeError as e:
            print("Chyba při načítání JSON souboru:", e)

    def create_task(self, text, completed=False):
        task_layout = BoxLayout(size_hint_y=None, height=30)
        check = CheckBox(size_hint_x=None, width=30, active=completed)
        check.bind(on_release=lambda instance: self.confirm_task_completion(instance, text))
        label = Label(
            text=text,
            font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
            font_size='15sp',  # Veľkosť fontu
            color=get_color_from_hex('#FFFAFF')            
        )
        delete_button = ImageButton(
        source='delete.png',  # Cesta k obrázku delete ikony
        size_hint_x=None, 
        width=50,  # Šírka ImageButton
        on_press=lambda *args: self.delete_task(task_layout, text)
        )
        delete_button.bind(on_press=lambda x: self.delete_task(task_layout, text))
        task_layout.add_widget(check)
        task_layout.add_widget(label)
        task_layout.add_widget(delete_button)
        self.tasks_layout.add_widget(task_layout)
        self.tasks.append({'layout': task_layout, 'text': text, 'check': check})

    
    def check_tasks_daily(self, *args):
        # Tato metoda nyní přímo kontroluje stavy CheckBoxů v layoutu, místo použití uloženého seznamu 'self.tasks'
        completed_status = [task_checkbox.active for task_layout in self.tasks_layout.children for task_checkbox in task_layout.children if isinstance(task_checkbox, CheckBox)]
        print("Stav dokončení úloh:", completed_status)
        if all(completed_status):
            self.tickstreak += 1
            print("Všetky úlohy boli dokončené. Tickstreak zvýšený.")
        else:
            self.tickstreak = 0
            print("Nie všetky úlohy boli dokončené. Tickstreak resetovaný.")
        self.tickstreak_label.text = f"{self.tickstreak}"
        self.save_tasks()
        self.clear_tasks()    
    
    def clear_tasks(self):
        self.tasks_layout.clear_widgets()  # Vymaže widgety z rozhraní
        self.tasks = []  # Vyčistí seznam úloh
        self.save_tasks()  # Uloží prázdný seznam do souboru
    


    def schedule_daily_check(self, *args):
        now = datetime.now()
        next_check = datetime(now.year, now.month, now.day, 23,59)
        if now > next_check:
            next_check += timedelta(days=1)
        delay = (next_check - now).total_seconds()
        Clock.schedule_once(self.check_tasks_daily, delay)



    def complete_task(self, checkbox_instance, task_text):
        # Nájdenie a aktualizácia stavu úlohy
        for task in self.tasks:
            if task['text'] == task_text:
                task['check'].active = True
                break

        # Uloženie zmeny
        self.save_tasks()


        # Zatvorenie vyskakovacieho okna
        self.popup.dismiss()

    def uncomplete_task(self, checkbox_instance, task_text):
        # Nájdenie a aktualizácia stavu úlohy
        for task in self.tasks:
            if task['text'] == task_text:
                task['check'].active = False
                break
        self.save_tasks()
  
    
    

    
    def cancel_task_completion(self, checkbox_instance, *args):
        checkbox_instance.active = False
        self.popup.dismiss()
   
    
    def confirm_task_completion(self, checkbox_instance, task_text):

        if checkbox_instance.active:  # Ak bol checkbox práve zaškrtnutý
            content = BoxLayout(orientation='vertical',)
            content.add_widget(Label(
                
                
                
                font_size='15sp',  # Veľkosť fontu
                color=get_color_from_hex('#FFFAFF'),
                
                text='Naozaj si úlohu spravil? \nPamätaj, robíš to len pre seba!'
                
                ))

            button_layout = BoxLayout(size_hint_y=None, height=30)
            yes_button = Button(text='Áno',
                font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
                font_size='15sp',  # Veľkosť fontu
                color=get_color_from_hex('#FFFAFF'),
                background_color=(0,100,0,1)            
            )
            yes_button.bind(on_press=lambda x: self.complete_task(checkbox_instance, task_text))
            no_button = Button(text='Nie',
                font_name='NeueFont',  # Meno fontu, ktoré ste zaregistrovali
                font_size='15sp',  # Veľkosť fontu
                color=get_color_from_hex('#FFFAFF'),
                background_color=(100,0,0,1)            
            )
            no_button.bind(on_press=lambda x: self.cancel_task_completion(checkbox_instance))

            button_layout.add_widget(yes_button)
            button_layout.add_widget(no_button)
            content.add_widget(button_layout)

            self.popup = Popup(title='',separator_height=0, content=content, size_hint=(None, None), size=(300, 150),background_color=(0,0,0,1))
            self.popup.open()
        else:  # Ak bol checkbox odškrtnutý
            self.uncomplete_task(checkbox_instance, task_text)




if __name__ == '__main__':
    TickOffApp().run()