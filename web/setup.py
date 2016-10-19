from distutils.core import setup

setup(
    name='app',
    version='1',
    packages=['app',],
    license='MIT',
    install_requires=[
        "flask",
        "flask-login",
        "flask-sqlalchemy",
        "flask-classy",
        "itsdangerous",
        "cerberus",
        "passlib",
        "crypto",
        "jinja2",
        "flask-wtf",
        "ipdb",
        "docker-compose",
        "codecov"
    ],
)
