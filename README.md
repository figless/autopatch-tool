### Формат конфигурационного файла

#### 1. actions (Основной блок)

##### 1.1 replace_string – Замена строк

- **Назначение**: Выполнение замены указанной строки на другую.
- **Поля**:
    - `target`: путь к файлу или "spec" (указывает на spec-файл).
    - `find`: строка для поиска.
    - `replace`: строка для замены.
    - `count`: количество замен (по умолчанию -1, заменяются все вхождения).

**Пример**:

```yaml
actions:
    - replace_string:
            - target: "spec"
              find: "RHEL"
              replace: "MyCustomLinux"
              count: 1
```

##### 1.2 delete_line – Удаление строк

- **Назначение**: Удаление заданных строк.
- **Поля**:
    - `target`: путь к файлу или "spec".
    - `lines`: список строк для удаления (поддерживается многострочный текст).

**Пример**:

```yaml
    - delete_line:
            - target: "README.md"
              lines:
                - "line1"
                - |
                    hello world
                    additional line
```

##### 1.3 modify_release – Изменение номера релиза

- **Назначение**: Добавление суффикса к номеру релиза.
- **Поля**:
    - `suffix`: строка, добавляемая к релизу.
    - `enabled`: включает или выключает модификацию (по умолчанию true).

**Пример**:

```yaml
    - modify_release:
        - suffix: ".mycustom.1"
          enabled: true
```

##### 1.4 changelog_entry – Добавление записей в changelog

- **Назначение**: Добавление записей в changelog spec-файла.
- **Поля**:
    - `name`: имя автора.
    - `email`: email автора.
    - `line`: строки для добавления в changelog (также используются как коммит-сообщения).

**Пример**:

```yaml
    - changelog_entry:
            - name: "eabdullin"
              email: "eabdullin@almalinux.org"
              line:
                - "Updated branding to MyCustomLinux"
```

##### 1.5 add_files – Добавление файлов

- **Назначение**: Добавление исходных файлов или патчей.
- **Поля**:
    - `type`: тип файла (patch или source).
    - `name`: имя файла.
    - `number`: номер патча/файла или "Latest" (по умолчанию "Latest").

**Пример**:

```yaml
    - add_files:
            - type: "patch"
              name: "my_patch.patch"
              number: "Latest"
```

##### 1.6 delete_files – Удаление файлов

- **Назначение**: Удаление файлов из репозитория.
- **Поля**: список имен файлов для удаления.

**Пример**:

```yaml
    - delete_files:
      - file_name: "file.txt"
```

### Описание блоков конфигурации

#### 1. dependencies (Добавление зависимостей)

**Назначение**:

Добавление зависимостей в BuildRequires или Requires секции spec-файла. Можно добавлять зависимости как для основного пакета, так и для его сабпакетов.

**Поля**:
- `main` – список зависимостей для основного пакета.
- `subpackage_name` – список зависимостей для сабпакетов (имя сабпакета должно совпадать с именем в spec-файле).
- `name` – название зависимости.
- `buildrequires` – true, если зависимость добавляется в BuildRequires; false – в Requires.

**Пример**:

```yaml
- dependencies:
        main:
            - name: "new-dependency1"
              buildrequires: true
            - name: "runtime-dependency"
              buildrequires: false
        subpackage1:
            - name: "subpackage-build-dep"
              buildrequires: true
            - name: "subpackage-runtime-dep"
              buildrequires: false
```

#### 2. apply_patch (Применение патчей)

**Назначение**:

Применение патчей к исходным файлам пакета. Патч применяется с помощью стандартной команды patch.

**Поля**:
- Список патчей – список имен патчей для применения.

**Пример**:

```yaml
- apply_patch:
    - "fix_typo.patch"
    - "bugfix.patch"
```

#### 3. run_custom_scripts (Запуск кастомных скриптов)

**Назначение**:

Выполнение пользовательских скриптов для подготовки пакета перед выполнением других действий (например, обновление метаданных или очистка временных файлов).

**Поля**:
- Список скриптов – имена скриптов для выполнения.

**Пример**:

```yaml
- run_custom_scripts:
    - "./scripts/cleanup.sh"
    - "./scripts/update_metadata.sh --force"
```

### Порядок выполнения действий

1. run_custom_scripts – выполняется первым (если включен).
2. apply_patch – применяется после скриптов.
3. Остальные действия выполняются в порядке описания.

### Предложения по улучшению конфигурации

1. Добавить возможность задавать переменные в конфигурации для использования в нескольких блоках:

```yaml
variables:
    distro_name: "MyCustomLinux"
```

2. Добавить возможность указания пути относительно корня репозитория для всех файлов:

```yaml
- replace_string:
        - target: "./docs/README.md"
```


**Примечание**

Секции apply_patch, run_custom_scripts и dependencies игнорируются
