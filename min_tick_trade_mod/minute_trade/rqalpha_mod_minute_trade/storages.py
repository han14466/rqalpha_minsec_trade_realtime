import locale
import os
import sys
import numpy as np
import h5py

from rqalpha.utils.i18n import gettext as _


class MinuteBarStore():
    DEFAULT_DTYPE = np.dtype([
        ('datetime', np.uint64),
        ('open', np.float),
        ('close', np.float),
        ('high', np.float),
        ('low', np.float),
        ('volume', np.float),
        ('total_turnover', np.float),
    ])

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileExistsError("File {} not exist，please update bundle.".format(path))
        self._h5 = open_h5(path, mode="r")

    def get_bars(self):
        try:
            return self._h5['data'][:]
        except KeyError:
            return np.empty(0, dtype=self.DEFAULT_DTYPE)


def open_h5(path, *args, **kwargs):
    # why do this? non-ascii path in windows!!
    if sys.platform == "win32":
        try:
            l = locale.getlocale(locale.LC_ALL)[1]
        except TypeError:
            l = None
        if l and l.lower() == "utf-8":
            path = path.encode("utf-8")
    try:
        return h5py.File(path, *args, **kwargs)
    except OSError as e:
        raise RuntimeError(_(
            "open data bundle failed, you can remove {} and try to regenerate bundle: {}"
        ).format(path, e))