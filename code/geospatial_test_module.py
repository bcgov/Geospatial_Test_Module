# Author: Kyla Gunn
# Ministry, Division, Branch: WLRS, GeoBC
# Created Date: February 25, 2026
# Updated Date: April 23, 2026
# Description:
#     This script runs a series of automated tests to verify that required
#     geospatial and data science Python libraries are available and functioning
#     correctly in the current environment.
#
#     The script first checks environment configuration and shared library paths,
#     then runs import tests to confirm that key dependencies (such as pandas,
#     geopandas, matplotlib, arcpy, and custom GeoBC modules) can be imported.
#     Additional functionality tests confirm that selected libraries are able to
#     perform basic operations, such as creating dataframes and geodataframes.
#
#     Logging is written to a log file only.Test failures are tracked using a 
#     dictionary that records the test namevand one or more failure reasons. A 
#     summary of any failures is written to the log file at the end of the test 
#     run.
# ------------------------------------------------------------------------------
# Improvements:
#     Additional functionality tests can be added when/if needed.
#
#     Failure tracking could be expanded to include skipped tests or
#     environment-specific warnings if required in the future.
#
#     Logging output could be standardized further.
# ------------------------------------------------------------------------------

# *** IMPORTS ***
# lets python interact with the system (file paths)
import sys
# built-in python testing tool
import unittest

# *** LOGGING ***
import logging
from pathlib import Path

# root directory of this script
script_dir = Path(__file__).parent

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()
logger.propagate = False

file_formatter = logging.Formatter(
    "{asctime} {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler(
    script_dir / f"{Path(__file__).stem}.log",
    mode="a",
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def log(msg: str, level=logging.INFO):
    """make logging easy!"""
    logger.log(level, msg)

def log_section(title: str):
    # blank line before section
    log("", logging.INFO)

    log("=" * 78, logging.INFO)
    log(title, logging.INFO)
    log("=" * 78, logging.INFO)


# *** CONFIGURATION ***
# stores location of shared network folder
GEOBC_LIBRARY_PATH = r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Python\Library"

failure_tracking__dict = {}

# *** IMPORTS AND CONFIGURATION ***
log_section("IMPORTS AND CONFIGURATION")

log("Checking GeoBC library path", logging.DEBUG)
if GEOBC_LIBRARY_PATH not in sys.path:
    sys.path.insert(0, GEOBC_LIBRARY_PATH)
    log("GeoBC library path added to sys.path", logging.DEBUG)
else:
    log("GeoBC library path already present in sys.path", logging.DEBUG)

# *** TEST CLASS 1: IMPORT TESTS ***
# group of tests that see if libraries import
class TestImports(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log_section("TEST CLASS #1 - IMPORT LIBRARIES")
        log("Beginning library import tests", logging.DEBUG)

# tries to import pandas
    def test_import_pandas(self):
        log("Testing import: pandas", logging.DEBUG)
        try:
            __import__("pandas")
            log("pandas imported successfully", logging.DEBUG)
        except ImportError:
            log("Failed to import pandas", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_import_pandas", []
            ).append("Failed to import pandas")
            self.fail("Failed to import pandas")

# tries to import geopandas
    def test_import_geopandas(self):
        log("Testing import: geopandas", logging.DEBUG)
        try:
            __import__("geopandas")
            log("geopandas imported successfully", logging.DEBUG)
        except ImportError:
            log("Failed to import geopandas", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_import_geopandas", []
            ).append("Failed to import geopandas")
            self.fail("Failed to import geopandas")

# tries to import matplotlib
    def test_import_matplotlib(self):
        log("Testing import: matplotlib", logging.DEBUG)
        try:
            __import__("matplotlib")
            log("matplotlib imported successfully", logging.DEBUG)
        except ImportError:
            log("Failed to import matplotlib", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_import_matplotlib", []
            ).append("Failed to import matplotlib")
            self.fail("Failed to import matplotlib")

# tries to import arcpy
    def test_import_arcpy(self):
        log("Testing import: arcpy", logging.DEBUG)
        try:
            __import__("arcpy")
            log("arcpy imported successfully", logging.DEBUG)
        except ImportError:
            log("ArcPy not available in this environment", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_import_arcpy", []
            ).append("ArcPy not available")
            self.fail("ArcPy not available")

# tries to import excelwings (skips for now as it's not installed in my environment)
    @unittest.skip("excelwings not currently installed in this environment")
    def test_import_excelwings(self):
        log("Testing import: excelwings (skipped)", logging.DEBUG)
        __import__("excelwings")

# tries to import custom GeoBC module 
    def test_import_geobc(self):
        log("Testing import: geobc", logging.DEBUG)
        try:
            __import__("geobc")
            log("geobc imported successfully", logging.DEBUG)
        except ImportError:
            log("Failed to import geobc module", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_import_geobc", []
            ).append("Failed to import geobc module")
            self.fail("Failed to import geobc module")

# *** TEST CLASS 2: LIBRARY FUNCTIONS ***
class TestFunctionality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log_section("TEST CLASS #2 - LIBRARY FUNCTIONALITY")
        log("Beginning functionality tests", logging.DEBUG)

# tests that pandas is functional
    def test_pandas_dataframe_creation(self):
        log("Testing pandas DataFrame creation", logging.DEBUG)
        import pandas as pd

        df = pd.DataFrame({"col1": [1, 2, 3]})
        log("Pandas DataFrame created with 3 rows", logging.DEBUG)

        self.assertEqual(len(df), 3)

# tests that geopandas is functional
    def test_geopandas_geodataframe_creation(self):
        log("Testing GeoDataFrame creation with CRS", logging.DEBUG)
        import geopandas as gpd
        from shapely.geometry import Point

        gdf = gpd.GeoDataFrame(
            {"id": [1, 2]},
            geometry=[Point(0, 0), Point(1, 1)],
            crs="EPSG:4326",
        )

        log("GeoDataFrame created successfully with EPSG:4326", logging.DEBUG)

        self.assertEqual(len(gdf), 2)

# tests that geopandas can read from the test file geodatabase
    def test_geopandas_can_read_test_geodatabase(self):
        log("Testing GeoPandas read from test geodatabase", logging.DEBUG)

        import geopandas as gpd

        gdb_path = script_dir.parent / "Test_Geodatabase" / "Test_Geodatabase.gdb"

        try:
            gdf = gpd.read_file(gdb_path, layer="test_points")
            log("Successfully read 'test_points' from test geodatabase", logging.DEBUG)

            self.assertGreater(len(gdf), 0)

        except Exception as e:
            log("Failed to read from test geodatabase", logging.ERROR)
            failure_tracking__dict.setdefault(
                "test_geopandas_can_read_test_geodatabase", []
            ).append(str(e))
            self.fail("Unable to read test geodatabase with GeoPandas")

# *** CONTROL TEST ORDER ***
def load_tests(loader, tests, pattern):
    """Ensure import tests run before functionality tests."""
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestImports))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionality))
    return suite

# *** TEST RUNNER ***
if __name__ == "__main__":
    unittest.main(exit=False)

    log_section("TEST SUMMARY")

    if failure_tracking__dict:
        for test_name, issues in failure_tracking__dict.items():
            log(test_name, logging.INFO)
            for issue in issues:
                log(f"  - {issue}", logging.INFO)
    else:
        log("No test failures detected", logging.INFO)

