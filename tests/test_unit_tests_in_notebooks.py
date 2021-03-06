import glob
import subprocess

import pytest


def create_test_cases_from_filenames():
    """Idea is to create test cases based on file names. Convention is
    that the notebook tests start with 'test-' and end in
    '.ipynb'. Furthermore, we have the following structure:

    test-NAME-CORRECTOUTCOME-COMMENT.ipynb where the dashes are separators for:

    - NAME: some more detail on the kind of tests

    - CORRECTOUTCOME: either 'pass' or 'fail'. This is the correct results
      for running nbval on the notebook.

    - COMMENT: can be used to describe the test further.

    Here is an example:

    In [8]: glob.glob('test-*.ipynb')
    Out[8]:
    ['test-latex-fail-randomoutput.ipynb',
     'test-latex-pass-correctouput.ipynb',
     'test-latex-pass-failsbutignoreoutput.ipynb']

    From the filenames, we can create input  data for parametrized tests.

    """
    testdata, testnames = [], []

    ipynb_files = glob.glob("unit/test-*.ipynb")
    for filename in ipynb_files:
        correct_outcome = filename.split('-')[2]
        assert correct_outcome in ['pass', 'fail']
        testnames.append(filename)
        testdata.append((filename, correct_outcome))

    return testnames, testdata


# Create test cases
testnames, testdata = create_test_cases_from_filenames()


@pytest.mark.parametrize("filename, correctoutcome", testdata, ids=testnames)
def test_print(filename, correctoutcome):

    command = "py.test --nbval -v " + filename
    print("Starting parametrized test with filename={}, correctoutcome={}"
          .format(filename, correctoutcome))
    print("Command about to execute is '{}'".format(command))

    exitcode = subprocess.call(command, shell=True)

    if correctoutcome is 'pass':
        assert exitcode is 0
        print("The call of py.test has not reported errors - this is good.")
    elif correctoutcome is 'fail':
        assert exitcode is not 0
        print("The call of py.test has reported errors - " +
              "this is good for this test.")
