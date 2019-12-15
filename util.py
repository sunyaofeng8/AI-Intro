# -*- coding: utf-8 -*-

import os
import itertools
from PIL import Image
import numpy as np
import pandas as pd


class MagicNumbers:
    test_epoch = 18  # used by the function get_loaded_model
    model_dir = 'models6'  # folder name to save models
    sample_dir = 'samples6'  # folder name to save visualized results
    prefix = '201912071134'


# Constants
flags = MagicNumbers()
hair_str2label = {
    '':       [0, 0, 0],
    'brown':  [0, 0, 1],
    'blonde': [0, 1, 0],
    'black':  [1, 0, 0]
}
gender_str2label = {
    '':       [0, 0],
    'male':   [1, 0],
    'female': [0, 1]
}
hairs = ['', 'black', 'blonde', 'brown']
genders = ['', 'male', 'female']
labels_str = list(itertools.product(hairs, genders))
nunique_labels = len(labels_str)


def get_dataset(shuffle=True):
    """ Returns the dataset for image sampling. """
    df = pd.read_csv('../celebA/list_attr_celeba.txt',
                     skiprows=1, delim_whitespace=True)[['Blond_Hair', 'Black_Hair', 'Brown_Hair', 'Male']]
    df['hair'] = 0
    for i, column_name in enumerate(('Blond_Hair', 'Black_Hair', 'Brown_Hair')):
        df.loc[df[column_name] == 1, 'hair'] = i + 1
    hair2index = {
        'blonde': 1,
        'black':  2,
        'brown':  3
    }
    gender2index = {
        'male':   1,
        'female': -1
    }

    datasets = {}
    for hair, gender in labels_str:
        if not hair or not gender:
            continue
        dataset = df[(df.hair == hair2index[hair]) & (df.Male == gender2index[gender])]
        if shuffle:
            dataset = dataset.sample(frac=1)
        datasets[(hair, gender)] = '../celebA/img_align_celeba/' + dataset.index.to_numpy()
    return datasets


def img_to_float32_centered(images):
    """ Convert images to float32 ranging from -1.0 to 1.0. """
    if not isinstance(images, np.ndarray):
        images = np.array(images, dtype=np.uint8)
    if images.dtype == np.uint8 and np.min(images) >= 0 and np.max(images) <= 255:
        images = images.astype(np.float32)
        return images / 127.5 - 1
    elif images.dtype == np.float32 and np.min(images) >= 0.0 and np.max(images) <= 1.0:
        return images * 2 - 1
    elif images.dtype == np.float32 and np.min(images) >= -1.0 and np.max(images) <= 1.0:
        return images
    else:
        raise ValueError('Argument images must either have dtype uint8 with range 0 - 255, or have dtype float32 with '
                         'range 0 -1 or -1 - 1.')


def img_to_uint8(images):
    """ Convert images to uint8 ranging from 0 to 255. """
    if not isinstance(images, np.ndarray):
        images = np.array(images, dtype=np.float32)
    if images.dtype == np.float32 and np.max(images) <= 1 and -1 <= np.min(images):
        images = ((images + 1) * 127.5).astype(np.uint8)
    elif images.dtype == np.float32 and np.max(images) <= 1 and np.min(images) >= 0:
        images = (images * 255).astype(np.uint8)

    return images


def get_label(hair_gender=None, hair='', gender=''):
    """ Return style label from string input. """

    if hair_gender is not None:
        hair, gender = hair_gender

    try:
        hair_label = hair_str2label[hair.lower()]
    except KeyError:
        raise ValueError('Invalid hair type.')

    try:
        gender_label = gender_str2label[gender.lower()]
    except KeyError:
        raise ValueError('Invalid gender type.')

    label = hair_label + gender_label
    label = np.array(label, dtype=np.float32)
    return label


def read_image(img_path):
    """ Reads an image from the given path. Returns a numpy array of the image. """
    img_size = 128
    # Original size (218, 178, 3), crop to square
    #image = Image.open(img_path).crop((0, 20, 178, 198)).resize((img_size, img_size))
    image = Image.open(img_path)
    image = img_to_float32_centered(image)
    return image


def read_images(img_path_list):
    """ Reads a list of images from a given list of paths. Returns a list of numpy arrays. """
    try:
        iter(img_path_list)
    except TypeError:
        img_path_list = [img_path_list]
    return [read_image(img_path) for img_path in img_path_list]


loaded_models = {}


def get_loaded_model(model_name):
    """ Retrieves and loads parameters for a model. """
    if model_name in loaded_models:
        return loaded_models[model_name]

    from models import get_G, get_D, get_Ea, get_Ec, get_RNN, get_CA
    get_model_fn = {
        'G':  get_G,
        'Ea': get_Ea,
        'Ec': get_Ec
    }
    model = get_model_fn[model_name]()
    model.train()
    save_dir = os.path.join(flags.model_dir, flags.prefix, '{}_{}.h5'.format(model_name, flags.test_epoch))
    if model.load_weights(save_dir) is False:
        raise RuntimeError("missing {} model".format(model_name))
    print('Loaded checkpoint from {}/{}...'.format(flags.model_dir, flags.prefix))
    loaded_models[model_name] = model
    return model


stopbyte = b'02'


def encode(data):
    data = data.replace(b'0', b'01')
    return data + stopbyte


def decode(data):
    data = data.replace(b'01', b'0')
    return data


def socket_read(conn):
    data = b''
    while True:
        new_data = conn.recv(1024)
        data += new_data
        if data.endswith(stopbyte):
            break
    return decode(data[:-2])
