#!/bin/sh

# Copyright (c) 2022 blackPanther Europe (www.blackpanther.hu)

if [ -n "$(echo $(pwd) | grep '/templates')" ];then

cd ..
    templates/update_lang.sh
    exit
fi

pybabel -v extract -F ./templates/babel.cfg -k _l -o ./templates/motionEye3.pot .
echo
echo "Step 1 done"
sleep 10

for i in en_US de_DE es_ES hu_HU ;do

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

done 

#pybabel compile -f -d ./lang

