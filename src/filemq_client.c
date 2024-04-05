/*  =========================================================================
    filemq_client - Very simple client

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
    filemq_client - Very simple client
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
            puts ("filemq_client inbox-dir [options] ...");
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

    fmq_client_t *client;
    int rc;
    zsock_t *msgpipe;
    zpoller_t *poller;

    if (argc < 2) {
        puts ("usage: filemq_client inbox-dir");
        return 0;
    }

    //  Create the client
    client = fmq_client_new ();
    assert (client);

    if (verbose){
        zsys_info ("filemq_client - Very simple client");
        fmq_client_verbose = 1;
    }

    rc = fmq_client_connect (client, "tcp://localhost:5670", 1000);
    assert (rc == 0);

    //  Set the clients storage location
    rc = fmq_client_set_inbox (client, argv [1]);
    assert (rc >= 0);

    //  Subscribe to the server's root
    rc = fmq_client_subscribe (client, "/");
    assert (rc >= 0);

    //  Get a reference to the msgpipe
    msgpipe = fmq_client_msgpipe (client);
    assert (msgpipe);

    //  Setup a poller
    poller = zpoller_new ( (void *) msgpipe, NULL);
    assert (poller);

    while (!zsys_interrupted) {
        void *sock = zpoller_wait (poller, 100);

        if (sock == msgpipe) {
            zmsg_t *msg = zmsg_recv ( (void *) msgpipe);
            zmsg_print (msg);
            zmsg_destroy (&msg);
        }
        else
        if (zpoller_terminated (poller)) {
            puts ("the poller terminated");
            break;
        }
    }

    puts ("interrupted");

    zpoller_destroy (&poller);
    fmq_client_destroy (&client);

    return 0;
}
