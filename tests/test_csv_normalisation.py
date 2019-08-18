#!/usr/bin/env python3

import csv
import io
import unittest
import difflib

class TestCSVNormalisation(unittest.TestCase):

  maxDiff = None

  def csv_normalisation(self, csv_file, quoting='space_and_comma'):

    if quoting == 'space_and_comma':
      # '\n ' so that spaces are also quoted
      lineterminator = '\n '
      # we need to strip the space, since we've asked for it to
      # be added as part of the line terminator
      strip_space = True
      quoting = csv.QUOTE_MINIMAL
    elif quoting == 'minimal':
      lineterminator = '\n'
      strip_space = False
      quoting = csv.QUOTE_MINIMAL
    elif quoting == "always":
      lineterminator = '\n'
      strip_space = False
      quoting = csv.QUOTE_ALL

    data = []

    original_csv_text = ''
    final_csv_text = ''

    with open(csv_file, 'r', newline='') as data_csv:
      original_csv_text = data_csv.read()
      # re-read to get CSV data
      data_csv.seek(0)
      csv_reader = csv.reader(data_csv)
      for row in csv_reader:
        data.append(row)

    with io.StringIO() as final_csv_buffer:
      temp_buffer = io.StringIO()
      csv_writer = csv.writer(temp_buffer,
                              lineterminator=lineterminator,
                              quoting=quoting)
      for row in data:
        csv_writer.writerow(row)
        if strip_space:
          # we won't lose data, since any spaces in a field will
          # be enclosed in quotes
          row_string = temp_buffer.getvalue().strip(' ')
        else:
          row_string = temp_buffer.getvalue()
        final_csv_buffer.write(row_string)
        temp_buffer.seek(0)
        temp_buffer.truncate()
        final_csv_text = final_csv_buffer.getvalue()

    # for i in range(0, len(original_csv_text.split('\n'))):
    #   with self.subTest(line=i):
    #     self.assertEqual(original_csv_text.split('\n')[i],
    #                      final_csv_text.split('\n')[i])
    try:
      self.assertMultiLineEqual(final_csv_text, original_csv_text)
    except:
      unified_diff = difflib.unified_diff(original_csv_text.split('\n'),
                                          final_csv_text.split('\n'),
                                          fromfile=('a/' + csv_file),
                                          tofile=('b/' + csv_file),
                                          n=0,
                                          lineterm='')
      raise self.failureException('\n' + '\n'.join(unified_diff))

  def test_data_csv_normalisation(self):
    self.csv_normalisation('src/data.csv', quoting='space_and_comma')

  # def test_sources_csv_normalisation(self):
  #     self.csv_normalisation('src/data.csv')

if __name__ == '__main__':
  unittest.main()
