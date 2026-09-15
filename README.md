# Convertidor de texto a voz

Una aplicación de escritorio sencilla para convertir archivos `.txt` y `.pdf` a MP3 usando Google Text-to-Speech.

![Vista previa de Text-to-Speech Converter](assets/screenshot.png)

## 🚀 Funcionalidades

* Convierte archivos `.txt` a MP3.
* Convierte archivos `.pdf` a MP3.
* Soporte para varios idiomas.
* Interfaz con tema oscuro.
* Conversión en segundo plano para mantener la interfaz fluida.
* Distribución en formato AppImage para Linux.

## 📦 Instalación

### AppImage

Descarga la última versión de la AppImage desde la página de [Releases](https://github.com/necrisscript/text-to-speech-converter/releases).

Dale permisos de ejecución:

```bash
chmod +x Text_To_Speech_Converter-x86_64.AppImage
```

Ejecuta la aplicación:

```bash
./Text_To_Speech_Converter-x86_64.AppImage
```

## 🛠️ Desarrollo

Clona el repositorio:

```bash
git clone https://github.com/necrisscript/text-to-speech-converter.git
cd text-to-speech-converter
```

Crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta la aplicación:

```bash
python main.py
```

## 🔨 Compilación

El proyecto utiliza PyInstaller para crear el ejecutable de Linux y linuxdeploy para empaquetarlo como una AppImage.

Genera el ejecutable:

```bash
pyinstaller --clean text_to_speech_converter.spec
```

El ejecutable se generará en:

```bash
dist/text-to-speech-converter
```

Después, puedes generar la AppImage resultante usando linuxdeploy.

## ⚠️ Notas

Esta aplicación utiliza Google Text-to-Speech, por lo que necesita una conexión a Internet activa para convertir el texto en audio.

Formatos de entrada compatibles:

* `.txt`
* `.pdf`

## 🧪 Estado del proyecto

Este proyecto fue creado principalmente para experimentar, aprender y pasar un buen rato programando con *vibe coding*. Es funcional, pero no pretende ser una solución profesional ni estar listo para entornos de producción. Siéntete libre de usarlo, modificarlo y romper cosas bajo tu propia responsabilidad.

## 📄 Licencia

Este proyecto está distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
