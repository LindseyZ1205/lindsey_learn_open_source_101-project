.. image:: https://github.com/LindseyZ1205/lindsey_learn_open_source_101-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/LindseyZ1205/lindsey_learn_open_source_101-project/actions?query=workflow:CI

.. image:: https://img.shields.io/pypi/v/lindsey-learn-open-source-101.svg
    :target: https://pypi.python.org/pypi/lindsey-learn-open-source-101

.. image:: https://img.shields.io/pypi/l/lindsey-learn-open-source-101.svg
    :target: https://pypi.python.org/pypi/lindsey-learn-open-source-101

.. image:: https://img.shields.io/pypi/pyversions/lindsey-learn-open-source-101.svg
    :target: https://pypi.python.org/pypi/lindsey-learn-open-source-101

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/LindseyZ1205/lindsey_learn_open_source_101-project

------

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/LindseyZ1205/lindsey_learn_open_source_101-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/LindseyZ1205/lindsey_learn_open_source_101-project/issues


Welcome to ``lindsey_learn_open_source_101`` Documentation
==============================================================================

``lindsey_learn_open_source_101`` is Lindsey Zhang's first open source Python
library, created as a learning project to understand the structure and workflow
of professional Python open source projects.

The core functionality is simple: an ``add_two`` function that adds two integers.
But the project structure, tooling, testing, and documentation follow professional
open source standards.

.. _install:

Install
------------------------------------------------------------------------------

.. code-block:: console

    pip install lindsey_learn_open_source_101


Usage
------------------------------------------------------------------------------

.. code-block:: python

    from lindsey_learn_open_source_101 import api

    result = api.add_two(1, 2)
    print(result)  # 3
