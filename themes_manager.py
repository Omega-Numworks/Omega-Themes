import sys
import argparse
import io
import os
import json
import tkinter as tk
from PIL import Image, ImageTk


def get_data(theme):
    json_file = open("themes/" + theme + ".json", "r")
    data = json.load(json_file)
    json_file.close()
    
    return data


def write_palette_h(data):
    file = open("../escher/include/escher/palette.h", "w")
    file.write("#ifndef ESCHER_PALETTE_H\n")
    file.write("#define ESCHER_PALETTE_H\n\n")
    file.write("#include <kandinsky/color.h>\n\n")
    file.write("class Palette {\n")
    file.write("public:\n")
    
    print(data["colors"])

    for key in data["colors"].keys():
        file.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["colors"][key] + ");\n")

    file.write("  constexpr static KDColor DataColor[] = {Red, Blue, Green, YellowDark, Magenta, Turquoise, Pink, Orange};\n")
    file.write("  constexpr static KDColor DataColorLight[] = {RedLight, BlueLight, GreenLight, YellowLight};\n")
    file.write("};\n\n")

    file.write("#define ATOM_APP_USE_PALETTE\n")
    file.write("class AtomPalette {\n")
    file.write("public:\n")

    for key in data["apps"]["atom"].keys():
        file.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["apps"]["atom"][key] + ");\n")

    file.write("  constexpr static KDColor AtomColor[] = {\n")
    file.write("      Unknown, AlkaliMetal, AlkaliEarthMetal, Lanthanide, Actinide, TransitionMetal,\n")
    file.write("      PostTransitionMetal, Metalloid, Halogen, ReactiveNonmetal, NobleGas\n")
    file.write("  };\n")
    file.write("};\n\n")
    file.write("#endif\n")

    file.close()


# parser = argparse.ArgumentParser(description="Process the themes.")
# parser.add_argument('--theme', help='the name of the theme')

# args = parser.parse_args()
# data = get_data(args.theme)

# write_palette_h(data)

def get_available_themes():
    themes = []
    for file in os.listdir("themes"):
        filename = os.path.splitext(file)[0]
        theme = filename, filename.replace("_", " ").capitalize()

        themes.append(theme)

    return themes


themes = get_available_themes()


# UI

class Window:
    def apply_theme(self, theme_index):
        if theme_index != ():
            filename = themes[theme_index[0]][0]
            data = get_data(filename)
            write_palette_h(data)
            self.popup("Omega - Themes", "Theme applied successfully")
        else:
            self.popup("Omega - Themes", "Please select a theme first")


    def create_ui(self):
        master = tk.Tk()
        master.title("Omega - Themes")
        master.geometry("260x400")
        master.resizable(width=False, height=False)

        # Image
        image = ImageTk.PhotoImage(Image.open("Omega.png").resize((200, 70)))
        panel = tk.Label(master, image = image, height = 100)
        panel.pack(fill=tk.X)

        # Listbox
        listbox = tk.Listbox(master, height=15)
        listbox.pack(fill=tk.X)

        for i in range(len(themes)):
            listbox.insert(i, themes[i][1])
        
        # Button
        patch_button = tk.Button(master, text="Apply", command=lambda: self.apply_theme(listbox.curselection()))
        patch_button.pack(fill=tk.X)

        self.window = master

        master.mainloop()

    
    def popup(self, title, message):
        popup = tk.Toplevel()
        popup.title("Omega - Themes")
        popup.geometry("400x60")
        popup.resizable(width=False, height=False)

        message = tk.Label(popup, text=message, anchor="w")
        message.pack(fill=tk.X)

        button = tk.Button(popup, text="Exit", command=lambda: sys.exit())
        button.pack(side=tk.RIGHT)
        
        popup.mainloop()


Window().create_ui()