#!/bin/sh

CLONEDIR="${1:-/tmp/mbserver-clone}"
rm -rf sql
[ -z "$1" ] && git clone git://github.com/metabrainz/musicbrainz-server.git "$CLONEDIR"
cp -r "$CLONEDIR/admin/sql" .
[ -z "$1" ] && rm -rf $CLONEDIR
