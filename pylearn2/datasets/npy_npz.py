"""Objects for datasets serialized in the NumPy native format (.npy/.npz)."""
import numpy
from theano import config
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix

class NpyDataset(DenseDesignMatrix):
    """A dense dataset based on a single array stored as a .npy file."""
    def __init__(self, file, mmap_mode=None):
        """
        Creates an NpzDataset object.

        Parameters
        ----------
        file : file-like object or str
            A file-like object or string indicating a filename. Passed
            directly to `numpy.load`.
        mmap_mode : str, optional
            Memory mapping options for memory-mapping an array on disk,
            rather than loading it into memory. See the `numpy.load`
            docstring for details.
        """
        loaded = numpy.load(file, mmap_mode)
        assert isinstance(loaded, numpy.ndarray), "single arrays (.npy) only"
        loaded = numpy.cast[config.floatX](loaded)
        if len(loaded.shape) == 2:
            super(NpyDataset, self).__init__(X=loaded)
        else:
            super(NpyDataset, self).__init__(topo_view=loaded)


class NpzDataset(DenseDesignMatrix):
    """A dense dataset based on a single array from a .npz archive."""
    def __init__(self, file, key):
        """
        Creates an NpzDataset object.

        Parameters
        ----------
        file : file-like object or str
            A file-like object or string indicating a filename. Passed
            directly to `numpy.load`.
        key : str
            A string indicating which key name to use to pull out a
            single array from the dictionary-like object.
        """
        loaded = numpy.load(file)
        assert not isinstance(loaded, numpy.ndarray), (
            "zipped groups of arrays (.npz) only"
        )
        assert key in loaded, "%s not found in loaded NPZFile" % key
        if len(loaded[key].shape) == 2:
            super(NpzDataset, self).__init__(X=loaded[key])
        else:
            super(NpzDataset, self).__init__(topo_view=loaded[key])