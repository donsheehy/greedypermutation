import unittest
import os
from click.testing import CliRunner
from  greedypermutation.cli import cli

class TestCLI(unittest.TestCase):
    def testgreedy(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            infile = 'pointfile.txt'
            outfile = 'testoutput.txt'
            with open(infile, 'w') as f:
                f.write(POINTS)
            result = runner.invoke(cli, [infile, '--outfile', outfile])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(outfile))
            with open(outfile, 'r') as f:
                for line in f.readlines():
                    self.assertEqual(len(line.split(';')), 2)

    def testgreedy_tostdout(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('pointfile', 'w') as f:
                f.write(POINTS)
            result = runner.invoke(cli, ['pointfile'])
            self.assertEqual(result.exit_code, 0)
            gp = result.output.split('\n')
            self.assertEqual(len(gp[0].split(';')), 2)
            self.assertTrue(';' in gp[0])
            self.assertEqual(gp[0].split(';')[1], 'None')

    def testgreedy_notree(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('pointfile', 'w') as f:
                f.write(POINTS)
            result = runner.invoke(cli, ['pointfile', '--notree'])
            self.assertEqual(result.exit_code, 0)
            gp = result.output.split('\n')
            self.assertTrue(';' not in gp[0])

    def testgreedy_quadratic(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('pointfile', 'w') as f:
                f.write(POINTS)
            result = runner.invoke(cli, ['pointfile', '--notree', '--algorithm', 'quadratic'])
            self.assertEqual(result.exit_code, 0)
            gp = result.output.split('\n')
            self.assertTrue(';' not in gp[0])



POINTS = """\
1 2
100 2
45 3
25 0
"""


if __name__ == '__main__':
    unittest.main()
