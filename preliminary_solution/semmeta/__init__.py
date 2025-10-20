# semmeta/__init__.py

# Core imports
from .metadata_Module import SEMMetaData
from .cleanjson_Module import JsonCleaner
from .visualize_Module import SEMVisualizer

# Instantiate reusable objects (optional)
SEMMeta = SEMMetaData()
CLEANER = JsonCleaner()

# Expose them for direct import
__all__ = ['SEMMetaData', 'JsonCleaner', 'SEMMeta', 'CLEANER', 'SEMVisualizer']

