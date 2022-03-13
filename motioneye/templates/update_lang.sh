#!/bin/sh

# Copyright (c) 2022 blackPanther Europe (www.blackpanther.hu)

if [ -n "$(echo $(pwd) | grep '/templates')" ];then
    cd ..
    templates/update_lang.sh $@
    exit
fi

#en_US de_DE es_ES hu_HU
pushd lang >/dev/null
LANG=$(find * -maxdepth 0 -type d)
popd >/dev/null

if [ ! -n "$LANG" ] ;then
    echo "Missing language dirs! Please define languages.."
    echo "Run 'make inithu' for create Hungarian language files OR"
    echo "Create a new directory in 'lang' older with your lang code, ex.: hu_HU for Hungarian"
    echo "Now set to en_US as default to run..."
    sleep 2
    LANG=en_US
fi

jstrans() {
[ ! -f "lang/motioneye.js.pot" ] && echo "Missing lang/motioneye.js.pot" && exit
    xgettext --from-code=UTF-8 --no-wrap -o lang/motioneye.js.pot static/js/*.js
for i in $LANG ;do
if [ -f "lang/$i/LC_MESSAGES/motioneye.js.po " ];then
    msgmerge --no-wrap -N -U lang/$i/LC_MESSAGES/motioneye.js.po lang/motioneye.js.pot
elif [ -f "lang/$i/LC_MESSAGES/messages.po" ];then
    msgmerge lang/$i/LC_MESSAGES/messages.po lang/motioneye.js.pot -o lang/$i/LC_MESSAGES/motioneye.js.po
else
    echo "MISSING TEMPLATE : 
    $PWD/lang/$i/LC_MESSAGES/messages.po"
    exit
fi

./scripts/po2json lang/$i/LC_MESSAGES/motioneye.js.po static/js/motioneye.$(echo $i| awk -F_ '{print $1}').json

done 
}

if [ "$1" = "js" ];then
jstrans
exit
fi

pybabel -v extract -F ./templates/babel.cfg -k _l -o ./templates/motionEye3.pot .

echo
echo "Step 1 done"
sleep 2

for i in $LANG ;do

if [ ! -f "lang/$i/LC_MESSAGES/messages.po" ];then
 pybabel init -l $i -d ./lang -i ./templates/motionEye3.pot
fi

echo
echo "Step 2 done"

#pybabel update -l $i -d ./lang -i ./templates/motionEye3.pot
echo "Already exists -> lang/$i/LC_MESSAGES/messages.po"
msgmerge ./lang/$i/LC_MESSAGES/messages.po ./templates/motionEye3.pot > ./lang/$i/temp-messages.po
mv -f lang/$i/temp-messages.po lang/$i/LC_MESSAGES/messages.po
msgfmt lang/$i/LC_MESSAGES/messages.po -o lang/$i/LC_MESSAGES/messages.mo
echo "Merge done"
echo
echo "Step 3 done"
jstrans
echo "Step 4 done"

done 

exit
#pybabel compile -f -d ./lang


