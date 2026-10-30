from __future__ import annotations

import sam3Toolkit


def testVersionIsSet():
    assert isinstance(sam3Toolkit.__version__, str)
    assert sam3Toolkit.__version__
