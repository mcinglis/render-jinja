
# Copyright 2015  Malcolm Inglis <http://minglis.id.au>
#
# render-jinja is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# render-jinja is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with render-jinja. If not, see <https://gnu.org/licenses/>.


from __future__ import print_function
import os
from argparse import ArgumentParser, ArgumentTypeError

import jinja2


class TemplateLoader(jinja2.BaseLoader):
    def get_source(self, environment, template_path):
        filename = os.path.join(os.getcwd(), template_path)
        mtime = os.path.getmtime(filename)
        def uptodate():
            return os.path.getmtime(filename) == mtime
        contents = read_file(template_path)
        return contents, filename, uptodate


def read_file(path):
    with open(path, 'r') as f:
        return f.read().decode()


def arg_parser(prog):
    p = ArgumentParser(prog=prog, description='Renders a Jinja template.')
    p.add_argument('path', type=str,
                   help='path to the template file')
    p.add_argument('attrs', nargs='*', type=parse_attr, metavar='k=v',
                   help='attributes to render the template with')
    p.add_argument('-o', '--output', type=str, default='/dev/stdout',
                   help='the path to write the rendered template to')
    return p


def parse_args(argv):
    p = arg_parser(argv[0])
    args = p.parse_args(argv[1:])
    args.attrs = dict(args.attrs)
    return args


def parse_attr(s):
    if '=' not in s:
        raise ArgumentTypeError('`%s` doesn\'t contain a `=`' % s)
    else:
        return tuple(s.split('=', 1))


def main(argv):
    args = parse_args(argv)
    env = jinja2.Environment(loader=TemplateLoader(),
                             undefined=jinja2.StrictUndefined)
    env.get_template(args.path)\
       .stream(argv=argv, **args.attrs)\
       .dump(args.output)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


