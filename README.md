## River Data Visulaizer

- Bryce Shaw
- James Chen

### Abstract

This project is intended to gather all the data required for a river user to understand the state of a river drainage. It will ingest data from the government of Alberta environmental monitoring stations, and display related trends on a dashboard. 

This will be useful for recreational river users (kayakers, canoers, fisher folk), commercial river operators (whitewater rafting), and town planners interested in flood forecasting. 

The app will overlay selected trends for customizable time ranges, and offer group trends based on location concerned. 

### Design strategy

We will use python for the backend, Django for the frontend. We will store data in database (which database?), which will be local to the application. Requested data will be populated into the database and cached. If requested data is partially available in the database, only the missing parts will be scraped from online sources. 

### Design Unknowns

- How do we build a front end
- how do we visualise data 
- 

### Implementation Plan

- Data retrieval. Scrapes provided datasource for specified date ranges.
- real time retriver
- Database Interface
- Database
- Frontend
- Visualization module -> displays requested data

### Evaluation

- Does it work?
- How laggy is it?
- Are we able to use big data tools to create a forecast trend?


## Project Components
- Database
- Real-time data consumer
- Historical Data importer
- Spark ML model builder
- Data transform (Raw Data -> model inputs)
- Model outputs archiver
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



