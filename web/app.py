import cherrypy
from deepdreamer.deepdreamer import deepdream, deepdream_video, list_layers
import os, sys
from pathlib import Path
from PIL import Image
import PIL

class App(object):
    def __init__(self):
        self.FILE_NAME = 'dream.jpg'

    def path(self, subpath):
        return os.path.abspath(os.getcwd()) + '/web/public' + subpath

    def purge(self, dir, pattern):
        for p in Path(dir).glob(pattern):
            p.unlink()

    def upload_path(self):
        return self.path('/upload')

    @cherrypy.expose
    def upload(self, ufile):
        # Either save the file to the directory where server.py is
        # or save the file to a given path:
        # upload_path = '/path/to/project/data/'
        upload_path = self.upload_path()

        # Save the file to a predefined filename
        # or use the filename sent by the client:
        # upload_filename = ufile.filename
        upload_filename = self.FILE_NAME

        upload_file = os.path.normpath(os.path.join(upload_path, upload_filename))
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = ''

        try:
            im: PIL.Image = Image.open(upload_file)
            im.thumbnail((640, 480), PIL.Image.ANTIALIAS)
            im.save(upload_file, "JPEG")
        except IOError:
            print("cannot create thumbnail for", upload_file)

        print("upload:", upload_file)
        self.dream(upload_file)
        raise cherrypy.HTTPRedirect("/")

    def dream(self,
              image,
              zoom=True,
              scale=0.05,
              dreams=10,
              itern=10,
              octaves=4,
              octave_scale=1.4,
              layers='inception_4c/output',
              clip=True,
              # choices=['bvlc_googlenet', 'googlenet_place205']
              network='bvlc_googlenet',
              gif=True,
              reverse=False,
              # of one gif frame
              duration=1,
              loop=False,
              # for video
              framerate=24,
              gpuid=0,
              gpu=True):

        try:
            deepdream(
                image, zoom=zoom, scale_coefficient=scale,
                irange=dreams, iter_n=itern, octave_n=octaves,
                octave_scale=octave_scale, end=layers, clip=clip,
                network=network, gif=gif, reverse=reverse,
                duration=duration, loop=loop, gpu=gpu, gpuid=gpuid)
        except Exception as e:
            print("Error: {}".format(e))
            sys.exit(2)
        finally:
            self.purge(self.upload_path(), self.FILE_NAME + '_*')
