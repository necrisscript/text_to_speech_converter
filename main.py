import os
import sys
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from app.services.tts_services import convert_file


def resource_path(relative_path):
    """
    Returns the absolute path to a resource.

    Works both when running from the source tree and
    when packaged with PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


UI_DIR = resource_path(os.path.join("app", "ui"))

THEME_FILE = os.path.join(UI_DIR, "theme.kv")
MAIN_KV_FILE = os.path.join(UI_DIR, "main.kv")


# Load the theme before the main layout.
Builder.load_file(THEME_FILE)
Builder.load_file(MAIN_KV_FILE)


class TTSLayout(BoxLayout):
    selected_file = StringProperty("")
    status = StringProperty(
        "Select a TXT or PDF file to begin."
    )
    is_converting = BooleanProperty(False)

    def select_file(self):
        selected_files = self.ids.file_chooser.selection

        if not selected_files:
            self.status = "Please select a file first."
            return

        self.selected_file = selected_files[0]

        self.status = (
            f"Selected: {os.path.basename(self.selected_file)}"
        )

    def start_conversion(self):
        if not self.selected_file:
            self.status = "Please select a TXT or PDF file first."
            return

        language = self.get_language_code()

        self.is_converting = True
        self.status = "Converting... Please wait."

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
        self.status = (
            "Conversion complete:\n"
            f"{output_file}"
        )

    def conversion_failed(self, error_message):
        self.is_converting = False
        self.status = (
            "Conversion failed:\n"
            f"{error_message}"
        )

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



class NecrisTTSApp(App):
    title = "Necris TTS"

    def build(self):
        return TTSLayout()


if __name__ == "__main__":
    NecrisTTSApp().run()
