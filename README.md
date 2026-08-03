# Py Download Tool

A fast and simple command-line tool for downloading files from direct URLs with a progress bar.

## Features

- Download any direct file URL
- Streaming downloads (low memory usage)
- Progress bar with download speed
- Automatic filename detection
- Prevents accidental file overwrites
- Custom output filename or directory
- Adjustable chunk size

---

## Installation

### Using pip

```bash
pip install py-download-tool
```

---

## Usage

Download a file:

```bash
download https://example.com/file.zip
```

Save with a custom name:

```bash
download https://example.com/file.zip -o myfile.zip
```

Save into a directory:

```bash
download https://example.com/file.zip -o Downloads/
```

Overwrite an existing file:

```bash
download https://example.com/file.zip --overwrite
```

Custom chunk size:

```bash
download https://example.com/file.zip --chunk-size 65536
```

---

## Command

```text
download URL [OPTIONS]
```

### Options

| Option | Description |
|---------|-------------|
| `-o`, `--output` | Output filename or directory |
| `--overwrite` | Replace an existing file |
| `--chunk-size` | Number of bytes downloaded per chunk |
| `-h`, `--help` | Show help message |

---

## Requirements

- Python 3.9 or newer

---

## Dependencies

- requests
- tqdm

---

## License

MIT License