# snipsync

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]

Syncs your UltiSnips snippets to JetBrain IDE ([see blog](https://sysid.github.io/snipsync/)).

*snipsync* is based on UltiSnips to parse UltiSnips snippets and transforms them into JetBrains XML *LiveTemplate*
syntax.

## Usage
- JetBrains must not be running during the update because is holds LiveTemplates in memory and saves them to disk at
shutdown. So any external changes to LiveTemplates will be overwritten.
  
```sh
# sync Ultisnip snippets based on static configuration
snipsync auto-sync

# sync Ultisnip snippets based on CLI arguments
snipsync sync -c "Python" "~/dev/binx/vim-config/UltiSnips/python.snippets" "~/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates/user.xml"
```

## Configuration
### Configuration File
- static configuration allows you to set all relevant parameters via config file
- if `init = no` then an existing `user.xml` LiveTemplate file will only be updated and existing LiveTemplates preserved
- if `init = yes` a new `user.xml` LiveTemplate file will be created. This is the right option, if you want to have
  only UltiSnips snippet in your `user.xml`.

Example:
```ini
[DEFAULT]
#live_templates_path = ~/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates
live_templates_path = ~/xxx
ultisnips_path = ~/dev/binx/vim-config/UltiSnips

[GLOBAL]
init = yes

[SNIP.SHELL]
ultisnips = %(ultisnips_path)s/sh.snippets
live_templates = %(live_templates_path)s/user.xml
live_templates_contexts = ["SHELL_SCRIPT", "Bash"]

[SNIP.PYTHON]
ultisnips = %(ultisnips_path)s/python.snippets
live_templates = %(live_templates_path)s/user.xml
live_templates_contexts = ["Python"]
```

### Configuration Location
the configuration file's default location is:
- Mac OS X: `~/Library/Application Support/snipsync`  
- Mac OS X (POSIX): `~/.snipsync`  
- Unix: `~/.config/snipsync`  
- Unix (POSIX): `~/.snipsync`    

Attention: Your configuration paths will change with major JetBrain upgrades

### Target Location of JetBrain *LiveTemplates*
In order to have the generated *LiveTemplate* `user.xml` file available in your JetBrains IDE, 
you need to provide the correct target directory for user defined snippets. This depends on your IDE
configuration, i.e. when you have setting sync activated this would be: 

- https://www.jetbrains.com/help/pycharm/directories-used-by-the-ide-to-store-settings-caches-plugins-and-logs.html#config-directory
- https://intellij-support.jetbrains.com/hc/en-us/articles/206544519-Directories-used-by-the-IDE-to-store-settings-caches-plugins-and-logs

If your settings are synchronized through JetBrains IDE Settings Sync plugin, these subfolders are located under `jba_config` in the configuration directory.


## How does it work?
- Creates/updates a `user.xml` live template file for intelij IDE from UltiSnip sources.
- Overwrites existing `user.xml`.
- Interprets UltiSnips syntax `${1}/${1:name}` as Tabstop (variable to replace) and `$1` (without brackets) as Mirror.

## Limitations
- Bespoke user-implemented Python functionality cannot be translated to *LiveTemplate* format
- Nested Tabstop's are not translated correctly (but are valid Ultisnips syntax)

## Gotchas
- make sure that *Tabstops* use always the format: `${1:default}`, curly brackets
- make sure that *Mirrors* never use curly brackets: `$1` instead of `${1}` (would be interpreted as *Tabstop*)

# Development
- additionally, generated xml `tags` do not result in error, but are being overwritten when JetBrain app closes, so
  there is no way to extend the JetBrains XML format
- for development install package locally with: `pipenv install -e .`
- `lexer.py, text.py, ultisnip.py` are used from Ultisnips directly, so no tests are provided here


## Changelog
- 0.2.0 Check for latest JetBrain software to ensure that latest user.xml will be updated  
- 0.1.0 Increase test coverage, update documentation  
- 0.0.9 Inital release  

...

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/snipsync?color=green
[pypi-url]: https://pypi.org/project/snipsync/
[build-image]: https://github.com/sysid/snipsync/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/sysid/snipsync/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/sysid/snipsync/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/sysid/snipsync
[quality-image]: https://api.codeclimate.com/v1/badges/3130fa0ba3b7993fbf0a/maintainability
[quality-url]: https://codeclimate.com/github/nalgeon/podsearch-py
