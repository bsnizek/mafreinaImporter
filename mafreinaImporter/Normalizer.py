# -*- coding: UTF-8 -*-
'''
Created on Jun 27, 2012

@author: bsnizek
'''

import string
from unicodedata import normalize, decomposition

class Normalizer():
    
    whitespace = ''.join([c for c in string.whitespace if ord(c) < 128])
    allowed = string.ascii_letters + string.digits + string.punctuation + whitespace

    CHAR = {}
    NULLMAP = ['' * 0x100]
    UNIDECODE_LIMIT = 0x0530
    
    mapping = {
    196 : 'AE', 198 : 'AE', 214 : 'OE', 220 : 'UE', 223 : 'ss', 224 : 'a',
    228 : 'ae', 230 : 'ae', 246 : 'oe', 252 : 'ue'
    }
    
    def mapUnicode(self, text, mapping=()):
        """
        This method is used for replacement of special characters found in a
        mapping before baseNormalize is applied.
        """
        res = u''
        for ch in text:
            ordinal = ord(ch)
            if ordinal in mapping:
                # try to apply custom mappings
                res += mapping.get(ordinal)
            else:
                # else leave untouched
                res += ch
        # always apply base normalization
        return self.baseNormalize(res)

    def baseNormalize(self, text):
        """
        This method is used for normalization of unicode characters to the base ASCII
        letters. Output is ASCII encoded string (or char) with only ASCII letters,
        digits, punctuation and whitespace characters. Case is preserved.
    
          >>> baseNormalize(123)
          '123'
    
          >>> baseNormalize(u'a\u0fff')
          'afff'
    
          >>> baseNormalize(u"foo\N{LATIN CAPITAL LETTER I WITH CARON}")
          'fooI'
    
          >>> baseNormalize(u"\u5317\u4EB0")
          '53174eb0'
        """
        if not isinstance(text, basestring):
            # This most surely ends up in something the user does not expect
            # to see. But at least it does not break.
            return repr(text)
    
        text = text.strip()
    
        res = []
        for ch in text:
            if ch in self.allowed:
                # ASCII chars, digits etc. stay untouched
                res.append(ch)
            else:
                ordinal = ord(ch)
                if ordinal < self.UNIDECODE_LIMIT:
                    h = ordinal >> 8
                    l = ordinal & 0xff
    
                    c = self.CHAR.get(h, None)
    
                    if c == None:
                        try:
                            mod = __import__('unidecode.x%02x'%(h), [], [], ['data'])
                        except ImportError:
                            self.CHAR[h] = self.NULLMAP
                            res.append('')
                            continue
    
                        self.CHAR[h] = mod.data
    
                        try:
                            res.append( mod.data[l] )
                        except IndexError:
                            res.append('')
                    else:
                        try:
                            res.append( c[l] )
                        except IndexError:
                            res.append('')
    
                elif decomposition(ch):
                    normalized = normalize('NFKD', ch).strip()
                    # string may contain non-letter chars too. Remove them
                    # string may result to more than one char
                    res.append(''.join([c for c in normalized if c in self.allowed]))
    
                else:
                    # hex string instead of unknown char
                    res.append("%x" % ordinal)
    
        return ''.join(res).encode('ascii')
        
    
    def normalize(self, s):
        return self.mapUnicode(s, mapping=self.mapping)


if __name__ == '__main__':
    n = Normalizer()
    print(n.normalize(u"ä"))
    