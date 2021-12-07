# Web server «grinx» 🥸

## Задача
> Реализовать упрощенный аналог nginx. Он должен работать оптимально (т.е. без полного разбора входящих пакетов если нет необходимости и т.п.) и не должен залипать на одном запросе (асинхронность, многопоточность, etc).


### Как запустить
`python3 -m grinx /path/to/config.json`


## Требования
- [x] Асинхронная/многопоточная/etc реализация
- [x] «Ручной» разбор HTTP-запросов
- [x] Поддержка keep-alive
- [ ] Обслуживание статических запросов + кэш дескрипторов открытых файлов (https://nginx.org/ru/docs/http/ngx_http_core_module.html#open_file_cache)
- [x] Автоматическая индексация файлов в каталоге
- [x] Логирование запросов
- [x] Виртуальные серверы
- [x] Конфигурация через файл конфигураций
- [x] Proxy pass
- [x] Изменение URI с помощью регулярных выражений, path rewrite

### Пример конфигурации
```
{
  "Host": "localhost", # by default
  "Port": "8000", # by default
  "Servers": [
    {
      "Host": "localhost:8001",
      "Locations": [
        {
          "Type": "RootFileLocation",
          "Path": "/foo/",
          "Root": "/Users/denissurkov/University/Python2021autumn/web_server"
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
        },
        {
          "Type": "PathRewriteMiddleware",
          "Rules": [
            {
              "From": "/foo/",
              "To": "/bar/",
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
- PathRewriteMiddleware
  - Rules:[]:
    - From: str (regex)
    - To: str


### Полезные ссылки:
- https://docs.python.org/3.8/library/asyncio-stream.html
- https://docs.python.org/3.8/library/argparse.html
- https://docs.pytest.org/en/6.2.x/goodpractices.html
- https://docs.python.org/3.8/library/configparser.html
- https://datatracker.ietf.org/doc/html/rfc2616
- https://docs.python.org/3.8/library/logging.html

Сурков Денис Дмитриевич, ФИИТ 2 курс 2021