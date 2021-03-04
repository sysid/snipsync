# snipsync

Syncs your UltiSnips snippets to JetBrain IDE.
You have to choose the correct target directory for user defined snippets. This depends on your IDE
configuration, i.e. when you have setting sync activated this would be: 

https://www.jetbrains.com/help/pycharm/directories-used-by-the-ide-to-store-settings-caches-plugins-and-logs.html#config-directory
https://intellij-support.jetbrains.com/hc/en-us/articles/206544519-Directories-used-by-the-IDE-to-store-settings-caches-plugins-and-logs

If your settings are synchronized through the IDE Settings Sync plugin, these subfolders are located under jba_config in the configuration directory.

- Creates a `user.xml` live template file for intelij IDE form UltiSnip sources.
- Overwrites existing `user.xml`.
- Interprets `${1}/${1:name}` as Tabstop (variable to replace) and `$1` (without brackets) as Mirror.

## Gotchas
- additional xml `tags` do not result in error, but are being overwritten when JetBrain app closes
- Tabstop's cannot be nested
- make sure that Tabstops use always the format: `${1:default}`, curly brackets
- make sure that Mirrors use always the format: `$1`, never `${1}`, no curly brackets

Do not:
`test -z "\$1" && echo "-E- tag required." 1>&2 && exit 1`

Instead do:
`test -z "\${1}" && echo "-E- tag required." 1>&2 && exit 1`