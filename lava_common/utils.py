# Copyright (C) 2018 Linaro Limited
#
# Author: Remi Duraffort <remi.duraffort@linaro.org>
#
# This file is part of LAVA.
#
# LAVA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# LAVA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along
# with this program; if not, see <http://www.gnu.org/licenses>.

import contextlib
import subprocess  # nosec dpkg
from lava_common.exceptions import InfrastructureError


def debian_package_arch(pkg):
    """
    Relies on Debian Policy rules for the existence of the
    changelog. Distributions not derived from Debian will
    return an empty string.
    """
    with contextlib.suppress(FileNotFoundError, subprocess.CalledProcessError):
        return (
            subprocess.check_output(  # nosec dpkg-query
                ("dpkg-query", "-W", "-f=${Architecture}\n", "%s" % pkg)
            )
            .strip()
            .decode("utf-8", errors="replace")
        )
    return ""


def debian_package_version(pkg):
    """
    Use dpkg-query to retrive the version of the given package.
    Distributions not derived from Debian will return an empty string.
    """
    with contextlib.suppress(FileNotFoundError, subprocess.CalledProcessError):
        return (
            subprocess.check_output(  # nosec dpkg-query
                ("dpkg-query", "-W", "-f=${Version}\n", "%s" % pkg)
            )
            .strip()
            .decode("utf-8", errors="replace")
        )
    return ""


def debian_filename_version(binary, label=False):
    """
    Relies on Debian Policy rules for the existence of the
    changelog. Distributions not derived from Debian will
    return an empty string.
    """
    # if binary is not absolute, fail.
    msg = "Unable to retrieve version of %s" % binary
    try:
        pkg_str = (
            subprocess.check_output(("dpkg-query", "-S", binary))  # nosec dpkg-query
            .strip()
            .decode("utf-8", errors="replace")
        )
        if not pkg_str:
            raise InfrastructureError(msg)
    except subprocess.CalledProcessError:
        raise InfrastructureError(msg)
    pkg = pkg_str.split(":")[0]
    pkg_ver = debian_package_version(pkg)
    if not label:
        return pkg_ver
    return "%s for <%s>, installed at version: %s" % (pkg, binary, pkg_ver)
