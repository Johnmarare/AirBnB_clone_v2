#!/usr/bin/python3
# Full deployment


from fabric.api import *
import os
from datetime import datetime


env.hosts = ['34.203.201.80', '54.237.86.111']
env.user = 'ubuntu'


def do_pack():
    """
    generates a .tgz archive from contents of the web_static
    """
    try:
        # Create the Versions folder if doesnt exist
        local("mkdir -p versions")

        # Create name of the archive
        time = datetime.now()
        timestamp = time.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Compress the contents of the web_static folder
        local("tar -czvf versions/{} web_static".format(archive_name))

        # if succesful return the archive
        return os.path.join("versions", archive_name)
    except Exception as e:
        # Return None if error occurs
        return None


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
        run('mv {}/web_static/* /{}'.format(release_folder, release_folder))
        run('rm -rf {}/web_static'.format(release_folder))

        # Delete the symbolic link
        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))

        # Create new link
        run('ln -s {} {}'.format(release_folder, current_link))

        print('New version deployed!')

        return True
    except Exception as e:
        return False


def deploy():
    """
    Function that creates and distributes an archive to my web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
