import ctypes
from pathlib import Path


class IntervalSet:
    """
    Preserves event sequence ordered in time.
    To save memory, class only stores time diff between neighbor events.
    uint16_t allows diff between two neighbor events, longer events no longer than 18 hours.
    If gap between events more than 18 hours - earlier events are evicted.
    Class supports quadratic sum between events in line behind no longer than 1800 seconds (30 minutes).
    """

    def __init__(self):
        self._lib = self._load_library()
        self._event_set = self._lib.es_create()

    @staticmethod
    def _load_library():
        lib_name = "interval_set_shared"

        # Try to find the library in common locations
        # Path(__file__).parent = /Users/alexgaas/Desktop/projects/evtseq/scripts/interval_set
        # Path(__file__).parent.parent = /Users/alexgaas/Desktop/projects/evtseq/scripts
        # Path(__file__).parent.parent.parent = /Users/alexgaas/Desktop/projects/evtseq
        paths = [
            Path(__file__).parent.parent.parent / "build" / "lib" / f"{lib_name}.dylib",
            Path(__file__).parent.parent.parent / "build" / "lib" / f"lib{lib_name}.dylib",
            Path(__file__).parent.parent.parent / "build" / "lib" / f"{lib_name}.so",
            Path(__file__).parent.parent.parent / "build" / "lib" / f"{lib_name}.dll",
            Path(__file__).parent.parent.parent / "lib" / f"{lib_name}.dylib",
            Path(__file__).parent.parent.parent / "lib" / f"lib{lib_name}.so",
            Path("/usr/local/lib") / f"lib{lib_name}.dylib",
            Path("/usr/local/lib") / f"lib{lib_name}.so",
            Path("/opt/homebrew/lib") / f"lib{lib_name}.dylib",
        ]

        for lib_path in paths:
            if lib_path.exists():
                lib = ctypes.CDLL(str(lib_path))
                # Set return types and argument types for functions
                lib.es_create.restype = ctypes.c_void_p
                lib.es_destroy.argtypes = [ctypes.c_void_p]
                lib.es_insert.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
                lib.es_get_sum_of_lengths.argtypes = [ctypes.c_void_p]
                lib.es_get_sum_of_lengths.restype = ctypes.c_uint32
                lib.es_get_sum_of_squared_lengths.argtypes = [ctypes.c_void_p]
                lib.es_get_sum_of_squared_lengths.restype = ctypes.c_uint32
                lib.es_get_interval_between_events_count.argtypes = [ctypes.c_void_p]
                lib.es_get_interval_between_events_count.restype = ctypes.c_uint32
                return lib

        raise RuntimeError(
            f"Could not find {lib_name} library. Build the project first with: "
            "cd build && cmake .. && make"
        )

    def insert(self, event_time):
        """Insert an event at the specified time"""
        self._lib.es_insert(self._event_set, ctypes.c_uint32(event_time))

    def get_sum_of_lengths(self):
        """Get sum of all time intervals between events (within 30 min threshold)"""
        return self._lib.es_get_sum_of_lengths(self._event_set)

    def get_sum_of_squared_lengths(self):
        """Get sum of squared time intervals between events (within 30 min threshold)"""
        return self._lib.es_get_sum_of_squared_lengths(self._event_set)

    def get_interval_between_events_count(self):
        """Get count of intervals between events (within 30 min threshold)"""
        return self._lib.es_get_interval_between_events_count(self._event_set)

    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, '_lib') and hasattr(self, '_event_set'):
            self._lib.es_destroy(self._event_set)

    def __repr__(self):
        return (f"IntervalSet(sum_lengths={self.get_sum_of_lengths()}, "
                f"sum_squared={self.get_sum_of_squared_lengths()}, "
                f"interval_count={self.get_interval_between_events_count()})")
