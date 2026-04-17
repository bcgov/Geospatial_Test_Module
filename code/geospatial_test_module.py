
# *** IMPORTS ***
# lets python interact with the system (file paths)
import sys
# built-in python testing tool
import unittest


# *** CONFIGURATION ***
# stores location of shared network folder
GEOBC_LIBRARY_PATH = r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Python\Library"

# adding it to python's path
if GEOBC_LIBRARY_PATH not in sys.path:
    sys.path.insert(0, GEOBC_LIBRARY_PATH)


# *** TEST CLASS 1: IMPORT TESTS ***
# group of tests that see if libraries import - one skipped for now (excelwings)
class TestImports(unittest.TestCase):

# tries to import pandas
    def test_import_pandas(self):
        try:
            __import__ ("pandas")
        except ImportError:
            self.fail(f"Failed to import pandas")

# tries to import geopandas
    def test_import_geopandas(self):
        try:
            __import__ ("geopandas")
        except ImportError:
            self.fail(f"Failed to import geopandas")

# tries to import matplotlib
    def test_import_matplotlib(self):
        try:
            __import__ ("matplotlib")
        except ImportError:
            self.fail(f"Failed to import matplotlib")

# tries to import arcpy
    def test_import_arcpy(self):
        try:
            __import__ ("arcpy")
        except ImportError:
            self.fail(f"ArcPy not available in this environment")

# tries to import excelwings (skips for now as it's not installed in my environment)
    @unittest.skip("excelwings not currently installed in this environment")
    def test_import_excelwings(self):
        __import__ ("excelwings")

# tries to import custom GeoBC module 
    def test_import_geobc(self):
        try:
            __import__ ("geobc")
        except ImportError:
            self.fail(f"Failed to import geobc module")


# *** TEST CLASS 2: LIBRARY FUNCTIONS ***
# test that libraries actually work - these are examples, and can be expanded later
class TestFunctionality(unittest.TestCase):

# tests that pandas is functional
#   creates a dataframe and checks it has 3 rows 
    def test_pandas_dataframe_creation(self):
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
# *** TEST TO LOAD FILE GEODATABASE
    def test_geopandas_geodataframe_creation(self):
        import geopandas as gpd
        from shapely.geometry import Point

        gdf = gpd.GeoDataFrame(
            {"id": [1,2]},
            geometry=[Point(0,0), Point(1,1)],
            crs="EPSG:4326",
        )

        self.assertEqual(len(gdf), 2)
        self.assertEqual(str(gdf.crs), "EPSG:4326")


# *** TEST RUNNER ***
# runs all tests once executed
if __name__ == "__main__":
    unittest.main()  # pyright: ignore[reportUnusedCallResult]

# *** ADD A LOGGING SET UP