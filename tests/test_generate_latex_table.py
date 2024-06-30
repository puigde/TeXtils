import unittest
import os
from textils.tables import generateLatexTable  # Adjust the import according to your project structure

class TestGenerateLatexTableSimpleOutput(unittest.TestCase):

    def setUp(self):
        self.numericRowValuesList = [
            [1.2345, 2.3456, 3.4567],
            [4.5678, 5.6789, 6.7890]
        ]
        self.header = ['Column1', 'Column2', 'Column3']
        self.strRowValuesList = [['Row1', 'A'], ['Row2', 'B']]
        self.outputPath = './tests/test_output.tex'
        self.caption = "This is a sample _caption_"
        self.label = "sample_label"
        self.expectedOutputPath = './tests/expected_output.tex'
        
        if os.path.exists(self.outputPath):
            os.remove(self.outputPath)

    def tearDown(self):
        if os.path.exists(self.outputPath):
            os.remove(self.outputPath)

    def test_output_matches_expected(self):
        generateLatexTable(
            numericRowValuesList=self.numericRowValuesList,
            header=self.header,
            outputPath=self.outputPath,
            strRowValuesList=self.strRowValuesList,
            caption=self.caption,
            label=self.label
        )
        
        with open(self.outputPath, 'r') as generated_file:
            generated_content = generated_file.read()
            
        with open(self.expectedOutputPath, 'r') as expected_file:
            expected_content = expected_file.read()
        self.maxDiff = None
        self.assertEqual(generated_content.strip(), expected_content.strip(), "The generated LaTeX file does not match the expected output.")

if __name__ == '__main__':
    unittest.main()
