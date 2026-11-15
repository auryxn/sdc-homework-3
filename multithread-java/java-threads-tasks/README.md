# Java Threads Management — решения

Проект состоит из независимых задач. Нужен JDK 17 или новее. Исходники находятся в `src/main/java/tasks`.

Компиляция всех задач:

```bash
mkdir -p out
javac -d out src/main/java/tasks/*.java
```

Запуск отдельной задачи из папки проекта:

```bash
java -cp out tasks.Task1
java -cp out tasks.Task2
java -cp out tasks.Task3
java -cp out tasks.Task4
java -cp out tasks.Task5
java -cp out tasks.Task6
java -cp out tasks.Task11 /path/to/directory TODO
```

Для Task1 можно передать N и M: `java -cp out tasks.Task1 10 200`. Для Task5 задаётся размер массива аргументом, например `java -cp out tasks.Task5 1000000`. Task6 по умолчанию запускает emergency shutdown; передайте `graceful` для graceful shutdown. Task11 принимает путь к папке и regex поиска в содержимом файлов.
