import io
import os
import uuid

from http.client import BAD_REQUEST

from flask import request, send_file, abort, Response


class OrbitController:

    @staticmethod
    def read_png_file_and_remove_it(filepath):
        with open(filepath, 'rb') as f:
            binary_data = io.BytesIO(f.read())

        os.remove(filepath)
        return binary_data

    @staticmethod
    def validate_params(zx, zy):
        if zx is None:
            abort(BAD_REQUEST)
        if zy is None:
            abort(BAD_REQUEST)

    @staticmethod
    def invoke(output_directory):

        zx = request.args.get("zx", None)
        zy = request.args.get("zy", None)
        num_iterations = 100

        OrbitController.validate_params(zx, zy)

        # Generate output file path
        # Using file ID to avoid concurrency problems
        file_id = str(uuid.uuid4())
        png_filepath = f'{output_directory}mandelbrot-orbit-{zx}-{zy}-{num_iterations}-{file_id}.png'

        # Generate orbit graph
        cmd = f'mandelbrot-orbit {zx} {zy} {num_iterations} {png_filepath}'
        os.system(cmd)

        return Response(OrbitController.read_png_file_and_remove_it(png_filepath), mimetype='image/png')
