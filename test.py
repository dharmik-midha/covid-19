import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly
import folium
import math
import os
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import tensorflow as tf
from pandas.io.json import json_normalize
from streamlit_folium import folium_static
from streamlit.script_request_queue import RerunData



url = 'https://api.covid19api.com/countries'
r = requests.get(url)
df0 = json_normalize(r.json())
st.write(df0)