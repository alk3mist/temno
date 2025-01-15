# 🔦 Temno

A CLI for [Yasno](https://yasno.com.ua) Outage Scheduling API.

> [!WARNING] 
> 🚧 This is a pet project / sandbox for exploring various dev tools.
> Do not use in production 😎.


## Installation

Install with `uv`:
```shell
uv tool install --from git+https://github.com/alk3mist/temno.git temno
```
or with `pipx`:
```shell
pipx install --python=3.13 "temno @ git+https://github.com/alk3mist/temno.git"
```

You can also run commands without installing:
```shell
uvx --from git+https://github.com/alk3mist/temno.git temno <command>
```

## Usage

### Print help
```console
❯ temno --help
                                                                      
 Usage: temno [OPTIONS] COMMAND [ARGS]...                             
 ...
```

### Find your blackout group
```console
❯ temno cities dnipro 
1 - м. Апостолове
2 - м. Верхівцеве
...

❯ temno streets dnipro --city-id=7
2881 - вул. Сірова
2882 - вул. Січнева
...

❯ temno houses dnipro --street-id=2881     
17 - 3.1
...
```

### Print your weekly schedule
```console
❯ temno schedule weekly dnipro 1.1
MON - 00:00 - 04:00 - POSSIBLE_OUTAGE
...
SUN - 21:00 - 00:00 - POSSIBLE_OUTAGE
```

### Print your daily schedule
```console
❯ temno schedule daily dnipro 5.1 # today by default
08:00 - 09:00 - DEFINITE_OUTAGE
16:00 - 19:30 - DEFINITE_OUTAGE

❯ temno schedule daily dnipro 5.2 tomorrow 
13:00 - 16:30 - DEFINITE_OUTAGE
```

### Export your schedule as an iCalendar
```console
❯ temno schedule weekly dnipro 2.1 --ical group_2_1.ics
Calendar saved to "group_2_1.ics"

❯ temno schedule daily dnipro 2.1 --ical group_2_1.ics
Calendar saved to "group_2_1.ics"
```
