# Necris TTS

 A simple desktop application for converting `.txt` and `.pdf` files to MP3 using Google Text-to-Speech.

 ## 🚀 Features

 - Convert `.txt` files to MP3
- Convert `.pdf` files to MP3
- Multiple language support
- Dark-themed interface
- Background conversion to keep the interface responsive
- Linux AppImage distribution

 ## 📦 Installation

 ### AppImage

 Download the latest AppImage from the Releases page.

 Make it executable:

```
chmod +x Necris_TTS-x86_64.AppImage
```

 Run the application:

```
./Necris_TTS-x86_64.AppImage
```

 ## 🛠️ Development

 Clone the repository:

```
git clone https://github.com/necrissript/necris_tts.git
cd necris_tts
```

 Create and activate a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

 Install the dependencies:

```
pip install -r requirements.txt
```

 Run the application:

```
python main.py
```

 ## 🔨 Build

 The project uses PyInstaller to create the Linux executable and linuxdeploy to package it as an AppImage.

 Build the executable:

```
pyinstaller --clean necris_tts.spec
```

 The executable will be generated in:

```
dist/necris-tts
```

 The resulting AppImage can then be generated using linuxdeploy.

 ## ⚠️ Notes

 Necris TTS uses Google Text-to-Speech and requires an active Internet connection for text-to-speech conversion.

 Supported input formats:

- `.txt`
- `.pdf`

 ## 📄 License

 This project is licensed under the terms of the LICENSE file.
