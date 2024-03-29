# import math
# import numpy as np
# import pandas as pd
# import pygeohash as gh

# from klarna.ml_logic.utils import simple_time_and_memory_tracker

# def transform_time_features(X: pd.DataFrame) -> np.ndarray:

#     assert isinstance(X, pd.DataFrame)
#     pickup_dt = pd.to_datetime(X["pickup_datetime"],
#                                format="%Y-%m-%d %H:%M:%S UTC",
#                                utc=True,
#                                infer_datetime_format = True)

#     pickup_dt = pickup_dt.dt.tz_convert("America/New_York").dt
#     dow = pickup_dt.weekday
#     hour = pickup_dt.hour
#     month = pickup_dt.month
#     year = pickup_dt.year
#     hour_sin = np.sin(2 * math.pi / 24 * hour)
#     hour_cos = np.cos(2 * math.pi / 24 * hour)

#     result = np.stack([hour_sin, hour_cos, dow, month, year], axis=1)
#     return result


# def transform_lonlat_features(X: pd.DataFrame) -> pd.DataFrame:

#     assert isinstance(X, pd.DataFrame)
#     lonlat_features = ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]

#     def distances_vectorized(df: pd.DataFrame, start_lat: str, start_lon: str, end_lat: str, end_lon: str) -> dict:
#         """
#         Calculate the haverzine and manhattan distance between two points on the earth (specified in decimal degrees).
#         Vectorized version for pandas df
#         Computes distance in kms
#         """
#         earth_radius = 6371

#         lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
#         lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

#         dlon_rad = lon_2_rad - lon_1_rad
#         dlat_rad = lat_2_rad - lat_1_rad

#         manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)
#         manhattan_km = manhattan_rad * earth_radius

#         a = (np.sin(dlat_rad / 2.0)**2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon_rad / 2.0)**2)
#         haversine_rad = 2 * np.arcsin(np.sqrt(a))
#         haversine_km = haversine_rad * earth_radius

#         return dict(
#             haversize=haversine_km,
#             manhattan=manhattan_km)

#     result = pd.DataFrame(distances_vectorized(X, *lonlat_features))

#     return result

# def compute_geohash(X: pd.DataFrame, precision: int = 5) -> np.ndarray:
#     """
#     Add a geohash (ex: "dr5rx") of len "precision" = 5 by default
#     corresponding to each (lon,lat) tuple, for pick-up, and drop-off
#     """
#     assert isinstance(X, pd.DataFrame)

#     X["geohash_pickup"] = X.apply(lambda x: gh.encode(
#         x.pickup_latitude, x.pickup_longitude, precision=precision),
#                                     axis=1)
#     X["geohash_dropoff"] = X.apply(lambda x: gh.encode(
#         x.dropoff_latitude, x.dropoff_longitude, precision=precision),
#                                     axis=1)
#     return X[["geohash_pickup", "geohash_dropoff"]]
