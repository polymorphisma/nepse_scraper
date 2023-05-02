import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

wasm_file = os.path.join(ROOT_PATH, 'required_data', 'nepse.wasm')
headindices_path = os.path.join(ROOT_PATH, 'required_data', 'headindices.csv')