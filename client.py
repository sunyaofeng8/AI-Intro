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
import pickle, socket
from PIL import Image
from util import read_image, encode, socket_read, img_to_uint8

class ServerInfo:
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 6666  # The port used by the server


def do_client(command, arguments, host=ServerInfo.host, port=ServerInfo.port):
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


def img_transform(img, save_path=''):
    """
    Transforms the image with every tag possible.

    :param img: Numpy NDArray of shape (128, 128, 3). The image to be transformed.
    :param save_path: A str. Path to save the transformed images, along with some transformed sampled images (since the
      model uses batch normalization, it is necessary to keep a certain degree of diversity to obtain good performance).
      If empty, do not save the images.

    :return: A dictionary of transformed images, each with shape (128, 128, 3). The key to the dictionary is (hair,
      gender), where hair is '', 'brown', 'blonde' or 'black', and gender is '', 'male' or 'female'. Empty string
      indicates that the feature is unmodified.
    """
    return do_client('img_transform', (img, save_path))


def img_interpolate(img_content, img_appearance1=('black', 'male'), img_appearance2=('blonde', 'female'),
                    n_interpolates=4, save_path=''):
    """
    Interpolate the img_content based on the appearance encodings of img_appearance1 and img_appearance2.

    :param img_content: Numpy NDArray of shape (128, 128, 3). The content image.
    :param img_appearance1: Numpy NDArray of shape (128, 128, 3) or tuple of str. The first appearance image. When
      provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param img_appearance2: Numpy NDArray of shape (128, 128, 3) or tuple of str. The second appearance image. When
      provided with tuple of str (hair, gender), sample randomly from img_datasets[(hair, gender)].
    :param n_interpolates: An int. Number of interpolates to be generated.
    :param save_path: A str. Path to save the interpolated images, along with some interpolated sampled images (since
      the model uses batch normalization, it is necessary to keep a certain degree of diversity to obtain good
      performance). If empty, do not save the images.

    :return: A dictionary of lists of interpolated images, each with shape (n_interpolates, 128, 128, 3). The
      interpolates are generated from the convex combination of the appearance encodings of img_appearance1 and
      img_appearance2, guided with the content encoding of img_content. The key to the dictionary is (hair, gender),
      where hair is '', 'brown', 'blonde' or 'black', and gender is '', 'male' or 'female'. Empty string indicates that
      the feature is unmodified.
    """
    return do_client('img_interpolate', (img_content, img_appearance1, img_appearance2, n_interpolates, save_path))


def kill_server():
    """ Sends a quit command to the server """
    do_client('quit', None)

def DL_GAN(fp):
    image = read_image(fp)
    result = img_transform(image)

    for key in result:
        img = result[key]
        img = img_to_uint8(img)
        img = Image.fromarray(img.astype('uint8')).convert('RGB')

        img_name = key[0] + '-' + key[1]
        img.save('DLGAN/%s.png' % img_name)

if __name__ == '__main__':
    #image = read_image('../celebA/img_align_celeba/177299.jpg')  # use read_image to read an image
    
    DL_GAN('face/face0.png')
    
    '''
    def _start_shell(local_ns):
        # An interactive shell useful for debugging/development.
        import IPython
        user_ns = {}
        if local_ns:
            user_ns.update(local_ns)
        user_ns.update(globals())
        IPython.start_ipython(argv=[], user_ns=user_ns)
    _start_shell(locals())
    '''
