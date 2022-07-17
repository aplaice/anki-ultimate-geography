#!/bin/sh

version="${1:-everfresh}"

cd build/ || exit 1
for lang_code in CS DE EN ES FR NB NL PL PT RU SV ZH
do
    zip -r "Ultimate_Geography_${version}_${lang_code}.zip" "Ultimate Geography [${lang_code}]"/
    zip -r "Ultimate_Geography_${version}_${lang_code}_EXTENDED.zip" "Ultimate Geography [${lang_code}] [Extended]"/
done
