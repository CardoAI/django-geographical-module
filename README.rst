===============
Django Geographical Module
===============

Quick start
-----------

1. Add "geographical_module" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'geographical_module',
    ]

2. Run ``python manage.py migrate`` to create the models.

3. Run ``python manage.py load_initial_nuts_data`` to populate the database with the NUTS values.
