from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

SO = Path(__file__).parent / "mechiviz" / "_native_lib" / "libwgpu_native.so"


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name != "wheel":
            return

        # fail loudly instead of silently building a wheel without the lib
        if not SO.exists():
            raise FileNotFoundError(f"missing {SO}, copy the manylinux build there first")

        # .so has no Python ABI dependence (loaded via cffi), so py3-none
        build_data["pure_python"] = False
        build_data["tag"] = "py3-none-manylinux_2_28_x86_64"