#!/usr/bin/env python3

import re, codecs
import argparse


LINE = re.compile(r"^{(?P<start>\d+)}{(?P<stop>\d+)}(?P<text>.*)")
TPL = """%d
%s --> %s
%s
"""


def get_time(frame, fps):
    hour = 0
    minute = 0
    second = 0
    milisecond = 0

    val = frame/fps

    if val > 3600:
        hour = int(val/3600)
        val = val - (hour * 3600)

    if val > 60:
        minute = int(val/60)
        val = val - (minute * 60)

    if val > 0:
        second = int(val)
        milisecond = (val - second) * 1000

    return "%02d:%02d:%02d,%03.3d" % (hour, minute, second, milisecond)

def get_line(lno, line, fps):
    start, stop, text = LINE.match(line).groups()
    start = get_time(int(start), fps)
    stop = get_time(int(stop), fps)
    return TPL % (lno, start, stop, "\n".join(text.split('|')))


def main():
    parser = argparse.ArgumentParser(
        description='Convert MicroDVD subtitles '
        'to SRT')
    parser.add_argument(
        '-f', '--fps', dest = 'fps', help='Frames per second. The '
        'destination movie file FPS. Default 25 frames per '
        'second.', default=25, type=float)
    parser.add_argument('-F', '--filename', dest = 'filename', type = str, required = True,
                        help='Subtitle in MicroDVD format.')
    parser.add_argument('-e', '--encoding', dest = 'encoding', default = 'utf-8',
                        help = 'Encoding to use on the MicroDVD file. Default is utf-8.' )
    args = parser.parse_args( )
    encoding = args.encoding.strip( )
    #
    for index, line in enumerate( open( args.filename, 'rb').readlines( ), 1 ):
        #print( index, line )
        print(get_line(index, codecs.decode(line, encoding = encoding), float(args.fps)))

if __name__=='__main__':
    main( )
