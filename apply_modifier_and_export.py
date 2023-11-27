# from bpy import ops
from bpy.ops.wm import open_mainfile
from argparse import ArgumentParser

arg_parser = ArgumentParser()
arg_parser.add_argument("-f", "--file", type=str, help="File to open")

args = arg_parser.parse_args()

open_mainfile(filename=args.file)
