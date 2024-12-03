**Запуск приложения из корневой директории проекта**
1. Соберите Docker-образ:

`docker build -t megaplan-update-parent-deal .`

2. Запустите Docker-контейнер:

_для linux:_
`docker run -d --name megaplan-container --restart=always -v $(pwd)/logs:/app/logs -p 8000:8000 megaplan-update-parent-deal`

_для windows:_
`docker run -d --name megaplan-container --restart=always -v ${PWD}/logs:/app/logs -p 8000:8000 megaplan-update-parent-deal`

**_Если нужно удалить контейнер для перезапуска кода:_**
`docker rm -f megaplan-container`