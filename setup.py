# Python3 version:
# Copyright (c) 2022 blackPanther Europe (www.blackpanther.hu)
#
#  - CODE BASED ON Calin Crisan <ccrisan@gmail.com> works -
#
# Authors: 
#    Chareles K Barcza <kbarcza@blackpanther.hu>
#    Miklos Horvath <hmiki@blackpanther.hu>

import os.path

from codecs import open
from setuptools import setup
from setuptools.command.sdist import sdist

import motioneye


here = os.path.abspath(os.path.dirname(__file__))
name = 'motioneye3'
version = motioneye.VERSION

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class SdistCommand(sdist):
    def make_release_tree(self, base_dir, files):
        sdist.make_release_tree(self, base_dir, files)
        self.apply_patches(base_dir)
        
    def apply_patches(self, base_dir):
        dropbox_keys_file = os.path.join(os.getcwd(), base_dir, 'extra', 'dropbox.keys')
        if os.path.exists(dropbox_keys_file):
            g = {}
            execfile(dropbox_keys_file, g)
            upload_services_file = os.path.join(os.getcwd(), base_dir, 'motioneye', 'uploadservices.py')
            if os.system("sed -i 's/dropbox_client_id_placeholder/%s/' %s" % (g['CLIENT_ID'], upload_services_file)):
                raise Exception('failed to patch uploadservices.py')
            if os.system("sed -i 's/dropbox_client_secret_placeholder/%s/' %s" % (g['CLIENT_SECRET'], upload_services_file)):
                raise Exception('failed to patch uploadservices.py')


setup(
    name=name,
    version=version,

    description='motionEye3 server',
    long_description=long_description,

    url='https://github.com/blackPantherOS/motionEye3/',

    author='Charles K Barcza (Py3) based on Calin Crisan work',
    author_email='info@blackpanther.hu',

    license='GPLv3',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11'
    ],

    keywords='motion video surveillance frontend',

    packages=['motioneye'],

    install_requires=['tornado>=5.1,<6', 'jinja2', 'pillow', 'pycurl'],

    package_data={
        'motioneye': [
            'static/*.*',
            'static/*/*',
            'templates/*',
            'scripts/*'
        ]
    },

    data_files=[
        (os.path.join('share/%s' % name, root), [os.path.join(root, f) for f in files])
                for (root, dirs, files) in os.walk('extra')
    ],

    entry_points={
        'console_scripts': [
            'meyectl=motioneye.meyectl:main',
        ],
    },
    
    cmdclass={
        'sdist': SdistCommand
    }
)
