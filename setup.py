"""Build and install Planet Rock radio track listing."""
# Copyright (c) 2012 Andrew Dawson
#
# See the file license.txt for copying permission.


from distutils.core import setup


setup(
    name="planetrock",
    version="1.0",
    description="List recently played tracks on Planet Rock radio.",
    author="Andrew Dawson",
    author_email="adawsonis@googlemail.com",
    packages=["planetrock"],
    package_dir={"planetrock": "lib"},
    scripts=["bin/prock"],
)

