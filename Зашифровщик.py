from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from cryptography.fernet import Fernet

class LogoScreen(Screen):
    def __init__(self, **kwargs):
        super(LogoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Отображение логотипа
        logo = Image(source='/storage/emulated/0/DCIM/Screenshots/Screenshot_20241006_181012_YouTube.jpg')
        layout.add_widget(logo)
        
        self.add_widget(layout)
        
        # Показать основной экран через 3 секунды
        Clock.schedule_once(self.show_main_screen, 3)

    def show_main_screen(self, dt):
        self.manager.current = 'main'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Поле для вывода имени выбранного файла
        self.file_label = Label(text='Выберите файл для шифрования или дешифрования')
        layout.add_widget(self.file_label)

        # Кнопка для выбора файла
        choose_file_button = Button(text='Выбрать файл')
        choose_file_button.bind(on_press=self.choose_file)
        layout.add_widget(choose_file_button)

        # Кнопка для шифрования
        encrypt_button = Button(text='Зашифровать файл')
        encrypt_button.bind(on_press=self.encrypt_file)
        layout.add_widget(encrypt_button)

        # Кнопка для дешифрования
        decrypt_button = Button(text='Дешифровать файл')
        decrypt_button.bind(on_press=self.decrypt_file)
        layout.add_widget(decrypt_button)

        self.add_widget(layout)

    def choose_file(self, instance):
        # Открываем файловый менеджер
        self.filechooser = FileChooserListView()
        self.filechooser.bind(on_submit=self.load_file)
        popup = Popup(title='Выбор файла', content=self.filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_file(self, instance, selection, touch):
        # Загружаем выбранный файл
        if selection:
            self.selected_file = selection[0]
            self.file_label.text = f'Выбранный файл: {self.selected_file}'
            self.load_file_content()

    def load_file_content(self):
        # Читаем содержимое файла
        with open(self.selected_file, 'rb') as f:
            self.file_content = f.read()

    def encrypt_file(self, instance):
        # Генерация ключа (если его нет)
        if not hasattr(self, 'key'):
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)

        # Шифрование файла
        encrypted = self.cipher.encrypt(self.file_content)

        # Сохранение зашифрованного файла
        with open(self.selected_file + '.meow', 'wb') as f:
            f.write(encrypted)

        self.show_popup('Успех', f'Файл зашифрован и сохранен как {self.selected_file}.meow')

    def decrypt_file(self, instance):
        # Дешифрование файла
        try:
            decrypted = self.cipher.decrypt(self.file_content)

            # Сохранение расшифрованного файла
            with open(self.selected_file + '.decrypted', 'wb') as f:
                f.write(decrypted)

            self.show_popup('Успех', f'Файл расшифрован и сохранен как {self.selected_file}.decrypted')
        except Exception as e:
            self.show_popup('Ошибка', 'Ошибка дешифрования: ' + str(e))

    def show_popup(self, title, message):
        # Отображение сообщения в виде всплывающего окна
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Закрыть')
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class EncryptorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LogoScreen(name='logo'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    EncryptorApp().run()
