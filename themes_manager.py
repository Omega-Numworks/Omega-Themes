import sys
import argparse
import io
import os
import json


def get_data(theme):
    """
    Load theme from file
    """
    json_file = open("themes/" + theme + ".json", "r")
    data = json.load(json_file)
    json_file.close()
    
    return data

def write_palette_h(data, file_p):
    """
    Write the header to file_p
    """
    file_p.write("#ifndef ESCHER_PALETTE_H\n")
    file_p.write("#define ESCHER_PALETTE_H\n\n")
    file_p.write("#include <kandinsky/color.h>\n\n")
    file_p.write("class Palette {\n")
    file_p.write("public:\n")

    for key in data["colors"].keys():
        file_p.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["colors"][key] + ");\n")

    file_p.write("  constexpr static KDColor DataColor[] = {Red, Blue, Green, YellowDark, Magenta, Turquoise, Pink, Orange};\n")
    file_p.write("  constexpr static KDColor DataColorLight[] = {RedLight, BlueLight, GreenLight, YellowLight};\n")
    file_p.write("};\n\n")

    if ("atom" in data["apps"]):
        file_p.write("#define ATOM_APP_USE_PALETTE\n")
        file_p.write("class AtomPalette {\n")
        file_p.write("public:\n")

        for key in data["apps"]["atom"].keys():
            file_p.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["apps"]["atom"][key] + ");\n")

        file_p.write("  constexpr static KDColor AtomColor[] = {\n")
        file_p.write("      Unknown, AlkaliMetal, AlkaliEarthMetal, Lanthanide, Actinide, TransitionMetal,\n")
        file_p.write("      PostTransitionMetal, Metalloid, Halogen, ReactiveNonmetal, NobleGas\n")
        file_p.write("  };\n")
        file_p.write("};\n\n")
    file_p.write("#endif\n")




def main(args):
    if (args.list):
        print(" ==== Avaliable themes ====");
        for file_info in os.listdir("themes"):
            filename = os.path.splitext(file_info)[0]
            print(filename)
        sys.exit(0)

    data = get_data(args.theme)
    
    if (args.stdout):
        write_palette_h(data, sys.stdout)
    else:
        with open("../escher/include/escher/palette.h", "w") as palette_file:
            write_palette_h(data, palette_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the themes.")
    parser.add_argument("theme", nargs="?", help="the name of the theme")
    parser.add_argument("-l", "--list", help="list themes", action="store_true")
    parser.add_argument("--stdout", help="print palette.h to stdout", action="store_true")

    args = parser.parse_args()
    main(args)

"""
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
"""
