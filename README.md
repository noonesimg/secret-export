# Secret export 
Simple python wrapper around ansible-vault

Allows to store secrets like API Tokens in an ansible-vault yaml files and export them in bulk to env variables

## Installation
```bash
# install requirements
pip install -r requirements.txt

# if you want to access it from anywhere
ln -s `pwd`/secrets-export.py /usr/bin/secret-export
```

## Usage
### Edit or create new vault file
requires the `$EDITOR` env variable
```bash
# creates new file if it doesn't exist and encrypts it with ansible-vault
./secret-export.py edit vault_file.yaml
```

### List env variable names
```bash
# only shows names of variables in your vault file
./secret-export.py ls vault_file.yaml
```

### View encrypted file content
```bash
# shows names and values 
./secret-export.py view vault_file.yaml 
```

### Export env variables from your vault file
```bash
# generates the file and copies '. ./export.sh' to clipboard
./secrets-export.py export vault_file.yaml

# exports the variables and removes ./export.sh file
. ./export.sh
```

# Configuration
If you don't want to be prompted for a password every single time. You can store the password in a file and export filepath to the `$ANSIBLE_VAULT_PASSWORD_FILE` env variable

# Note
tested on python 3.10.12 and ansible-vault 2.16.2
