import subprocess
import os

# define path to essensial files
path_to_converter = r"wkhtmltox\bin\wkhtmltopdf.exe"
path_to_input_file = r"test.html"
path_to_output_file = r"out\test.pdf"

# run converter
result = subprocess.run([path_to_converter, path_to_input_file, path_to_output_file])
