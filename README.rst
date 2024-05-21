Open edX Extensions
###################

This repository serves as a comprehensive directory of various XBlocks available on the internet.
The challenge is that there are numerous XBlocks, apps, and third-party services scattered across different repositories and sites.
Existing directories, such as the `Confluence XBlocks Directory`_ and the `Open edX Extensions Directory`_, have their limitations.
The former is outdated and unmaintained, while the latter is closed, making it difficult to add new tools and does not contain all the tools.

Our goal is to create a centralized resource that lists both free and paid XBlocks for educators and developers.
While we strive to be as inclusive as possible, we recognize that some personal or commercial XBlocks may not be included.
We welcome contributions to keep this directory comprehensive and up-to-date. Help us make this resource valuable for everyone!

.. _Confluence XBlocks Directory: https://openedx.atlassian.net/wiki/spaces/COMM/pages/43385346/XBlocks+Directory
.. _Open edX Extensions Directory:

Usage
*****

Create a new virtual environment and install dependencies:

.. code-block::bash

    python -m venv .venv
    source .venv/bin/activate
    pip install requirements/base.txt


Then, build and serve the HTML:

.. code-block:: bash

    make html

You can access the page on http://127.0.0.1:8000

Contributing
************

Any contributions are welcome! Please check the `CONTRIBUTING`_ doc to learn how to contribute.

.. _CONTRIBUTING: CONTRIBUTING.rst

License
*******

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor/blob/master/LICENSE.txt>`_.
