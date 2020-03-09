## River Data Visualizer

- Bryce Shaw
- Zixin (James) Chen

### Abstract

This project is intended to gather all the data required for a river user to understand the state of a river drainage. It will ingest data from the government of Alberta environmental monitoring stations, and display related trends on a dashboard. 

This will be useful for recreational river users (kayakers, canoers, fisher folk), commercial river operators (whitewater rafting), and town planners interested in flood forecasting. 

The app will overlay selected trends for customizable time ranges, and offer group trends based on location concerned. 

### Project Scenario & Goals

The goal of this is to group together all available data trends that are available to determine the state of a river drainage. A user (person who in interested in understanding the drainage details) will be able to view all the information available to them in one place, select time frame window, scale trend axis, and view predictions (if that part gets implemented) 

### Design strategy

We will use python or node.js for the backend, React for the frontend. We will store data in a MySQL database, hosted in a docker container on a Cybera VM. Data will be added to the database using a webscraping function monitoring the alberta rivers webpage. We will investigate the feasibility of passing this into our database using a publish and subscribe message broker (AWS IoT core MQTT). The frontend webpage will submit query parameters to the backend, which will create queries to be sent to the database. The response will be parsed and made available to the frontend compenents. 

### Design Unknowns

- Designing a interactable front end which contains a visualization module.
- Visualize data gathered in the database using graphs and plots.
- Feasibility and suitability of MQTT message broker in this use case.

### Implementation Plan

- Data retrieval. Scrapes provided data source for specified date ranges.
- Real time retriever, which updates database with up-to-date information.
- Database Interface
- Database
- Frontend
- Visualization module -> displays requested data

### Evaluation

- Does it work?
- How responsive is it?
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
- MySQL
- AWS IoT Core MQTT
- Frontend using react.js
- Data import functions using python or Node.js

## ML model structure
- We will transform the data such that each point (hourly data, potentially down-sampled depending on computational limits) includes data from the last 14 days (potentially quite a bit less, depending on the drainage size) of data points.

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



