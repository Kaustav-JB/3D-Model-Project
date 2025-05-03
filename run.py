# main.py

import subprocess
import webbrowser
import os
import sys
import time

def run_point_e():
    print(f"Running Point-E program...")
    point_e_script = os.path.join(os.path.dirname(__file__), 'text_to_3d_model.py')
    subprocess.run([sys.executable, point_e_script])

def run_triposr():
    print("Launching TripoSR Gradio interface...")
    tripo_script = os.path.join(os.path.dirname(__file__), 'tripoSR', 'app', 'gradio_app.py')
    process = subprocess.Popen([sys.executable, tripo_script])
    time.sleep(5)
    webbrowser.open("http://127.0.0.1:7860")
    process.wait()

def main():
    print("Select an option:")
    print("1. Text prompt to 3D model (Point-E)")
    print("2. Image to 3D model (TripoSR)")
    choice = input("> ").strip()

    if choice == '1':
        run_point_e()
    elif choice == '2':
        run_triposr()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == '__main__':
    main()