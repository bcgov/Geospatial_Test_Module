# Author: Kyla Gunn
# Ministry, Division, Branch: WLRS, GeoBC
# Created Date: February 25, 2026
# Updated Date: April 23, 2026
# Description:
#     This script runs a series of automated tests to check that required
#     geospatial and data science Python libraries are available and working
#     correctly in the current environment.
#
#     The script first verifies that common dependencies such as pandas,
#     geopandas, matplotlib, arcpy, and custom GeoBC modules can be imported.
#     It then runs a small number of basic functionality tests to confirm that
#     key libraries can create dataframes, geodataframes, and read spatial data
#     where applicable.
#
#     Logging is set up to write detailed output to a log file while keeping
#     terminal output readable. This helps with debugging environment issues
#     and provides a record of test results.
# ------------------------------------------------------------------------------
# Improvements: 
#     Additional functionality tests could be added to better represent
#     real-world workflows (e.g., projections, spatial operations, or writing
#     outputs to disk).
#
#     Hard-coded file paths (e.g., network locations or example data paths)
#     could be moved to a configuration file or environment variables for
#     easier reuse across environments.
#
#     Logging could be expanded to include a summary of passed, failed, and
#     skipped tests at the end of the test run.
# Suggestions...
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

# Setup logger name
logger_name = "Logger.main" if __name__ == "__main__" else f"{__name__}.main"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)  
logger.handlers.clear()         
logger.propagate = False       

# set formatters
file_formatter = logging.Formatter(
    "{asctime} - {name} - {levelname} - {message}",
    style="{"
)
console_formatter = logging.Formatter("{message}", style="{")

# set and add handlers
log_file_path = script_dir / f"{Path(__file__).stem}.log"  # use script name
fileHandler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")  # w = overwrite a = append
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(file_formatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)  # terminal will not print debug
consoleHandler.setFormatter(console_formatter)
logger.addHandler(consoleHandler)

# Reduce verbosity from noisy third-party libraries
logging.getLogger("numexpr").setLevel(logging.WARNING)

def log(msg: str, level: int = logging.INFO):
    """make logging easy!"""
    logger.log(level, msg)


# *** CONFIGURATION ***
# stores location of shared network folder
GEOBC_LIBRARY_PATH = r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Python\Library"

# adding it to python's path
if GEOBC_LIBRARY_PATH not in sys.path:
    sys.path.insert(0, GEOBC_LIBRARY_PATH)
    log(f"Added GeoBC library path to sys.path: {GEOBC_LIBRARY_PATH}", logging.DEBUG)


# *** TEST CLASS 1: IMPORT TESTS ***
# group of tests that see if libraries import - one skipped for now (excelwings)
class TestImports(unittest.TestCase):

# tries to import pandas
    def test_import_pandas(self):
        log("Testing import: pandas", logging.DEBUG)
        try:
            __import__("pandas")
        except ImportError:
            log("Failed to import pandas", logging.ERROR)
            self.fail("Failed to import pandas")

# tries to import geopandas
    def test_import_geopandas(self):
        log("Testing import: geopandas", logging.DEBUG)
        try:
            __import__("geopandas")
        except ImportError:
            log("Failed to import geopandas", logging.ERROR)
            self.fail("Failed to import geopandas")

# tries to import matplotlib
    def test_import_matplotlib(self):
        log("Testing import: matplotlib", logging.DEBUG)
        try:
            __import__("matplotlib")
        except ImportError:
            log("Failed to import matplotlib", logging.ERROR)
            self.fail("Failed to import matplotlib")

# tries to import arcpy
    def test_import_arcpy(self):
        log("Testing import: arcpy", logging.DEBUG)
        try:
            __import__("arcpy")
        except ImportError:
            log("ArcPy not available in this environment", logging.WARNING)
            self.fail("ArcPy not available in this environment")

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
        except ImportError:
            log("Failed to import geobc module", logging.ERROR)
            self.fail("Failed to import geobc module")


# *** TEST CLASS 2: LIBRARY FUNCTIONS ***
# test that libraries actually work - these are examples, and can be expanded later
class TestFunctionality(unittest.TestCase):

# tests that pandas is functional
#   creates a dataframe and checks it has 3 rows 
    def test_pandas_dataframe_creation(self):
        log("Testing pandas DataFrame creation", logging.DEBUG)
        import pandas as pd  # pyright: ignore[reportMissingTypeStubs]

        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
            }
        )

        self.assertEqual(len(df), 3)

# tests that geopandas is functional
#   creates a GDF (geodataframe) with geometry and a CRS (coordinate reference system)
    def test_geopandas_geodataframe_creation(self):
        log("Testing GeoDataFrame creation with CRS", logging.DEBUG)
        import geopandas as gpd
        from shapely.geometry import Point

        gdf = gpd.GeoDataFrame(
        {"id": [1, 2]},
            geometry=[Point(0, 0), Point(1, 1)],
            crs="EPSG:4326",
        )

        self.assertEqual(len(gdf), 2)
        self.assertEqual(str(gdf.crs), "EPSG:4326")


    def test_geopandas_can_read_file_geodatabase(self):
        log("Testing read of file geodatabase", logging.DEBUG)
        import os
        import geopandas as gpd
        import fiona 

        gdb_path = r"W:\path\to\your\data\example.gdb"

        if not os.path.exists(gdb_path):
            log("File geodatabase not available in this environment", logging.WARNING)
            self.skipTest("File geodatabase not available in this environment")

        layers = fiona.listlayers(gdb_path) 
        self.assertGreater(len(layers), 0)

        gdf = gpd.read_file(gdb_path, layer=layers[0])
        self.assertFalse(gdf.empty)
        self.assertIsNotNone(gdf.geometry)


# *** TEST RUNNER ***
# runs all tests once executed
if __name__ == "__main__":
    log("Starting geospatial dependency test suite")
    unittest.main()  # pyright: ignore[reportUnusedCallResult]