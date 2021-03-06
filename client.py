"""
The client sends a pickle-encoded dictionary (similar to a JSON file) to the server.
The dict typically includes two keys, 'command' and 'args'.
- If the 'command' is quit, the function returns False and server quits.
- Else, command(*args) is executed and the result is sent back to the client.

The response sent to client is also a pickle-encoded dictionary/
The dict typically includes 'status' and 'result'.
- If 'status' is -1, the execution failed and the error message is in 'result'.
- If 'status' is 0, the execution is successful and the result is in 'result'.
"""

from time import time
import pickle, socket, os
from PIL import Image
import numpy as np
from util import read_image, encode, socket_read, img_encode, img_decode, img_to_uint8


class ServerInfo:
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 6666  # The port used by the server


def get_result(command, arguments, host=ServerInfo.host, port=ServerInfo.port):
    """ Performs a remote process call `command(*arguments)` """
    data = pickle.dumps({'command': command, 'args': arguments})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encode(data))
        if command == 'quit':
            return
        print('%d bytes of data sent, awaiting result...' % len(data))
        # read result from server
        start = time()
        result = socket_read(s)
        end = time()
        print('Received results of {} bytes. Wait time: {} seconds.'.format(len(result), end - start))
        result = pickle.loads(result)
        if result['status'] == 0:
            return result['result']
        else:
            raise ValueError(result['result'])


def save_result(result, save_path, key_is_filename=False):
    """
    Saves the server-returned result to images under save_path.

    :param result: A dictionary with attributes as keys and image of size (128, 128, 3) as values.
    :param save_path: A str. Path to save the result images.
    :param key_is_filename: A boolean. Whether the dict keys are the filename strings.

    :return: None.
    """
    for key, img in result.items():
        img = img_to_uint8(img)
        img = Image.fromarray(img, mode='RGB')
        if key_is_filename:
            filename = key + '.png'
        else:
            filename = '{}.png'.format('-'.join(map(str, key)))
        img.save(os.path.join(save_path, filename))


def img_get_all(img_content, img_appearance1=('black', 'male'), img_appearance2=('blonde', 'female'),
                labels_str=(('', ''), ('black', 'male'), ('blonde', 'female')),
                n_gaussian_appearance=3, n_interpolates=4, save_path='', server_save_path='', n_sampled_content=5):
    """
    Return results of all applications of DLGAN.

    Application 1: Transform the img_content with every possible label. Returns len(flags.labels_str) images.
    Application 2: Transform the img_content with both img_appearance1 and labels in labels_str. Returns len(labels_str)
      images.
    Application 3: Transform the img_content with both sampled gaussian appearances and labels in labels_str. Returns
      n_gaussian_appearance * len(labels_str) images.
    Application 4: Transform the img_content with appearance interpolation between img_appearance1 and img_appearance2
       and labels in labels_str. Returns n_interpolates * len(labels_str) images.

    :param img_content: Numpy NDArray of shape (128, 128, 3) or str. The image to be transformed.
    :param img_appearance1: Numpy NDArray of shape (128, 128, 3) or tuple of str. The first appearance image. When
      provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param img_appearance2: Numpy NDArray of shape (128, 128, 3) or tuple of str. The second appearance image. When
      provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param labels_str: A list of (hair, gender) label strings. If None, all possible labels are used. Recommended length
      is 2 or 3, in which case the computation cost is affordable.
    :param n_gaussian_appearance: An int. Number of gaussian appearances to sample.
    :param n_interpolates: An int. Number of interpolates to be generated.
    :param save_path: A str. Path to save the transformed images, with name `app-hair-gender-[alpha].png`. If empty
      (default), do not save the images.
    :param server_save_path: A str. Path to save all generated images on the server (for debugging). If empty, do not
      save the images.
    :param n_sampled_content: An int. Number of sampled content images of each dataset. Larger value leads to higher
      quality of generated images (since the model uses batch normalization, it is necessary to keep a certain degree of
      diversity to obtain good performance).

    :return: A dictionary of (len(flags.labels_str) + len(labels_str) * (1 + n_gaussian_appearance + n_interpolates)) of
      DLGAN-generated images, each with shape (128, 128, 3) and scale [-1., 1]. The key to the dictionary is a string
      formatted as 'app-hair-gender-[alpha]', where app is the application (see above), hair is '', 'brown', 'blonde' or
      'black', gender is '', 'male' or 'female' (empty string indicates that the feature is unmodified.), and alpha is
      the interpolation coefficient and is not present in applications 1-3.
    """
    # read and encode the images
    if isinstance(img_content, str):
        img_content = read_image(img_content)
    if isinstance(img_appearance1, str):
        img_appearance1 = read_image(img_appearance1)
    if isinstance(img_appearance2, str):
        img_appearance2 = read_image(img_appearance2)
    img_content = img_encode(img_content)
    if isinstance(img_appearance1, np.ndarray):
        img_appearance1 = img_encode(img_appearance1)
    if isinstance(img_appearance2, np.ndarray):
        img_appearance2 = img_encode(img_appearance2)
    result = get_result('img_get_all', (img_content, img_appearance1, img_appearance2, labels_str,
                                        n_gaussian_appearance, n_interpolates, server_save_path, n_sampled_content))
    result = {k: img_decode(v) for k, v in result.items()}
    if save_path:
        save_result(result, save_path, key_is_filename=True)
    return result


