# Web server «grinx» 🥸

## Задача
> Реализовать упрощенный аналог nginx. Он должен работать оптимально (т.е. без полного разбора входящих пакетов если нет необходимости и т.п.) и не должен залипать на одном запросе (асинхронность, многопоточность, etc).


### Как запустить
`python3 -m grinx localhost 8001`


## Требования
- [x] Асинхронная/многопоточная/etc реализация
- [x] «Ручной» разбор HTTP-запросов
- [ ] Поддержка keep-alive
- [ ] Обслуживание статических запросов + кэш дескрипторов открытых файлов (https://nginx.org/ru/docs/http/ngx_http_core_module.html#open_file_cache)s
- [x] Автоматическая индексация файлов в каталоге
- [x] Логирование запросов
- [x] Виртуальные серверы
- [ ] Конфигурация через файл конфигураций
- [ ] Proxy pass
- [ ] Изменение URI с помощью регулярных выражений, path rewrite

### Пример конфигурации
```
{
    "Servers": [
        {
            "Host": "localhost:8001",
            "Locations": [
                {
                    "Type": "RootFileLocation",
                    "Path": "/foo/",
                    "Root": "/home/"
                }
            ],
            "Middlewares": [
                {
                    "Type": "BasicAuthMiddleware",
                    "Users": [
                        {
                            "User": "admin",
                            "Password": "superhardpassword"
                        }
                    ]
                }
            ]
        }
    ]
}
```

### Доступные Location

- RootFileLocation
  - Path: str
  - Root: str
- AliasFileLocation
  - Path: str
  - Alias: str
- ProxyPassLocation
  - Path: str
  - PassTo: str

### Доступные Middleware
- BasicAuthMiddleware
  - Users[]:
    - User: str
    - Password: str


### Полезные ссылки:
- https://docs.python.org/3.8/library/asyncio-stream.html
- https://docs.python.org/3.8/library/argparse.html
- https://docs.pytest.org/en/6.2.x/goodpractices.html
- https://docs.python.org/3.8/library/configparser.html
- https://datatracker.ietf.org/doc/html/rfc2616
- https://docs.python.org/3.8/library/logging.html

Сурков Денис Дмитриевич, ФИИТ 2 курс 2021