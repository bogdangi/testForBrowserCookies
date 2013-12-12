Тестовое задание на вакансию Инженера по автоматизации тестирования (Яндекс.Браузер)
====================================================================================

Вам необходимо составить и автоматизировать необходимый и достаточный набор
тестовых сценариев для проверки работы механизма http cookie в браузере
`google chrome`.

В ответ мы хотели бы получить:

- Описание тестовых сценариев.
- Автотест, написанный на языке python 2.x, с использованием selenium webdriver.

.. contents::

INSTALL
=======

Instal Google Chrome
--------------------

For example for Ubuntu::

    $ apt-get install google-chrome-stable

Install chrome web driver
-------------------------

Download web driver from http://chromedriver.storage.googleapis.com/index.html

For example for linux i386::

    $ wget http://chromedriver.storage.googleapis.com/2.7/chromedriver_linux32.zip

Unzip and make link on web driver::

    $ unzip chromedriver_linux32.zip
    $ ln chromedriver /usr/local/bin/chromedriver

Install environment
-------------------

Build project::

    $ python bootstrap.py
    $ bin/buildout
    

Running auto tests
==================

Run tests::

    $ bin/pybot tests/
