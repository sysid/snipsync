#!/usr/bin/env bash
################################################################################
# sync_to_intelij.sh
################################################################################
set +ex
source ~/dev/binx/profile/sane_bash.sh

TWBASH_DEBUG=true
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
START_TIME=$SECONDS

pushd() {
  # shellcheck disable=SC2164
  command pushd "$@" >/dev/null
}

popd() {
  # shellcheck disable=SC2164
  command popd >/dev/null
}


PROJ_DIR="/Users/Q187392/dev/py/snipsync"
#TEMPLATES="/Users/Q187392/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates"
TEMPLATES="/Users/Q187392/Library/Application Support/JetBrains/WebStorm2020.3/jba_config/templates"
ULTISNIPS="/Users/Q187392/dev/binx/vim-config/UltiSnips"

PYTHON="/Users/Q187392/.local/share/virtualenvs/snipsync-AQxb-dHp/bin/python"
FORCE="-s"
#VERBOSE="-v"

pgrep -lf webstorm > /dev/null
if [ $? -eq 0 ]; then
    echo "-E- Webstorm is running. Stop first."
    exit 1
fi


pushd "$PROJ_DIR" || exit 1

init () {
    Green "-M- Initializing from backup. FIX THIS!"
    cp -v "/Users/Q187392/dev/binx/intelij/user.xml_20210228_205741" "$TEMPLATES/user.xml"
}

execute () {
    echo "$1"
    eval "$1"
}

################################################################################
echo "-M- Start $(date)"

#init

cmd="$PYTHON snipsync/main.py -c "Bash" -c "SHELL_SCRIPT" $VERBOSE $FORCE "$ULTISNIPS/sh.snippets" "\'$TEMPLATES/user.xml\'""
execute "$cmd"

#cmd="$PYTHON snipsync/main.py -c "Python" $VERBOSE $FORCE  "$ULTISNIPS/python.snippets" "\'$TEMPLATES/user.xml\'""
#execute "$cmd"
#
#cmd="$PYTHON snipsync/main.py -c "SQL" $VERBOSE $FORCE  "$ULTISNIPS/sql.snippets" "\'$TEMPLATES/user.xml\'""
#execute "$cmd"

popd || exit 1

echo "-M- End: $(($SECONDS - $START_TIME))"
exit 0
