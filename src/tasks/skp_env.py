import os, sys, json, re
from pprint import pprint

# SKP
SKP_USER = os.environ["SKP_USER"]
SKP_HOME = os.environ["SKP_HOME"]

# JUPYTER
try:
    JUPYTER_HOME = os.environ["JUPYTER_HOME"]
    JUPYTER_GPU = os.environ["JUPYTER_GPU"]

    # JAVA
    JAVA_VER = os.environ["JAVA_VER"]

    # SCALA
    SCALA_VER = os.environ["SCALA_VER"]

    # JULIA
    JULIA_VER = os.environ["JULIA_VER"]

    # SPARK
    SPARK_VER = os.environ["SPARK_VER"]

    # R
    R_LIBS = os.environ["R_LIBS"]
    
    JUPYTER = True
except:
    JUPYTER = False

