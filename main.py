from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from flask import Flask, render_template_string
class Image2ascii():
    #Класс для конвертации изображения в ASCII-арта
    # Определяем символы для ASCII-арта, начиная от самого тёмного к самому светлому
    ASCII_CHARS = ['@', '#', '8', 'S', 'B', '5', 'X', '0', 'P', '%', '$', 'M', 'Q', 'H', 'W', 'K', 'D', 'R', 'A', 'G', 'O', '2', '3', '4', '6', '9', 'q', 'm', 'u', 'v', 'y', 'z', 'i', '!', '?', ';', ':', ',', '.', ' ']
    def __init__(self, image_path,new_width=100):
        self.image_path = image_path
        self.new_width = new_width
        try:
            self.image = Image.open(image_path,)
        except Exception as e:
            print(f"Не удалось открыть изображение: {e}")
    def resize_image(self):
        """Изменение размера изображения, сохраняя пропорции."""
        width, height = self.image.size
        aspect_ratio = height / width
        new_height = int(aspect_ratio * self.new_width * 0.45)  # коррекция высоты для ASCII
        self.image=self.image.resize((self.new_width, new_height))
    
    def hsv_image(self):
        self.image=self.image.convert('HSV')
    
    def grayscale_image(self):
        """Преобразование изображения в оттенки серого."""
        self.image=self.image.convert("L")
    
    def gif_to_ascii_frames(self):
        self.frames=[]
        if ".gif" in self.image_path:
            with Image.open(self.image_path) as img:
                for frame in range(img.n_frames):
                    img.seek(frame)
                    self.image=img
                    self.resize_image()
                    self.grayscale_image()
                    self.pixels_to_ascii()
                    self.frames.append(self.ascii_str)
        return self.frames
                    
                    

    def pixels_to_ascii(self):
        """Преобразование пикселей изображения в ASCII-символы."""
        self.ascii_str=[]
        pixels = self.image.getdata()
        for i,pixel in enumerate(pixels):
            if i%self.new_width == 0:
                self.ascii_str.append("\n")
            self.ascii_str.append(self.ASCII_CHARS[int(pixel*(len(self.ASCII_CHARS)-1) / 255)])
        self.ascii_str=''.join(self.ascii_str)
    
    def pixels_to_html_code(self):
        self.html_str=[]
        pixels = self.image.getdata()
        for i,pixel in enumerate(pixels):
            if i%self.new_width == 0:
                self.html_str.append("\n")
            self.html_str.append("<font style=\"color: hsl({0}, {1}%, {2}%);\">".format(int(pixel[0]/255*360),int(pixel[1]/255*100),int(pixel[2]/255*90))+"█"+"</font>")
        self.html_str=''.join(self.html_str)
    
    def get_colored_ascii_image(self,filename):
        # Преобразование изображения
        self.resize_image()
        self.hsv_image()
        # Преобразование в html ascii код
        self.pixels_to_html_code()
        ascii_img = self.html_str

        # Вывод результата
        if filename!=None:
            file=open(filename,"w",encoding="utf8")
            file.write(ascii_img)
        #print(ascii_img)
    
    def get_gray_ascii_image(self,filename=None):

        # Преобразование изображения
        self.resize_image()
        self.grayscale_image()

        # Преобразование пикселей в ASCII
        self.pixels_to_ascii()
        ascii_img = self.ascii_str

        # Вывод результата
        if filename!=None:
            file=open(filename,"w")
            file.write(ascii_img)
        #print(ascii_img)
# Создаем простой веб-сервер с Flask
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII GIF</title>
    <style>
        pre {
            font-family: monospace;
            white-space: pre;
            font-size: 4px;
        }
    </style>
</head>
<body>
    <pre id="ascii"></pre>
    <script>
        const frames = {{ frames|safe }};
        let currentFrame = 0;
        
        function showFrame() {
            document.getElementById('ascii').textContent = frames[currentFrame];
            currentFrame = (currentFrame + 1) % frames.length;
        }
        
        setInterval(showFrame, 30); // Частота обновления кадров
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, frames=Image2ascii("files/02.gif",600).gif_to_ascii_frames())
if __name__ == "__main__":
    #Image2ascii("alya.webp",4000).get_gray_ascii_image("test.txt")
    app.run(debug=True)