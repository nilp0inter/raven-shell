from __future__ import print_function

import ConfigParser
import argparse
import logging
import os
import sys
from raven.utils.stacks import get_lines_from_file

from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

SYSTEM_CONF = '/etc/raven.conf'
USER_CONF = os.path.expanduser('~/.raven.conf')


def abort(message, retval=1):
    print(message)
    exit(retval)


def raise_():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store", dest="config")
    parser.add_argument("-l", "--logger", action="store", dest="logger",
                        default="shell")

    levels = parser.add_subparsers(dest="level", help="Log level.")

    exception = levels.add_parser("exception")
    critical = levels.add_parser("critical")
    error = levels.add_parser("error")
    warning = levels.add_parser("warning")
    info = levels.add_parser("info")
    debug = levels.add_parser("debug")

    for level in (exception, critical, error, warning, info, debug):
        level.add_argument("project", nargs='?', action="store",
                           default=os.environ.get('SENTRY_PROJECT'))
        level.add_argument("message", nargs=1, action="store")
        level.add_argument("-u", "--user-context", action="append",
                           dest="user_context")
        level.add_argument("-t", "--tag-context", action="append",
                           dest="tags_context")

    args = parser.parse_args()

    # Config
    config = ConfigParser.ConfigParser()
    if args.config is None:
        config.read([USER_CONF, SYSTEM_CONF])
    else:
        config.read([args.config])

    # Project
    if args.project is None:
        abort("SENTRY_PROJECT not set. Aborting.")

    dsn = None
    try:
        dsn = config.get(args.project, 'dsn')
    except:
        dsn = os.environ.get('SENTRY_DSN')
    finally:
        if dsn is None:
            abort("SENTRY_DSN not set. Aborting.")

    client = Client(dsn)
    handler = SentryHandler(client)

    for context_name in ('user_context', 'tags_context'):
        context = getattr(args, context_name)
        client_context_setter = getattr(client, context_name)

        if context:
            for c in context:
                key, value = (None, None)
                try:
                    key, value = c.split('=', 1)
                except:
                    pass
                finally:
                    if None in (key, value):
                        abort("Malformed {} {}".format(context_name, c))
                    client_context_setter({key: value})

    setup_logging(handler)
    logger = logging.getLogger(args.logger)

    source = os.environ.get('BASH_SOURCE')
    lineno = os.environ.get('LINENO')
    print(os.environ)
    print(get_lines_from_file(source, lineno, 3))

    getattr(logger, args.level)(args.message[0], exc_info=False,
            extra=os.environ)
