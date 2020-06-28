import io
import os
import uuid

from flask import request, send_file, Response

FORMAT_PPM_IMAGE = "0"
FORMAT_ASCII_GRAPH = "1"


class MandelbrotController:

    @staticmethod
    def invoke(output_directory):
        graph_format = request.args.get("format")

        # Verbose options
        vo_performance_data = 'r'
        vo_fractal_data = 'f'

        # Optimisation options
        op_periodicity = 'y'

        options = f'{vo_performance_data}{vo_fractal_data}{op_periodicity}'

        if graph_format == FORMAT_PPM_IMAGE:
            # Generate tile
            return MandelbrotController.generate_image(options, output_directory)
        else:
            # Generate ascii graph
            return MandelbrotController.generate_ascii_graph(options, output_directory)

    @staticmethod
    def get_tile_points_from_request():
        left_bottom_zx = request.args.get("left_bottom_zx")
        left_bottom_zy = request.args.get("left_bottom_zy")
        top_right_zx = request.args.get("top_right_zx")
        top_right_zy = request.args.get("top_right_zy")

        left_bottom = f'{left_bottom_zx} {left_bottom_zy}'
        top_right = f'{top_right_zx} {top_right_zy}'

        return [left_bottom, top_right]

    @staticmethod
    def get_resolution_from_request():
        res_x = request.args.get("res_x")
        res_y = request.args.get("res_y")
        resolution = f'{res_x} {res_y}'
        return resolution

    @staticmethod
    def read_txt_file_and_remove_it(filepath):
        with open(filepath) as f:
            yield from f

        os.remove(filepath)

    @staticmethod
    def read_png_file_and_remove_it(filepath):
        with open(filepath, 'rb') as f:
            binary_data = io.BytesIO(f.read())

        os.remove(filepath)
        return binary_data

    @staticmethod
    def generate_image_filename_without_extension(color_map):
        res_x = request.args.get("res_x")
        res_y = request.args.get("res_y")

        # Output filename
        color_map_name_from_color_map = {
            "0": "black-on-white",
            "1": "white-on-black",
            "2": "colored-periods"
        }
        color_map_name = color_map_name_from_color_map[color_map]

        # Using file ID to avoid concurrency problems
        file_id = str(uuid.uuid4())

        filename = f'mandelbrot-{color_map_name}-{res_x}x{res_y}-{file_id}'

        return filename

    @staticmethod
    def generate_image(options, output_directory):
        left_bottom, top_right = MandelbrotController.get_tile_points_from_request()
        resolution = MandelbrotController.get_resolution_from_request()
        color_map = request.args.get("color_map")

        # Generate output file path
        filename = MandelbrotController.generate_image_filename_without_extension(color_map)
        ppm_filepath = f'{output_directory}{filename}.ppm'
        png_filepath = f'{output_directory}{filename}.png'

        # Generate tile
        arguments = f'{left_bottom} {top_right} {resolution} {FORMAT_PPM_IMAGE} {color_map} {ppm_filepath}'
        cmd = f'/usr/src/app/mandelbrot -{options} -- {arguments}'
        os.system(cmd)

        # Convert PPM image to PNG
        cmd = f'pnmtopng {ppm_filepath} > {png_filepath}'
        os.system(cmd)

        # Remove ppm file
        os.remove(ppm_filepath)

        return Response(MandelbrotController.read_png_file_and_remove_it(png_filepath), mimetype='image/png')

    @staticmethod
    def generate_ascii_graph_filepath(output_directory, ascii_map):
        res_x = request.args.get("res_x")
        res_y = request.args.get("res_y")

        ascii_map_name_from_ascii_map = {
            "0": "at-sign",
            "1": "iterations",
            "2": "full-iterations",
            "3": "periods"
        }
        ascii_map_name = ascii_map_name_from_ascii_map[ascii_map]

        # Using file ID to avoid concurrency problems
        file_id = str(uuid.uuid4())

        filename = f'mandelbrot-{ascii_map_name}-{res_x}x{res_y}-{file_id}.txt'

        filepath = f'{output_directory}{filename}'

        return filepath

    @staticmethod
    def generate_ascii_graph(options, output_directory):
        left_bottom, top_right = MandelbrotController.get_tile_points_from_request()
        resolution = MandelbrotController.get_resolution_from_request()
        ascii_map = request.args.get("ascii_map")

        # Generate output file path
        filepath = MandelbrotController.generate_ascii_graph_filepath(output_directory, ascii_map)

        # Generate ascii graph
        arguments = f'{left_bottom} {top_right} {resolution} {FORMAT_ASCII_GRAPH} {ascii_map} {filepath}'
        cmd = f'/usr/src/app/mandelbrot -{options} -- {arguments}'
        os.system(cmd)

        # noinspection PyTypeChecker
        return Response(MandelbrotController.read_txt_file_and_remove_it(filepath), mimetype='text/plain')
