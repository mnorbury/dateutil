from setuptools import setup, find_packages

setup(
        name = "lcogt-dateutils",
        version = "0.1.1",
        description = "Utility functions for manipulating datetimes",
        author = "Martin Norbury",
        author_email = "mnorbury@lcogt.net",
        url = "http://www.lcogt.net/",
        packages = find_packages('src'),
        package_dir = {'':'src'},
        test_suite="nose.collector",
        install_requires = []
     )
