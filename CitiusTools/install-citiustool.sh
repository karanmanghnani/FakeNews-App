#!/bin/sh


chmod 0755 nec.sh
chmod 0755 es/*.perl
chmod 0755 pt/*.perl
chmod 0755 en/*.perl
chmod 0755 gl/*.perl

echo "Permissions of execution, done!"

echo "Just for Galician: storing data... you require the module Storable to be installed (CPAN)"
./gl/./store_lex.perl

