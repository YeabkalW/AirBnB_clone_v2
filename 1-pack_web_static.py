#!/usr/bin/python3
"""python script that uses fabric to generate .tgz"""

from fabric.api import local
from datetime import datetime
from fabric.decorators import runs_once

@runs_once
def do_pack():
    '''uses fabric to generate .tgz for web_static folder'''
    local("mkdir -p versions")
    location = ("versions/web_static_{}.tgz".format(datetime.strftime
                                                    .now(), "%Y%m%d%H%M%S"))
    resp = local("tar -cvzf {} web_static".format(location))
    if resp.failed:
        return None
    return location