#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/lxyu/kindle-clippings

import collections
import msgpack
import os

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.msgpack"
OUTPUT_DIR = u"output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def get_sections(filename):
    with open(filename, 'r') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]

    
    location_line = lines[1]

    ## handle "Your Highlight Location 39-39"
    ## and "Your Highlight on Page 193 | Location 2950-2950 | Added o"
    
    if "page" in location_line.lower():
        lowcase = location_line.lower()
        pagenum_start = lowcase.rfind('page') + 4
        
        pagenum_end = location_line.rfind('-')
        position = location_line[pagenum_start:pagenum_end]
        if '|' in position:
            position = position[:position.rfind('|')-1]
        
    else:
        position = location_line[29:location_line.rfind('-')]
    
    if not position:
        return

    try:
        clip['position'] = int(position)
    except:
        import ipdb; ipdb.set_trace()
        
    clip['content'] = lines[2]

    return clip

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    value = value[:100]
    return value

def export_txt(clips):
    """
    Export each book's clips to single text.
    """
    for book in clips:
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos].encode('utf-8'))

        filename = os.path.join(OUTPUT_DIR, u"%s.txt" % slugify(book))
        with open(filename, 'w') as f:
            f.write("\n\n--\n\n".join(lines))


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'r') as f:
            return msgpack.unpack(f, encoding='utf-8')
    except IOError:
        return {}


def save_clips(clips):
    """
    Save new clips to DATA_FILE
    """
    with open(DATA_FILE, 'wb') as f:
        f.write(msgpack.packb(clips, encoding='utf-8'))


def read_clippings(from_file):
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    # extract clips
    sections = get_sections(from_file)
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][clip['position']] = clip['content']

    # remove key with empty value
    clips = {k: v for k, v in clips.iteritems() if v}
    
    # save/export clips
    save_clips(clips)
    export_txt(clips)
    
    return clips

def main():
    read_clippings(u'My Clippings.txt')
    
    # save/export clips
    save_clips(clips)
    export_txt(clips)


if __name__ == '__main__':
    main()
