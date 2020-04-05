from cleo import Command
import os
import shutil
import zipfile
from ..exceptions import ProjectLimitReached


class NewCommand(Command):
    """
    Creates a new Masonite project

    new
        {name? : Name of your Masonite project}
        {target? : Path of you Masonite project}
        {--b|--branch=False : Specify which branch from the Masonite repo you would like to install}
        {--r|--release=False : Specify which version of Masonite you would like to install}
    """

    def handle(self):
        name = self.argument('name')
        if not name:
            name = 'project'

        target = self.argument('target')

        if not target:
            target = '.'

        branch = self.option('branch')
        version = self.option('release')
        if not os.path.isdir(os.path.join(os.getcwd(), name)):
            from io import BytesIO
            import requests

            for directory in os.listdir(os.getcwd()):
                if directory.startswith('masonite-'):
                    return self.comment('There is a folder that starts with "masonite-" and therefore craft cannot create a new project')
            try:
                if branch != 'False':
                    get_branch = requests.get(
                        'https://api.github.com/repos/MasoniteFramework/cookie-cutter/branches/{0}'.format(branch))

                    if 'name' not in get_branch.json():
                        return self.comment('Branch {0} does not exist.'.format(branch))

                    zipball = 'https://github.com/MasoniteFramework/cookie-cutter/archive/{0}.zip'.format(branch)
                elif version != 'False':
                    get_zip_url = requests.get(
                        'https://api.github.com/repos/MasoniteFramework/cookie-cutter/releases')
                    zipball = False

                    for release in get_zip_url.json():
                        if 'tag_name' in release and release['tag_name'].startswith('v{0}'.format(version)):
                            self.info('Installing version {0}'.format(release['tag_name']))
                            self.line('')
                            zipball = release['zipball_url']
                            break

                    if zipball is False:
                        return self.info('Version {0} could not be found'.format(version))
                else:
                    get_zip_url = requests.get(
                        'https://api.github.com/repos/MasoniteFramework/cookie-cutter/releases')
                    tags = []

                    for release in get_zip_url.json():
                        if release['prerelease'] is False:
                            tags.append(release['tag_name'].replace('v', ''))

                    tags = sorted(tags, key=lambda v: [int(i) for i in v.split('.')], reverse=True)

                    get_zip_url = requests.get(
                        'https://api.github.com/repos/MasoniteFramework/cookie-cutter/releases/tags/v{0}'.format(tags[0]))

                    zipball = get_zip_url.json()['zipball_url']
            except TypeError:
                raise ProjectLimitReached('You have reached your hourly limit of creating new projects. Try again in 1 hour.')
            success = False

            zipurl = zipball

            self.info('Crafting Application ...')

            try:
                # Python 3
                from urllib.request import urlopen

                with urlopen(zipurl) as zipresp:
                    with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall(os.getcwd())

                success = True
            except ImportError:
                # Python 2
                import urllib
                r = urllib.urlopen(zipurl)
                with zipfile.ZipFile(BytesIO(r.read())) as z:
                    z.extractall(os.getcwd())

                success = True
            except Exception as e:
                raise e

            if success:
                for directory in os.listdir(os.getcwd()):
                    if directory.startswith('MasoniteFramework-cookie-cutter') or directory.startswith('cookie-cutter-'):
                        if target == '.':
                            from_dir = os.path.join(os.getcwd(), '{0}'.format(directory))
                            to_dir = os.path.abspath(os.path.expanduser(target))

                            for file in os.listdir(from_dir):
                                shutil.move(os.path.join(from_dir, file), to_dir)
                            os.rmdir(from_dir)
                        else:
                            os.rename(os.path.join(os.getcwd(), '{0}'.format(directory)), os.path.join(os.getcwd(), target))

                        self.info('Application Created Successfully!')
                        self.info('Installing Dependencies ')
                        if target == '.':
                            self.call('install')

                            self.info('Installed Successfully. Just Run `craft serve` To Start Your Application.')
                        else:
                            self.info("Project Created Successfully. You now will have to CD into your new '{}' directory and run `craft install` to complete the installation".format(target))

                        return

            else:
                self.comment('Could Not Create Application :(')
        else:
            self.comment('Directory {0} already exists. Please choose another project name'.format(name))
