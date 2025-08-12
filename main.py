#!/usr/bin/env python3
import socket
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
from displayhatmini import DisplayHATMini
from speedtest import Speedtest

# --- Функции получения данных ---
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_internet_speed():
    try:
        st = Speedtest()
        st.get_best_server()
        dl = st.download() / 1e6  # Mbps
        ul = st.upload() / 1e6
        return dl, ul
    except:
        return None, None

def is_ssh_active():
    try:
        out = subprocess.check_output(["who"]).decode()
        return any("pts/" in line for line in out.splitlines())
    except:
        return False

# --- Инициализация дисплея ---
width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(buffer)

display = DisplayHATMini(buffer)
display.set_led(0.1, 0.1, 0.1)  # слабая подсветка LED
font = ImageFont.load_default()

# --- Основной цикл ---
while True:
    # Получаем данные
    ip = get_ip_address()
    dl, ul = get_internet_speed()
    ssh_status = "SSH: ACTIVE" if is_ssh_active() else "SSH: idle"

    # Очищаем экран
    draw.rectangle((0, 0, width, height), (0, 0, 0))

    # Выводим текст
    draw.text((5, 5), f"IP: {ip}", font=font, fill=(255, 255, 255))
    if dl is not None:
        draw.text((5, 20), f"DL: {dl:.1f} Mb/s", font=font, fill=(0, 255, 0))
        draw.text((5, 35), f"UL: {ul:.1f} Mb/s", font=font, fill=(0, 255, 255))
    else:
        draw.text((5, 20), "Speed test error", font=font, fill=(255, 0, 0))
    draw.text((5, 50), ssh_status, font=font, fill=(255, 255, 0))

    # Обновляем экран
    display.display()

    # Обновление каждую минуту
    time.sleep(60)
