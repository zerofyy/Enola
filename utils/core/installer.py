import sys
import os
import subprocess
from importlib import metadata
from packaging import requirements

from utils.logging import Logger


Logger = Logger()


class Installer:
    """ Class for installing python modules. """

    def check_requirements(self) -> dict[str, str]:
        """
        Check the required modules.

        Returns:
             A dictionary with missing or outdated requirements.
        """

        Logger.log('checking requirements...')

        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

        bad_reqs = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            is_ok, req, info = self.check_module(line)

            if not is_ok:
                bad_reqs[req.name] = info
                Logger.log(f'module is {info}')

            else:
                Logger.log('module is ok')

        return bad_reqs


    @staticmethod
    def check_module(module: str) -> tuple[bool, requirements.Requirement, str]:
        """
        Check whether a module is installed and up-to-date.

        Arguments:
            module: The python module being checked with optional version specifiers.

        Returns:
            Whether the module is installed and up-to-date and information regarding its state.
        """

        req = requirements.Requirement(module)
        try:
            metadata.distribution(req.name)

            installed_version = metadata.version(req.name)
            if req.specifier and not req.specifier.contains(installed_version):
                return False, req, 'outdated'

        except metadata.PackageNotFoundError:
            return False, req, 'missing'

        return True, req, 'OK'


    @staticmethod
    def install_module(module: str) -> None:
        """
        Install a python module.

        Arguments:
             module: The python module being installed with optional version specifiers.
        """

        Logger.log('installing module...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module],
                              stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    @staticmethod
    def update_module(module: str) -> None:
        """
        Update a python module.

        Arguments:
             module: The python module being updated with optional version specifiers.
        """

        Logger.log('updating module...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module, '--upgrade'],
                              stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def ensure_requirements(self) -> None:
        """ Check for and install any missing or outdated requirements. """

        Logger.log('checking requirements...')

        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            is_ok, req, info = self.check_module(line)
            if is_ok:
                Logger.log('module is ok')
                continue

            Logger.log(f'module is {info}')

            if info == 'missing':
                self.install_module(line)

            elif info == 'outdated':
                self.update_module(line)


    @staticmethod
    def restart() -> None:
        """ Restart the bot. """

        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('python main.py')
        sys.exit(0)


__all__ = ['Installer']
