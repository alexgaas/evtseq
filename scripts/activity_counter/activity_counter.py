import ctypes
from pathlib import Path


class ActivityCounter:
    """
    Provides key activity in the 24 hours.
    For correct update must get a new event timestamp within previous event timestamp.

    Uses a 24-bit bitset to track which hours in a day had activity.
    Automatically shifts the bitset as time progresses through the day.
    When a day boundary is crossed, the bitset is cleared.
    """

    # Constants
    DAY_DURATION_HOURS = 24
    HOUR_DURATION_SECONDS = 3600
    DAY_DURATION_SECONDS = DAY_DURATION_HOURS * HOUR_DURATION_SECONDS

    def __init__(self):
        self._lib = self._load_library()
        self._counter = self._lib.ac_create()

    @staticmethod
    def _load_library():
        lib_name = "activity_counter_shared"

        # Try to find the library in common locations
        # Path(__file__).parent = /Users/alexgaas/Desktop/projects/evtseq/scripts/activity_counter
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
                lib.ac_create.restype = ctypes.c_void_p
                lib.ac_destroy.argtypes = [ctypes.c_void_p]
                lib.ac_update.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32]
                lib.ac_clear.argtypes = [ctypes.c_void_p]
                lib.ac_get_last_24_hours_activity.argtypes = [ctypes.c_void_p]
                lib.ac_get_last_24_hours_activity.restype = ctypes.c_uint8
                lib.ac_get_latest_consecutive_activity.argtypes = [ctypes.c_void_p]
                lib.ac_get_latest_consecutive_activity.restype = ctypes.c_uint8
                return lib

        raise RuntimeError(
            f"Could not find {lib_name} library. Build the project first with: "
            "cd build && cmake .. && make"
        )

    def update(self, time, last_time):
        """
        Update activity counter with new timestamp.
        time: current timestamp
        last_time: previous timestamp (must be <= time)
        """
        self._lib.ac_update(self._counter, ctypes.c_uint32(time), ctypes.c_uint32(last_time))

    def clear(self):
        """Clear all activity bits"""
        self._lib.ac_clear(self._counter)

    def get_last_24_hours_activity(self):
        """Get the number of hours with activity in the last 24 hours"""
        return self._lib.ac_get_last_24_hours_activity(self._counter)

    def get_latest_consecutive_activity(self):
        """Get the number of consecutive hours with activity ending at current time"""
        return self._lib.ac_get_latest_consecutive_activity(self._counter)

    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, '_lib') and hasattr(self, '_counter'):
            self._lib.ac_destroy(self._counter)

    def __repr__(self):
        return (f"ActivityCounter(last_24h={self.get_last_24_hours_activity()}, "
                f"consecutive={self.get_latest_consecutive_activity()})")
