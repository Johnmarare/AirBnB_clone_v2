#!/usr/bin/python3
# Fabfile that distributes an archive to my web servers


import os
from fabric.api import *


env.hosts = ['34.203.201.80', '54.237.86.111']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Funtion to distribute an archive to my web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive to the /tmp/ directory on web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to folder in web server
        # Extract the filename from the folder
        archive_name = os.path.basename(archive_path)
        release_folder = '/data/web_static/releases/{}'.format(
                os.path.splitext(archive_name)[0])

        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_folder))

        # Delete the archive from webserver
        run('rm /tmp/{}'.format(archive_name))

        # Delete the symbolic link
        current_link = '/data/web_static/current'
        run('rm -f {}'.format(current_link))

        # Create new link
        run('ln -s {} {}'.format(release_folder, current_link))

        print('New version deployed!')

        return True
    except Exception as e:
        print(e)
        return False
