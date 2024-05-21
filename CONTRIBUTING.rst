Contributing
############

Any contributions are more than welcome. You can help us by adding new MFEs, apps, tools, services.

Add a new extension
*******************
First, let's see how the application works.

There are 2 YAML files in the root of the project called ``extensions.yml`` and ``vendors.yml``.
These 2 files act like the database of the app. each extension has a structure like These:

.. code-block:: yml

  - name: Problem Builder XBlock
    description: This repository provides Problem Builder and Step Builder XBlocks.
    category: Advanced learning tools
    license: AGPLv3
    vendor: Open Craft
    url: https://github.com/open-craft/problem-builder
    image: docs/_images/problem-builder-xblock.png


.. note:: Extensions can have an image or a YouTube link, or none.


To track the extensions, they all have a ``last_commit`` and a ``status`` field. You don't have to
populate them manually. just run the ``make update`` command and it will take care of it.

In the update process, you might hit the GitHub ratelimit.
To prevent this, go ahead and create a `GitHub Personal Token`_ and export it in your
terminal like this:

```bash
export GITHUB_TOKEN="ghp_abcdefg123456789"
```

.. _GitHub Personal Token: https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens