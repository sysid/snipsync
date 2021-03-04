# snipsync

## Gotchas
- additional xml `tags` do not result in error, but are being overwritten when JetBrain app closes
- Tabstop's can be nested

## Caveats
- make sure that Tabstops use always the format: `${1:default}`, curly brackets
- make sure that Mirrors use always the format: `$1`, never `${1}`, no curly brackets

Do not:
`test -z "\$1" && echo "-E- tag required." 1>&2 && exit 1`

Do:
`test -z "\${1}" && echo "-E- tag required." 1>&2 && exit 1`


## Scratch
re.findall('\\${\\d+[:}].*?}', x)