def img_transform(img_content, img_appearance=None, labels_str=None, gaussian_appearance=False,
                  save_path='', server_save_path='', n_sampled_img=5):
    """
    Transforms the img_content with labels specified in labels_str and (optional) appearance image.

    :param img_content: Numpy NDArray of shape (128, 128, 3) or str. The image to be transformed.
    :param img_appearance: Numpy NDArray of shape (128, 128, 3) or str. The image providing appearance information. If
      None (default), it is equal to the img_content.
    :param labels_str: A list of (hair, gender) label strings. If None (default), all possible labels are used.
    :param gaussian_appearance: A bool. Whether to use gaussian random variable as appearance encodings.
    :param save_path: A str. Path to save the transformed images, with name `hair-gender.png`. If empty (default), do
      not save the images.
    :param server_save_path: A str. Path to save the transformed images, along with the transformed sampled images.
      If empty (default), do not save the images.
    :param n_sampled_img: An int. Number of sampled images of each dataset (since the model uses batch normalization, it
      is necessary to keep a certain degree of diversity to obtain good performance).

    :return: A dictionary of transformed images, each with shape (128, 128, 3). The key to the dictionary is (hair,
      gender), where hair is '', 'brown', 'blonde' or 'black', and gender is '', 'male' or 'female'. Empty string
      indicates that the feature is unmodified.
    """
    # read and encode the images
    if isinstance(img_content, str):
        img_content = read_image(img_content)
    if img_appearance is not None and isinstance(img_appearance, str):
        img_appearance = read_image(img_appearance)
    img_content = img_encode(img_content)
    if img_appearance is not None:
        img_appearance = img_encode(img_appearance)
    result = get_result('img_transform', (img_content, img_appearance, labels_str, gaussian_appearance,
                                          server_save_path, n_sampled_img))
    result = {k: img_decode(v) for k, v in result.items()}
    if save_path:
        save_result(result, save_path)
    return result


def img_interpolate(img_content, img_appearance1=('black', 'male'), img_appearance2=('blonde', 'female'),
                    n_interpolates=4, labels_str=(('', ''),), save_path='', server_save_path='', n_sampled_img=5):
    """
    Interpolate the img_content based on the appearance encodings of img_appearance1 and img_appearance2.

    :param img_content: Numpy NDArray of shape (128, 128, 3) or str. The content image.
    :param img_appearance1: Numpy NDArray of shape (128, 128, 3) or tuple of str or str. The first appearance image.
      When provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param img_appearance2: Numpy NDArray of shape (128, 128, 3) or tuple of str or str. The second appearance image.
      When provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param n_interpolates: An int. Number of interpolates to be generated.
    :param labels_str: A list of (hair, gender) label strings. If None, all possible labels are used. Default to (('',
      ''),), which means no explicit label is provided.
    :param save_path: A str. Path to save the transformed images, with name `hair-gender.png`. If empty (default), do
      not save the images.
    :param server_save_path: A str. Path to save the interpolated images, along with some interpolated sampled images.
      If empty, do not save the images.
    :param n_sampled_img: An int. Number of sampled images of each dataset (since the model uses batch normalization, it
      is necessary to keep a certain degree of diversity to obtain good performance).

    :return: A dictionary of lists of interpolated images, each with shape (128, 128, 3). The interpolates are generated
      from the convex combination of the appearance encodings of img_appearance1 and img_appearance2, guided with the
      content encoding of img_content. The key to the dictionary is (hair, gender, alpha), where hair is '', 'brown',
      'blonde' or 'black', gender is '', 'male' or 'female' (empty string indicates that the feature is unmodified.),
      and alpha is the interpolation coefficient.
    """
    # read and encode the images
    if isinstance(img_content, str):
        img_content = read_image(img_content)
    if isinstance(img_appearance1, str):
        img_appearance1 = read_image(img_appearance1)
    if isinstance(img_appearance2, str):
        img_appearance2 = read_image(img_appearance2)
    img_content = img_encode(img_content)
    if isinstance(img_appearance1, np.ndarray):
        img_appearance1 = img_encode(img_appearance1)
    if isinstance(img_appearance2, np.ndarray):
        img_appearance2 = img_encode(img_appearance2)
    result = get_result('img_interpolate', (img_content, img_appearance1, img_appearance2,
                                            n_interpolates, labels_str, server_save_path, n_sampled_img))
    result = {k: img_decode(v) for k, v in result.items()}
    if save_path:
        save_result(result, save_path)
    return result


def kill_server():
    """ Sends a quit command to the server """
    get_result('quit', None)


if __name__ == '__main__':
    # img_get_all('face/face0.png')

    image = img_get_all('../celebA/img_align_celeba/177299.jpg')  # use read_image to read an image
    '''
    #result = img_transform(image)
    #result = img_transform(image)  # test 1
    #result = img_transform(image, image)  # test 2
    #result = img_transform(image, gaussian_appearance=True)  # test 3
    result = img_get_all(image, save_path='DLGAN')  # test 4
    # _start_shell(locals())
    '''
