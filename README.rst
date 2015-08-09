NIMPLY
------

Or **N**-ot **IMPL**-emented **Y**-et it is tool for doing code reviews in files aside from CVS (GitHub, GitLab and etc).

It is may be useful when you make review for whole file and not concrete revision. Or may be colleague sended file directly for your eyes. Or in your team used SVN who dont have nice web gui and branching practice.

It is my fun project and you can use or not use it on own risk. All contribution are welcome in any way.

**Technologies used**:

* Flask
* Mongodb
* ReactJs

INSTALL
=======

If is Flask based project.

Checkout the code, up virtualenv and install dependencies:

.. code:: bash

    pip install -r requirements-dev.txt

Then need to install static dependencies:

.. code:: bash

    cd static
    npm install


DEVELOP
=======

For building static in project i'm using ``Gulp`` so look inside ``static/gulpfile.js`` for available tasks.

Default (builds all: jsx and less files):

.. code:: bash

    cd static
    gulp
