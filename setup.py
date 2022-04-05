import os
import sys
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.13'  # 10.13, supports >= high-sierra

# get numpy as dependency when it is not pre-installed
# from: https://stackoverflow.com/a/54128391/798093
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        import builtins
        builtins.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

py_version   = sys.version[0]
package_name = 'SimpleCRF-binaries'

compile_args = []
if sys.platform.startswith('linux'):
    # Override platform tag for linux
    sys.argv.append('--plat-name') 
    sys.argv.append('manylinux1_x86_64')
elif sys.platform.startswith('darwin'):
    # Override platform tag, or it gets tag 10_15 for some reason
    sys.argv.append('--plat-name')
    sys.argv.append('macosx_10_13_x86_64')

    # set OSX Deploment Target to 10.13
    compile_args = ['-Xclang', '-mmacosx-version-min=10.13']


module_name1   = 'maxflow'
maxflow_source = "maxflow_python/wrap_py{0:}.cpp".format(py_version)
module1 = Extension(module_name1,
                    include_dirs = ['./dependency', './maxflow_python'],
                    sources = ['maxflow_python/maxflow.cpp', 
                               'maxflow_python/util.cpp',
                               'dependency/maxflow-v3.0/graph.cpp', 
                               'dependency/maxflow-v3.0/maxflow.cpp',
                                maxflow_source],
                    extra_compile_args=compile_args,
                    py_limited_api=False)

module_name2    = 'denseCRF'
densecrf_source = "densecrf_python/wrap2D_py{0:}.cpp".format(py_version)
module2 = Extension(module_name2,
                    include_dirs = [ 
                                    './dependency/densecrf/include', 
                                    './dependency/densecrf/external/liblbfgs/include'], 
                    sources=['./densecrf_python/densecrf.cpp',
                            './densecrf_python/densecrf_core.cpp',
                            './dependency/densecrf/src/densecrf.cpp',
                            './dependency/densecrf/src/labelcompatibility.cpp',
                            './dependency/densecrf/src/objective.cpp',
                            './dependency/densecrf/src/optimization.cpp',
                            './dependency/densecrf/src/pairwise.cpp',
                            './dependency/densecrf/src/permutohedral.cpp',
                            './dependency/densecrf/src/unary.cpp',
                            './dependency/densecrf/src/util.cpp',
                            './dependency/densecrf/external/liblbfgs/lib/lbfgs.c', 
                            densecrf_source,
                            ],
                    extra_compile_args=compile_args,
                    py_limited_api=False)

module_name3    = 'denseCRF3D'
densecrf_source = "densecrf_python/wrap3D_py{0:}.cpp".format(py_version)
module3 = Extension(module_name3,
                    include_dirs = [ 
                                    './dependency/densecrf3d/include', 
                                    './dependency/densecrf/external/liblbfgs/include'], 
                    sources=['./densecrf_python/densecrf3d.cpp',
                            './densecrf_python/densecrf3d_util.cpp',
                            './dependency/densecrf3d/src/densecrf.cpp',
                            './dependency/densecrf3d/src/labelcompatibility.cpp',
                            './dependency/densecrf3d/src/objective.cpp',
                            './dependency/densecrf3d/src/optimization.cpp',
                            './dependency/densecrf3d/src/pairwise.cpp',
                            './dependency/densecrf3d/src/permutohedral.cpp',
                            './dependency/densecrf3d/src/unary.cpp',
                            './dependency/densecrf3d/src/util.cpp',
                            './dependency/densecrf/external/liblbfgs/lib/lbfgs.c', 
                            densecrf_source,
                            ],
                    extra_compile_args=compile_args,
                    py_limited_api=False)

# Get the summary
description = 'An open-source toolkit for conditional random field (CRF) and dense CRF'

# Get the long description
if (sys.version[0] == '2'):
    import io
    with io.open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(name=package_name,
      version = "0.2.1.2",
      author  ='Guotai Wang and André Pedersen',
      author_email = 'wguotai@gmail.com',
      description  = description,
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      url      = 'https://github.com/andreped/SimpleCRF/tree/binaries',
      license  = 'BSD',
      packages = setuptools.find_packages(),
      ext_modules = [module1, module2, module3],
      classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
      ],
      python_requires = '>=3.6',
      cmdclass={'build_ext': build_ext},)


# to build, run python setup.py build or python setup.py build_ext --inplace
# to install, run python setup.py install
