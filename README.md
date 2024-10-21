# Ollama save/load models
Save and load ollama models just like operating docker images.

## Usage
```sh
ollama pull gemma2:2b-instruct-q4_K_M
ollama list
# NAME                         ID              SIZE      MODIFIED
# gemma2:2b-instruct-q4_K_M    cb2d06dce813    1.7 GB    30 seconds ago

# save to stdout
export OLLAMA_MODELS="/path/to/ollama/models"  # change this if you have alternative path
./ollama-save.py gemma2:2b-instruct-q4_K_M | gzip > gemma2.tar.gz

# load from filename
./ollama-load.py gemma2.tar.gz
```

## FAQ

### macOS `tar` version
macOS use `BSD-tar` so you may encounter the following error when loading tarball on a linux machine:
```
tar: Ignoring unknown extended header keyword 'LIBARCHIVE.xattr.com.apple.provenance'
```
Use `GNU-tar` to fix this:
```sh
brew install gnu-tar
```
