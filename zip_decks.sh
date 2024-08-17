#!/bin/sh

version="${1:-everfresh}"

build_paths=""

LANG_CODES=$(head -n 1 src/data/guid.csv | sed 's/country,//' | sed 's/guid://g' | sed 's/guid/en/' | sed 's/,/ /g' | tr '[:lower:]' '[:upper:]')

cd build/ || exit 1
for lang_code in $LANG_CODES
do
    standard_zip="Ultimate_Geography_${version}_${lang_code}.zip"
    extended_zip="Ultimate_Geography_${version}_${lang_code}_EXTENDED.zip"
    zip -r "$standard_zip" "Ultimate Geography [${lang_code}]"/
    zip -r "$extended_zip" "Ultimate Geography [${lang_code}] [Extended]"/
    build_paths="$build_paths build/$standard_zip build/$extended_zip"
done

# Magic cookie for setting value https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#example-setting-a-value
echo '::set-output name=DECK_PATHS::'"${build_paths}"
