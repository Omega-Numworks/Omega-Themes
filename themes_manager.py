import sys
import argparse
import os
import json
import shutil


def get_icons_list():
    """
    Load icon list from file
    """
    with open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "icons.json", "r") as json_file:
        data = json.load(json_file)
    
    return data

def get_data(theme):
    """
    Load theme from file
    """
    with open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "themes" + os.path.sep + theme + ".json", "r") as json_file:
        data = json.load(json_file)
    
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
        if type(data["colors"][key]) is str:
            file_p.write("  constexpr static KDColor " + key + " = KDColor::RGB24(0x" + data["colors"][key] + ");\n")
        else:
            for sub_key in data["colors"][key].keys():
                file_p.write("  constexpr static KDColor " + key + sub_key + " = KDColor::RGB24(0x" + data["colors"][key][sub_key] + ");\n")

    # Default values - Sometimes never used
    file_p.write("  constexpr static KDColor YellowDark = KDColor::RGB24(0xffb734);\n")
    file_p.write("  constexpr static KDColor YellowLight = KDColor::RGB24(0xffcc7b);\n")
    file_p.write("  constexpr static KDColor PurpleBright = KDColor::RGB24(0x656975);\n")
    file_p.write("  constexpr static KDColor PurpleDark = KDColor::RGB24(0x414147);\n")
    file_p.write("  constexpr static KDColor GreyWhite = KDColor::RGB24(0xf5f5f5);\n")
    file_p.write("  constexpr static KDColor GreyBright = KDColor::RGB24(0xececec);\n")
    file_p.write("  constexpr static KDColor GreyMiddle = KDColor::RGB24(0xd9d9d9);\n")
    file_p.write("  constexpr static KDColor GreyDark = KDColor::RGB24(0xa7a7a7);\n")
    file_p.write("  constexpr static KDColor GreyVeryDark = KDColor::RGB24(0x8c8c8c);\n")
    file_p.write("  constexpr static KDColor Select = KDColor::RGB24(0xd4d7e0);\n")
    file_p.write("  constexpr static KDColor SelectDark = KDColor::RGB24(0xb0b8d8);\n")
    file_p.write("  constexpr static KDColor WallScreen = KDColor::RGB24(0xf7f9fa);\n")
    file_p.write("  constexpr static KDColor WallScreenDark = KDColor::RGB24(0xe0e6ed);\n")
    file_p.write("  constexpr static KDColor SubTab = KDColor::RGB24(0xb8bbc5);\n")
    file_p.write("  constexpr static KDColor LowBattery = KDColor::RGB24(0xf30211);\n")
    file_p.write("  constexpr static KDColor Red = KDColor::RGB24(0xff000c);\n")
    file_p.write("  constexpr static KDColor RedLight = KDColor::RGB24(0xfe6363);\n")
    file_p.write("  constexpr static KDColor Magenta = KDColor::RGB24(0xff0588);\n")
    file_p.write("  constexpr static KDColor Turquoise = KDColor::RGB24(0x60c1ec);\n")
    file_p.write("  constexpr static KDColor Pink = KDColor::RGB24(0xffabb6);\n")
    file_p.write("  constexpr static KDColor Blue = KDColor::RGB24(0x5075f2);\n")
    file_p.write("  constexpr static KDColor BlueLight = KDColor::RGB24(0x718fee);\n")
    file_p.write("  constexpr static KDColor Orange = KDColor::RGB24(0xfe871f);\n")
    file_p.write("  constexpr static KDColor Green = KDColor::RGB24(0x50c102);\n")
    file_p.write("  constexpr static KDColor GreenLight = KDColor::RGB24(0x52db8f);\n")
    file_p.write("  constexpr static KDColor Brown = KDColor::RGB24(0x8d7350);\n")
    file_p.write("  constexpr static KDColor Purple = KDColor::RGB24(0x6e2d79);\n")
    # End

    file_p.write("  constexpr static KDColor DataColor[] = {Red, Blue, Green, YellowDark, Magenta, Turquoise, Pink, Orange};\n")
    file_p.write("  constexpr static KDColor DataColorLight[] = {RedLight, BlueLight, GreenLight, YellowLight};\n")

    file_p.write("  constexpr static KDColor AtomColor[] = {\n")
    file_p.write("    AtomUnknown, AtomAlkaliMetal, AtomAlkaliEarthMetal, AtomLanthanide, AtomActinide, AtomTransitionMetal,\n")
    file_p.write("    AtomPostTransitionMetal, AtomMetalloid, AtomHalogen, AtomReactiveNonmetal, AtomNobleGas\n")
    file_p.write("  };\n")
    file_p.write("};\n\n")

    file_p.write("#endif\n")


# parser = argparse.ArgumentParser(description="Process the themes.")
# parser.add_argument('--theme', help='the name of the theme')

# args = parser.parse_args()
# data = get_data(args.theme)

def main(args):
    if (args.list):
        print(" ==== Avaliable themes ====");
        for file_info in os.listdir(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "themes"):
            filename = os.path.splitext(file_info)[0]
            print(filename)
        sys.exit(0)

    data = get_data(args.theme)
    
    if (args.icon):
        # Get the icon in the icon theme folder
        icons = get_icons_list()
        
        icon_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "icons" + os.path.sep + data["icons"] + os.path.sep + icons[args.output.replace(args.build_dir, "")]
        
        # Check if the file exists
        if os.path.isfile(icon_path):
            # If yes, copy from theme
            shutil.copyfile(icon_path, args.output)
        else:
            # If no, copy from src
            print(" (!!)   Icon " + icons[args.output.replace(args.build_dir, "")] + " not found in icon theme " + data["icons"] + ". Using default!")
            shutil.copyfile(args.output.replace(args.build_dir, ""), args.output)
    else:
        if (args.stdout):
            write_palette_h(data, sys.stdout)
        else:
            with open(args.output, "w") as palette_file:
                write_palette_h(data, palette_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the themes.")
    parser.add_argument("theme", nargs="?", help="the name of the theme")
    parser.add_argument("output", nargs="?", help="path to the output header file")
    parser.add_argument("build_dir", nargs="?", help="path to the output folder")
    parser.add_argument("-l", "--list", help="list themes", action="store_true")
    parser.add_argument("-i", "--icon", help="outputs an icon instead of a header", action="store_true")
    parser.add_argument("--stdout", help="print palette.h to stdout", action="store_true")

    args = parser.parse_args()
    main(args)

