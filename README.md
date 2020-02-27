# River-Forecast-App
This is a project to model river flow data and forecast into the future. 

## Project Components
- Database
- Real-time data consumer
- Historical Data importer
- Spark ML model builder
- Data transform (Raw Data -> model inputs)
- Front end

## Frameworks
- Apache Spark ML
- MySQL (?)
- Apache Kafka
- Frontend using react.js
- data import functions using java or Node.js

## ML model structure
- We will transform the data such that each point (hourly data, potentially downsampled depending on computational limits) includes data from the last 14 days (potentially quite a bit less, depending on the drainage size) of data points.

## Model Features
- River Level (target)
- Precipitation
- Date
- Snow pillow height
- Temperature
- Cloud Cover

## Data Sources
- Snow pillow 
- River Flow 
- Weather 
- Precipitation

## Rivers of interest
- Pipestone River
- Spillimacheen River
- Elbow River
- Stikine River



