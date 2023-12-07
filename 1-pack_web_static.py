#!/usr/bin/python3

from fabric.api import local
from datetime import datetime
import os


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
