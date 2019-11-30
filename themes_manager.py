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
        print(data["colors"][key])
        if type(data["colors"][key]) is str:
            file.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["colors"][key] + ");\n")
        else:
            for sub_key in data["colors"][key].keys():
                file.write("  constexpr static KDColor " + key + sub_key + " = KDColor::RGB24(0x" + data["colors"][key][sub_key] + ");\n")

    # Default values - Sometimes never used
    file.write("  constexpr static KDColor YellowDark = KDColor::RGB24(0xffb734);\n")
    file.write("  constexpr static KDColor YellowLight = KDColor::RGB24(0xffcc7b);\n")
    file.write("  constexpr static KDColor PurpleBright = KDColor::RGB24(0x656975);\n")
    file.write("  constexpr static KDColor PurpleDark = KDColor::RGB24(0x414147);\n")
    file.write("  constexpr static KDColor GreyWhite = KDColor::RGB24(0xf5f5f5);\n")
    file.write("  constexpr static KDColor GreyBright = KDColor::RGB24(0xececec);\n")
    file.write("  constexpr static KDColor GreyMiddle = KDColor::RGB24(0xd9d9d9);\n")
    file.write("  constexpr static KDColor GreyDark = KDColor::RGB24(0xa7a7a7);\n")
    file.write("  constexpr static KDColor GreyVeryDark = KDColor::RGB24(0x8c8c8c);\n")
    file.write("  constexpr static KDColor Select = KDColor::RGB24(0xd4d7e0);\n")
    file.write("  constexpr static KDColor SelectDark = KDColor::RGB24(0xb0b8d8);\n")
    file.write("  constexpr static KDColor WallScreen = KDColor::RGB24(0xf7f9fa);\n")
    file.write("  constexpr static KDColor WallScreenDark = KDColor::RGB24(0xe0e6ed);\n")
    file.write("  constexpr static KDColor SubTab = KDColor::RGB24(0xb8bbc5);\n")
    file.write("  constexpr static KDColor LowBattery = KDColor::RGB24(0xf30211);\n")
    file.write("  constexpr static KDColor Red = KDColor::RGB24(0xff000c);\n")
    file.write("  constexpr static KDColor RedLight = KDColor::RGB24(0xfe6363);\n")
    file.write("  constexpr static KDColor Magenta = KDColor::RGB24(0xff0588);\n")
    file.write("  constexpr static KDColor Turquoise = KDColor::RGB24(0x60c1ec);\n")
    file.write("  constexpr static KDColor Pink = KDColor::RGB24(0xffabb6);\n")
    file.write("  constexpr static KDColor Blue = KDColor::RGB24(0x5075f2);\n")
    file.write("  constexpr static KDColor BlueLight = KDColor::RGB24(0x718fee);\n")
    file.write("  constexpr static KDColor Orange = KDColor::RGB24(0xfe871f);\n")
    file.write("  constexpr static KDColor Green = KDColor::RGB24(0x50c102);\n")
    file.write("  constexpr static KDColor GreenLight = KDColor::RGB24(0x52db8f);\n")
    file.write("  constexpr static KDColor Brown = KDColor::RGB24(0x8d7350);\n")
    file.write("  constexpr static KDColor Purple = KDColor::RGB24(0x6e2d79);\n")
    # End

    file.write("  constexpr static KDColor DataColor[] = {Red, Blue, Green, YellowDark, Magenta, Turquoise, Pink, Orange};\n")
    file.write("  constexpr static KDColor DataColorLight[] = {RedLight, BlueLight, GreenLight, YellowLight};\n")

    file.write("  constexpr static KDColor AtomColor[] = {\n")
    file.write("    AtomUnknown, AtomAlkaliMetal, AtomAlkaliEarthMetal, AtomLanthanide, AtomActinide, AtomTransitionMetal,\n")
    file.write("    AtomPostTransitionMetal, AtomMetalloid, AtomHalogen, AtomReactiveNonmetal, AtomNobleGas\n")
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