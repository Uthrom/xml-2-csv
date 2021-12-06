#!/usr/bin/env python3
'''\
  Tool for converting XML files to CSV

'''
__version__ = "0.0.3"

import sys
from xml.etree import ElementTree
from argparse import ArgumentParser

class MyParser(ArgumentParser):
  def error(self, message):
    sys.stderr.write('error: %s\n' % message)
    self.print_help()
    sys.exit(2)

if __name__ == "__main__":
  parser = MyParser(description=__doc__)
  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s ' + __version__)
  parser.add_argument('-d', '--delim', default=',', 
		      dest='DELIM', help='Set delimiter (default ",")')
  parser.add_argument('-i', '--input', nargs='+', dest="INFILES",
                      help='<Required> input file(s)', required=True)
  parser.add_argument('-o', '--output', dest="OUTFILE", help='<Required> output file', required=True)
  parser.add_argument('-a', '--append', dest='APPEND', action='store_true', default=False, help="Append to file instead of overwriting")
  args = parser.parse_args()
  #print(args)

  f_status = "w"

  if args:
    if args.APPEND:
      f_status = "a"
  else:
    sys.stderr.write("ARGS is None for some reason.\n")

  try:
    with open(args.OUTFILE, f_status) as out_f:
      for in_f in args.INFILES:
        tree = ElementTree.parse(in_f)
        root = tree.getroot()

        conv_id = ""
        medium = ""
        donated = ""
        msg_id = ""
        part_id = ""
        time_s = ""
        body_s = ""

        conv_id = root.attrib['id']
        medium = root.attrib['medium']
        donated = root.attrib['donated']

        for messages in root:
          for message in messages:
            msg_id = message.attrib['id']
            part_id = message.attrib['participant']
            time_s = message.attrib['time']
            for body in message:
              body_s = body.text

            out_f.write(args.DELIM.join(item or '' for item in [conv_id, medium,donated, msg_id, part_id, time_s,body_s]) + "\n")

#            out_f.write('{},{},{},{},{},{},{}\n'.format(conv_id, medium,
#                                                donated, msg_id, part_id, time_s, body_s))
	      
      out_f.close()
      sys.exit(0)

  except IOError as e:
    sys.stderr.write("Failed to save %s: %d - %s", args.OUTFILE, e.errno, e.strerror)
    sys.exit(1)


