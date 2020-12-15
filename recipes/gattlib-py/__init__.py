from pythonforandroid.recipe import PythonRecipe, IncludedFilesBehaviour
from pythonforandroid.toolchain import shprint, info
from pythonforandroid.util import current_directory
from pythonforandroid import logger
import sh
from glob import glob
from os.path import join
import os

class GattlibRecipe(IncludedFilesBehaviour, PythonRecipe):
    version = None
    url = None
    name = 'gattlib-py'
    site_packages_name = 'gattlib'

    src_filename = 'src'

    depends = ['pyjnius']
    call_hostpython_via_targetpython = False

    def should_build(self, arch):
        return True # always rebuild?

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        # to find jnius and identify p4a
        env['PYJNIUS_PACKAGES'] = self.ctx.get_site_packages_dir()
        return env

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)

        info('Copying java files to dist_dir')

        #destdir = join(self.ctx.bootstrap.dist_dir, 'src', 'main', 'java')
        #destdir = join(self.ctx.bootstrap.distribution.dist_dir, 'src', 'main', 'java')
        destdir = self.ctx.javaclass_dir
        #os.makedirs(destdir, exist_ok=True)

        for path in glob(join(self.get_build_dir(arch.arch), 'gattlib', '*.java')):
            shprint(sh.cp, '-a', path, destdir)

recipe = GattlibRecipe()
