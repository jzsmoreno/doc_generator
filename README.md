# doc_generator
 
## Installation

### 1. Install System Dependencies

For Ubuntu/Debian-based systems:

Run the following commands to install the required system libraries:

```bash
sudo apt-get update
sudo apt install pandoc
sudo apt-get install -y libgobject-2.0-0 libpango-1.0-0 libcairo2
```

For macOS:

On macOS, you can use Homebrew to install the necessary libraries:

```bash
brew install gtk+3
brew install pandoc
brew unlink glib && brew link glib
brew install cairo pango gobject-introspection gdk-pixbuf
brew install weasyprint
brew pyenv-sync
```

Check your `LD_LIBRARY_PATH` or `DYLD_LIBRARY_PATH`: If you're on a Linux or macOS system, ensure that the required library paths are included in your system's library search path.

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH  # For Linux
export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH  # For macOS
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH" # For Apple Silicon Macs
```

Manual symlinking, instead of linking each library individually to `/usr/local/lib`, you can link the `/opt/homebrew/lib` contents (as long as you don't have an existing `/usr/local/lib` directory):

```bash
sudo ln -s /opt/homebrew/lib /usr/local/lib
```