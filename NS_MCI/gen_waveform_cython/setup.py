from distutils.core import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy


link_args = ['-static-libgcc',
             '-static-libstdc++',
             '-Wl,-Bstatic,--whole-archive',
             '-lwinpthread',
             '-DMS_WIN64',
             '-Wl,--no-whole-archive']


class Build(build_ext):
    def build_extensions(self):
        if self.compiler.compiler_type == 'mingw32':
            for e in self.extensions:
                e.extra_link_args = link_args
        super(Build, self).build_extensions()


setup(
    cmdclass={'build_ext': Build},
    ext_modules=cythonize(Extension(
        'gen_waveform',
        sources=['gen_waveform.pyx'],
        language='c++',
        include_dirs=[numpy.get_include()],
        library_dirs=[],
        libraries=[],
        extra_compile_args=[],
        extra_link_args=[]
    )))
