import os
import sys
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import SpinnerOption

from app.services.tts_services import convert_file
from app.services.translation_service import get_text


class LanguageSpinnerOption(SpinnerOption):
    pass


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


UI_DIR = resource_path(os.path.join("app", "ui"))

THEME_FILE = os.path.join(UI_DIR, "theme.kv")
MAIN_KV_FILE = os.path.join(UI_DIR, "main.kv")

Builder.load_file(THEME_FILE)
Builder.load_file(MAIN_KV_FILE)


class TTSLayout(BoxLayout):
    current_lang = StringProperty("en")
    selected_file = StringProperty("")
    selected_file_display = StringProperty("")
    status = StringProperty("")
    is_converting = BooleanProperty(False)

    t_subtitle = StringProperty("")
    t_selected_file_label = StringProperty("")
    t_no_file = StringProperty("")
    t_language = StringProperty("")
    t_select_btn = StringProperty("")
    t_convert_btn = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_translations()
        self.status = get_text(self.current_lang, "initial_status")

    def change_language(self, lang):
        self.current_lang = lang
        self.update_translations()
        if not self.selected_file and not self.is_converting:
            self.status = get_text(self.current_lang, "initial_status")

    def update_translations(self):
        lang = self.current_lang
        self.t_subtitle = get_text(lang, "subtitle")
        self.t_selected_file_label = get_text(lang, "selected_file")
        self.t_no_file = get_text(lang, "no_file_selected")
        self.t_language = get_text(lang, "language")
        self.t_select_btn = get_text(lang, "select_file")
        self.t_convert_btn = get_text(lang, "convert")

    def select_file(self):
        selected_files = self.ids.file_chooser.selection

        if not selected_files:
            self.status = get_text(self.current_lang, "please_select_file")
            return

        self.selected_file = selected_files[0]
        filename = os.path.basename(self.selected_file)
        self.selected_file_display = filename
        self.status = f"{get_text(self.current_lang, 'file_selected_prefix')}{filename}"

    def start_conversion(self):
        if not self.selected_file:
            self.status = get_text(self.current_lang, "please_select_file")
            return

        language = self.get_language_code()

        self.is_converting = True
        self.status = get_text(self.current_lang, "converting")

        conversion_thread = threading.Thread(
            target=self.convert_in_background,
            args=(self.selected_file, language),
            daemon=True,
        )

        conversion_thread.start()

    def convert_in_background(self, input_file, language):
        try:
            output_file = convert_file(
                input_file=input_file,
                language=language,
            )

            Clock.schedule_once(
                lambda dt: self.conversion_finished(output_file)
            )

        except Exception as error:
            Clock.schedule_once(
                lambda dt: self.conversion_failed(str(error))
            )

    def conversion_finished(self, output_file):
        self.is_converting = False
        self.status = f"{get_text(self.current_lang, 'complete_prefix')}{output_file}"

    def conversion_failed(self, error_message):
        self.is_converting = False
        self.status = f"{get_text(self.current_lang, 'failed_prefix')}{error_message}"

    def get_language_code(self):
        language_codes = {
            "English": "en",
            "Spanish": "es",
            "Portuguese": "pt",
        }

        selected_language = self.ids.language_spinner.text

        return language_codes.get(
            selected_language,
            "en",
        )


class TextToSpeechApp(App):
    title = "Text-to-Speech Converter"

    def build(self):
        return TTSLayout()


if __name__ == "__main__":
    TextToSpeechApp().run()
