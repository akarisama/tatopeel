import unittest
import logging
import tatopeel
from tatopeel import FakeFile

logging.basicConfig(level=logging.DEBUG)


class TatoTest(unittest.TestCase):

    # Tests the fake file class used for testing.
    def test_fakefile(self):
        ff1 = FakeFile([])
        ff2 = FakeFile([])

        ff1.write("meow meow!")
        ff2.write("nyan nyan!")

        self.assertEqual(ff1.data, ["meow meow!"])
        self.assertEqual(ff2.data, ["nyan nyan!"])

    # Tests that the ability to convert files to
    def test_conversion(self):
        lang1ff = FakeFile([])
        lang2ff = FakeFile([])

        # Creates a basic fake bases file.
        bases = {
            '1': '0',
            '2': '1'
        }

        # Creates a basic fake set of sentence file lines.
        lines = ['1	eng	Cat', '2	jpn	猫']

        tatopeel.convert(bases, lines, 'eng', 'jpn', lang1ff, lang2ff)

        print(lang1ff.data)
        print(lang2ff.data)

        self.assertEqual(lang1ff.data, ['Cat'])
        self.assertEqual(lang2ff.data, ['猫'])

    def test_file(self):
        # Creates fake 'files' to write sentences to
        lang1ff = FakeFile([])
        lang2ff = FakeFile([])

        # Reads the test base files to a dict
        bases = tatopeel.read_bases('test_bases.csv')

        with open('test_sentences.csv', newline='', encoding="utf-8") as sfile:
            lines = sfile.readlines()

            tatopeel.convert(bases, lines, 'eng', 'jpn', lang1ff, lang2ff)

        self.assertEqual(lang1ff.data, ['Cat'])
        self.assertEqual(lang2ff.data, ['猫'])


if __name__ == '__main__':
    unittest.main()
