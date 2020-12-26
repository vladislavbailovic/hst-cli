import setuptools

setuptools.setup(
    name = "hst-cli",
    version = "0.0.1",
    description = "hst-cli is package and a command line tool for manipulating the hosts file",
    packages = setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            'hst = hst:hst_cli.main'
        ]
    },
    python_requires = ">=3.8"
)
