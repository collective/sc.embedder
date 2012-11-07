#! /bin/sh
LOCAL=`dirname $0`

I18NDOMAIN="sc.embedder"
I18NDUDE="$LOCAL/bin/i18ndude"
BASE_DIRECTORY="src/sc/embedder"

# Synchronise the templates and scripts with the .pot.
$I18NDUDE rebuild-pot --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot \
    --merge ${BASE_DIRECTORY}/locales/manual.pot \
    --create ${I18NDOMAIN} \
    ${BASE_DIRECTORY}

# Synchronise the resulting .pot with all .po files
for po in ${BASE_DIRECTORY}/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
$I18NDUDE sync --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot $po
done

# Synchronise the templates and scripts with the .pot.
$I18NDUDE rebuild-pot --pot ${BASE_DIRECTORY}/locales/plone.pot \
    --create plone \
    ${BASE_DIRECTORY}/configure.zcml \
    ${BASE_DIRECTORY}/profiles/default/workflows

# Synchronise the Plone's pot file (Used for the workflows)
for po in ${BASE_DIRECTORY}/locales/*/LC_MESSAGES/plone.po; do
$I18NDUDE sync --pot ${BASE_DIRECTORY}/locales/plone.pot $po
done

# Report of errors and suspect untranslated messages
$I18NDUDE find-untranslated -n ${BASE_DIRECTORY}