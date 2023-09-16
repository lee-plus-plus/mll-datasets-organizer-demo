from dataset import *
import re

if __name__ == '__main__':
    filenames = glob(join('.', '*/*.arff'))
    for filename in filenames:
        print(filename)
        try:
            name   = re.split(r"(.+)/(.+)\.arff", filename)[2]
            folder = re.split(r"(.+)/(.+)\.arff", filename)[1]
            target_filename = f'{folder}/{name}.mat'

            X, Y = load_from_arff(filename, return_attribute_definitions=False)
            mat_dict = {'data': X, "target": Y}

            save_to_mat(target_filename, mat_dict)
            print(f'successfully saved at {target_filename}')

        except:
            print('error, skip')
        finally:
            print()
