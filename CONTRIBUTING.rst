.. highlight:: shell

To test : 

    $ flake8 repeatedtestframework tests
    $ python setup.py test
    $ tox

To build : 

    $ python setup.py bdist_wheel --universal

To upload : 

    $ twine upload dist/<recent release>
