#!/usr/bin/python

import sys
import urllib
import urllib2
from lxml import etree

__oracle_address = "http://www.lintukoto.net/viihde/oraakkeli/index.php"

def ask_from_oracle(question):
  form_values = {
    "kysymys_69141524":question,
    "rnd":"69141524" }

  data = urllib.urlencode(form_values)
  req = urllib2.Request(__oracle_address, data)
  response = urllib2.urlopen(req)

  parsed = etree.HTML(response.read())
  return parsed.xpath("//p[contains(@class, 'vastaus')]/text()")[0]

def main(argv):
  print ask_from_oracle("toimiiko?")

if __name__ == "__main__":
  main(sys.argv[1:])
