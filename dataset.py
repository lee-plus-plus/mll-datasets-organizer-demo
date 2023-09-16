import arff
from scipy import sparse
import re
import numpy as np
from scipy.io import loadmat, savemat
from os.path import join

from glob import glob
import re


def _load_from_arff(filename, dtype='float', encode_nominal=True):
    arff_frame = arff.load(open(filename, 'r'), encode_nominal=True)

    description = arff_frame['description']
    relation = arff_frame['relation']

    # get meta infomation
    _, name, info = re.split('(.+): (.*)', relation)[:3]
    info_ = info.split()
    info_dict = {key: value for key, value in zip(info_[0::2], info_[1::2])}

    assert('-m' in info_dict);
    assert('-d' in info_dict);
    assert('-q' in info_dict);
    assert('-label_location' in info_dict);
    assert('-is_sparse' in info_dict);


    dim_label = int(info_dict['-q'])
    label_location = info_dict['-label_location']
    assert(dim_label != 0)

    matrix = sparse.csc_matrix(np.array(arff_frame['data']))

    if label_location == "start":
        X, y = matrix[:, dim_label:], matrix[:, :dim_label].astype(int)
        feature_names = arff_frame['attributes'][dim_label:]
        label_names = arff_frame['attributes'][:dim_label]
    elif label_location == "end":
        X, y = matrix[:, :-dim_label], matrix[:, -dim_label:].astype(int)
        feature_names = arff_frame['attributes'][:-dim_label]
        label_names = arff_frame['attributes'][-dim_label:]
    else:
        raise ValueError("Label location not in {start, end}")

    return X, y, feature_names, label_names, info_dict


def load_from_arff(filename, dtype='float', encode_nominal=True,
                   return_attribute_definitions=True):
    X, y, feature_names, label_names, info_dict = _load_from_arff(
        filename,
        dtype=dtype,
        encode_nominal=encode_nominal
    )

    if return_attribute_definitions:
        return X, y, feature_names, label_names
    else:
        return X, y


def save_to_arff(X, y, label_location="end", save_sparse=True, filename=None,
                 dataset_name='traindata'):
    X = X.todok()
    y = y.todok()

    x_prefix = 0
    y_prefix = 0

    assert set(np.unique(y.toarray().flatten())) == {0, 1}
    assert X.shape[0] == y.shape[0]
    x_attributes = [(u'X{}'.format(i), u'NUMERIC')
                    for i in range(X.shape[1])]
    y_attributes = [(u'y{}'.format(i), [str(0), str(1)])
                    for i in range(y.shape[1])]

    if label_location == "end":
        y_prefix = X.shape[1]
        attributes = x_attributes + y_attributes

    elif label_location == "start":
        x_prefix = y.shape[1]
        attributes = y_attributes + x_attributes

    else:
        raise ValueError("Label location not in {start, end}")

    if save_sparse:
        data = [{} for r in range(X.shape[0])]
    else:
        data = [[0 for c in range(X.shape[1] + y.shape[1])]
                for r in range(X.shape[0])]

    for keys, value in list(X.items()):
        data[keys[0]][x_prefix + keys[1]] = value

    for keys, value in list(y.items()):
        data[keys[0]][y_prefix + keys[1]] = value

    dataset = {
        u'description': u'{}'.format(dataset_name),
        u'relation': u'{}: -m {} -d {} -q {} label_location {} -is_sparse {}'.format(
            dataset_name, X.shape[0], X.shape[1], y.shape[1], label_location, save_sparse
        ),
        u'attributes': attributes,
        u'data': data
    }

    arff_data = arff.dumps(dataset)

    if filename is None:
        return arff_data

    with open(filename, 'w') as fp:
        fp.write(arff_data)


def show_info_arff(filename, dtype='float', encode_nominal=True):
    X, y, feature_names, label_names, info_dict = _load_from_arff(
        filename,
        dtype=dtype,
        encode_nominal=encode_nominal
    )
    str = ''
    str += 'shape: X={}, y={}\n'.format(X.shape, y.shape)
    if len(feature_names) > 4:
        str += 'feature_names [{}] : [{}, {}, ..., {}, {}]\n'.format(
            len(feature_names),
            feature_names[0], feature_names[1], feature_names[-2], feature_names[-1]
        )
    else:
        str += 'feature_names [{}] : [{}]\n'.format(
            len(feature_names),
            ', '.join(feature_names)
        )

    if len(label_names) > 4:
        str += 'label_names [{}] : [{}, {}, ..., {}, {}]\n'.format(
            len(label_names),
            label_names[0], label_names[1], label_names[-2], label_names[-1]
        )
    else:
        str += 'label_names [{}] : [{}]\n'.format(
            len(label_names),
            ', '.join(label_names)
        )
    str += ('info_dict: {}'.format(info_dict))
    return str


def load_all_from_mat(filename):
    data = loadmat(filename)
    return data

def load_from_mat(filename, varname):
    data = loadmat(filename)
    var = data[varname]
    return var


def save_to_mat(filename, mat_dict):
    savemat(filename, mat_dict)

# demo
if __name__ == '__main__':
    print('search available datasets ...')

    filenames = glob(join('.', '*/*.arff'))
    for f in filenames:
        print(f)
        try:
            print(show_info_arff(f))
        except:
            print('failed to read: unrecognized format')
        finally:
            print()
