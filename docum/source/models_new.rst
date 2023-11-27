=================
Модели баз данных
=================

.. raw:: html

    <style>
    img:hover {
        cursor: pointer;
    }
    </style>

    <br />
    <hr style="margin-top:50px; margin:auto; width:200px; height:2px; background-color:blue"  />
    <br />

    <div style="text-align: center;">
    <img title="Открыть в новой вкладке" src="_static/db_image.PNG" alt="img_db" style="width: 80%; height: 80%;" onclick="window.open(this.src)">
    </div>

    <br />
    <hr style="margin-top:50px; margin:auto; width:200px; height:2px; background-color:blue"  />
    <br />



.. note::

    | Тут хранятся модели базы данных
    | Используется sqlalchemy 1.4 declarative_base
    | Больше информации: https://docs.sqlalchemy.org/en/14/orm/tutorial.html


.. automodule:: model.model
    :members:
    :undoc-members:
    :exclude-members: Base, init_db
