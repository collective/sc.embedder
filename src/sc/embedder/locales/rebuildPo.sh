#!/bin/sh

i18ndude rebuild-pot --pot sc.embedder.pot --create sc.embedder ..
i18ndude merge --pot sc.embedder.pot --merge manual.pot
i18ndude sync --pot sc.embedder.pot ./*/LC_MESSAGES/sc.embedder.po

i18ndude rebuild-pot --pot tinymce.pot --create tinymce ../skins
i18ndude sync --pot tinymce.pot ./*/LC_MESSAGES/tinymce.po

# Compile po files
for lang in $(find ./ -mindepth 1 -maxdepth 1 -type d); do
    if test -d $lang/LC_MESSAGES; then
        msgfmt -o $lang/LC_MESSAGES/sc.embedder.mo $lang/LC_MESSAGES/sc.embedder.po
        msgfmt -o $lang/LC_MESSAGES/tinymce.mo $lang/LC_MESSAGES/tinymce.po
    fi
done
