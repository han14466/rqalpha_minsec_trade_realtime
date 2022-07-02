import locale
import os
import sys
import numpy as np
import h5py

from rqalpha.utils.i18n import gettext as _


class TickBarStore():
    DEFAULT_DTYPE = np.dtype([
        ('date', np.uint64),
        ('time', np.uint64),
        ('last', np.float),
        ('high', np.float),
        ('low', np.float),
        ('volume', np.float),
        ('open_interest', np.float),
        ('total_turnover', np.float),
        ('a1', np.float),
        ('b1', np.float),
        ('a2', np.float),
        ('b2', np.float),
        ('a3', np.float),
        ('b3', np.float),
        ('a4', np.float),
        ('b4', np.float),
        ('a5', np.float),
        ('b5', np.float),
        ('a1_v', np.float),
        ('b1_v', np.float),
        ('a2_v', np.float),
        ('b2_v', np.float),
        ('a3_v', np.float),
        ('b3_v', np.float),
        ('a4_v', np.float),
        ('b4_v', np.float),
        ('a5_v', np.float),
        ('b5_v', np.float)
    ])

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileExistsError("File {} not exist，please update bundle.".format(path))
        self._h5 = open_h5(path, mode="r")

    def get_ticks(self,date):
        try:
            return self._h5[date][:]
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