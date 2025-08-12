#!/usr/bin/env python3
import time
import socket
import subprocess
import re
from displayhatmini import DisplayHATMini
from speedtest import Speedtest

def get_ip_address():
    # простой способ получить LAN IP (Wi-Fi/eth)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "N/A"
    finally:
        s.close()

def get_internet_speed():
    try:
        st = Speedtest()
        st.get_best_server()
        dl = st.download() / 1e6  # Mbps
        ul = st.upload() / 1e6  # Mbps
        return dl, ul
    except Exception as e:
        return None, None

def is_ssh_active():
    # ищем active sshd-процессы (не включая собственный)
    out = subprocess.check_output(["who"]).decode()
    return any("pts/" in line for line in out.splitlines())

def main():
    display = DisplayHATMini()
    display.clear()
    display.set_backlight(0.5)

    while True:
        ip = get_ip_address()
        dl_speed, ul_speed = get_internet_speed()
        ssh_status = "SSH: ACTIVE" if is_ssh_active() else "SSH: idle"

        display.clear()
        lines = []
        lines.append(f"IP: {ip}")
        if dl_speed is not None:
            lines.append(f"DL: {dl_speed:.1f} Mb/s")
            lines.append(f"UL: {ul_speed:.1f} Mb/s")
        else:
            lines.append("Speed test failed")
        lines.append(ssh_status)

        y = 0
        for line in lines:
            display.write_text(line, pos=(0, y))
            y += 8  # отступ между строками

        display.update()  # применяем изменения
        time.sleep(60)
        
if __name__ == "__main__":
    main()
