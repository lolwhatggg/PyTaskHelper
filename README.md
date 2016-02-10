Py.task
=======

Описание
--------
Проект состоит из трех частей:
1. Парсер сайта [AnyTask](http://anytask.urgu.org)
2. Расширение Chrome [Py.task Helper](https://goo.gl/QgQ9rC)
3. Сайт [Pytask.info](http://pytask.info)

### Парсер
Собирает информацию с курсов python.task и Perltask
сайта [AnyTask](http://anytask.urgu.org)

```parser/courseparser.py``` сохраняет данные по каждому из курсов python.task и Perltask в формате ```JSON``` в папку ```courses/```

```parser/statistics_maker.py``` сохраняет статистику по курсам из ```courses/``` в файлы:
+ ```database/tasks_base.json```
+ ```database/tasks_full.json```
+ ```database/categories.json```

### Расширение Chrome
Используя заранее постоенную статистику в формате ```JSON```, располагающуюся на сервере, изменяет страницы курсов python.task и Perltask на [AnyTask](http://anytask.urgu.org). Статистика отображается под названиями соответствующих задач.

### Сайт
Используется для просмотра подробной статистики по задачам<br>
Командой ```site/gulp``` запускается ```site/gulpfile.coffee```<br>
Сайт собирается в папке ```site/dist/```<br>
Компилирует файлы из ```site/jade/```, ```site/coffee/```, ```site/stylus/```<br>
Копирует файлы из ```site/external/```<br>
Чтобы сначала удалить папку ```site/dist/``` используется ```site/run.sh```, который также сам запускает ```gulp```

Используется
------------
 + Парсер
+ [Python](http://python.org/)
+ [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
 + Chrome Extension
+ [jQuery](https://jquery.com/)
 + Сайт
+ [npm](https://www.npmjs.com/)
+ [Gulp](https://gulpjs.com/)
+ [Jade](https://jade-lang.com/)
+ [Stylus](https://stylus-lang.com/)
+ [CoffeeScript](https://coffeescript.org/)
+ [jQuery](https://jquery.com/)
+ [Bootstrap](https://getbootstrap.com/)

Авторы
------
 + Слава Вихарев
+ [GitHub](https://github.com/SlavaVikharev)
+ [VK](https://vk.com/slavavikharev)
 + Антон Зырянов
+ [GitHub](https://github.com/avefablo/)
+ [VK](https://vk.com/id18048395)

&copy; Sinasey &amp; Avefablo 2016
