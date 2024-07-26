#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# In[2]:


pip install geopy


# In[3]:


import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# In[4]:


cities = [
    ["Kyiv", "Ukraine"],
    ["Warsaw", "Poland"],
    ["Berlin", "Germany"],
    ["London", "UK"],
    ["Madrid", "Spain"],
    ["Paris", "France"],
    ["Rome", "Italy"],
    ["Prague", "Czechia"],
    ["Istanbul", "Turkey"],
    ["Stockholm", "Sweden"],
    ["Sofia", "Bulgaria"],
    ["Bucharest", "Romania"],
    ["Zurich", "Switzerland"],
]
df = pd.DataFrame(cities, columns=["city", "country"])


# In[5]:


locator = Nominatim(user_agent="myGeocoder")
geocode = RateLimiter(locator.geocode, min_delay_seconds=.1)

def get_coordinates(city, country):
  response = geocode(query={"city": city, "country": country})
  return {
    "latitude": response.latitude,
    "longitude": response.longitude
  }

df_coordinates = df.apply(lambda x: get_coordinates(x.city, x.country), axis=1)
df = pd.concat([df, pd.json_normalize(df_coordinates)], axis=1)


# In[6]:


from getpass import getpass
openweathermap_api_key = getpass('Enter Openweathermap API key: ')


# In[7]:


import datetime

def get_weather(row):

  owm_url = f"https://api.openweathermap.org/data/2.5/weather?lat={row.latitude}&lon={row.longitude}&appid={openweathermap_api_key}"
  owm_response = requests.get(owm_url)
  owm_response_json = owm_response.json()
  sunset_utc = datetime.datetime.fromtimestamp(owm_response_json["sys"]["sunset"])
  return {
      "temp": owm_response_json["main"]["temp"] - 273.15,
      "description": owm_response_json["weather"][0]["description"],
      "icon": owm_response_json["weather"][0]["icon"],
      "sunset_utc": sunset_utc,
      "sunset_local": sunset_utc + datetime.timedelta(seconds=owm_response_json["timezone"])
  }

df_weather = df.apply(lambda x: get_weather(x), axis=1)
df = pd.concat([df, pd.json_normalize(df_weather)], axis=1)


# In[8]:


try:
  import geopandas as gpd
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install geopandas')
  import geopandas as gpd

try:
  import contextily as ctx
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install contextily')
  import contextily as ctx


# In[9]:


pip install geopandas


# In[10]:


try:
  import geopandas as gpd
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install geopandas')
  import geopandas as gpd

try:
  import contextily as ctx
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install contextily')
  import contextily as ctx


# In[12]:


pip install contextily


# In[13]:


try:
  import geopandas as gpd
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install geopandas')
  import geopandas as gpd

try:
  import contextily as ctx
except ModuleNotFoundError:
  if 'google.colab' in str(get_ipython()):
    get_ipython().run_line_magic('pip', 'install contextily')
  import contextily as ctx


# In[14]:


gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=4326)


# In[18]:


from skimage import io
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage  

# plot city location marker
ax = gdf.to_crs(epsg=3857).plot(figsize=(12,8), color="black")

# add weather icon
def add_icon(row):
  img = io.imread(f"https://openweathermap.org/img/wn/{row.icon}@2x.png")
  img_offset = OffsetImage(img, zoom=.4, alpha=1, )
  ab = AnnotationBbox(img_offset, [row.geometry.x+150000, row.geometry.y-110000], frameon=False)
  ax.add_artist(ab)

gdf.to_crs(epsg=3857).apply(add_icon, axis=1)

# add city name label
gdf.to_crs(epsg=3857).apply(lambda x: ax.annotate(text=f"{x.city}  ", fontsize=10, color="black", xy=x.geometry.centroid.coords[0], ha='right'), axis=1);

# add temperature
gdf.to_crs(epsg=3857).apply(lambda x: ax.annotate(text=f" {round(x.temp)}°", fontsize=15, color="black", xy=x.geometry.centroid.coords[0], ha='left'), axis=1);

# add margins
xmin, ymin, xmax, ymax = gdf.to_crs(epsg=3857).total_bounds
margin_y = .2
margin_x = .2
y_margin = (ymax - ymin) * margin_y
x_margin = (xmax - xmin) * margin_x

ax.set_xlim(xmin - x_margin, xmax + x_margin)
ax.set_ylim(ymin - y_margin, ymax + y_margin)

# add basemap
ctx.add_basemap

ax.set_axis_off()


# In[ ]:




