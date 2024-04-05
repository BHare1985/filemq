/*  =========================================================================
    filemq_server - Very simple server

    Copyright (c) the Contributors as noted in the AUTHORS file.
    This file is part of FileMQ, a C implemenation of the protocol:
    https://github.com/danriegsecker/filemq2.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
    =========================================================================
*/

/*
@header
    filemq_server - Very simple server
@discuss
@end
*/

#include "filemq_classes.h"

int main (int argc, char *argv [])
{
    bool verbose = false;
    int argn;
    for (argn = 1; argn < argc; argn++) {
        if (streq (argv [argn], "--help")
        ||  streq (argv [argn], "-h")) {
            puts ("filemq_server publish-from [options] ...");
            puts ("  --verbose / -v         verbose test output");
            puts ("  --help / -h            this information");
            return 0;
        }
        else
        if (streq (argv [argn], "--verbose")
        ||  streq (argv [argn], "-v"))
            verbose = true;
        else {
            printf ("Unknown option: %s\n", argv [argn]);
            return 1;
        }
    }

    zactor_t *server;
    server = zactor_new (fmq_server, "filemq_server");

    if (verbose){
        zsys_info ("filemq_server - Very simple server");
        zstr_send (server, "VERBOSE");
    }

    zstr_sendx (server, "PUBLISH", argv [1], "/", NULL);
    zstr_sendx (server, "BIND", "tcp://*:5670", NULL);

    while (!zsys_interrupted)
        zclock_sleep (1000);

    puts ("interrupted");

    zactor_destroy (&server);

    return 0;
}
