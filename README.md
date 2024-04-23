Interference SAR analysis by Tellus
=======

# Requirements

# Development

- [pyenv](https://github.com/pyenv/pyenv)
- [localstack](https://github.com/localstack/localstack)

### Install [pyenv](https://github.com/pyenv/pyenv)

```bash
$ brew install pyenv
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
$ exec $SHELL -l
```

```bash
$ pyenv install 3.10.14
$ pyenv local 3.10.14
$ python --version
Python 3.10.14
```

### Make of virtual environment and dependent libraries

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install pipenv
$ pipenv install
```

## Development environment

### Activate of virtual environment

- Activate

```bash
$ source .venv/bin/activate
```

- Deactivate

```bash
$ deactivate
```

# Running

## Setting environment variables

```bash
$ export TELLUS_API_ACCESS_TOKEN="<YOUR Tellus API ACCESS TOKEN>"
```

## 1. Find coherent pairs

```bash
$ python src/process_1.py
```

## 2. Output intensity and phase images

TBD

## 3. Image alignment and interference processing

TBD

## 4. Remove track stripes and extract terrain change information

TBD

# Reference

- https://sorabatake.jp/12465/
- https://sorabatake.jp/18669/
- https://qiita.com/mountrock/items/2cf79dc803e70a9de39c
