import ctypes
from pathlib import Path


class ProbabilisticCounter:
    def __init__(self):
        self._lib = self._load_library()
        self._counter = self._lib.pc_create()

    @staticmethod
    def _load_library():
        lib_name = "prob_counter_shared"

        # Try to find the library in common locations
        # Path(__file__).parent = /Users/alexgaas/Desktop/projects/evtseq/scripts/prob_counter
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
                lib.pc_create.restype = ctypes.c_void_p
                lib.pc_destroy.argtypes = [ctypes.c_void_p]
                lib.pc_increment.argtypes = [ctypes.c_void_p]
                lib.pc_get_value.argtypes = [ctypes.c_void_p]
                lib.pc_get_value.restype = ctypes.c_uint32
                lib.pc_get_max_value.restype = ctypes.c_uint32
                return lib

        raise RuntimeError(
            f"Could not find {lib_name} library. Build the project first with: "
            "cd build && cmake .. && make"
        )

    def increment(self):
        """Increment the counter with probabilistic logic based on current value"""
        self._lib.pc_increment(self._counter)

    def get_value(self):
        """Get the estimated count value"""
        return self._lib.pc_get_value(self._counter)

    @staticmethod
    def get_max_value():
        """Get the maximum value the counter can represent"""
        return 2684305408

    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, '_lib') and hasattr(self, '_counter'):
            self._lib.pc_destroy(self._counter)

    def __repr__(self):
        return f"ProbabilisticCounter(value={self.get_value()})"
