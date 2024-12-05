# SurfsUp - Climate Analysis API

## Overview
Welcome to the **SurfsUp Climate Analysis API**! This project analyzes weather data and provides a Flask-powered RESTful API to deliver insights on precipitation, temperature, and station information. The API is designed to support decisions related to climate analysis for potential business ventures.


### Files and Directories:
1. **`Resources/`**:
   - `hawaii.sqlite`: SQLite database containing weather data for Hawaii.
   - `hawaii_measurements.csv`: Raw data file with temperature and precipitation measurements.
   - `hawaii_stations.csv`: Metadata file for all weather stations.

2. **`app.py`**:
   - The main Flask application that provides various API routes for accessing climate data.

3. **`climate_starter.ipynb`**:
   - Jupyter Notebook that performs initial exploratory data analysis (EDA) and sets up queries used in the Flask application.

4. **`.ipynb_checkpoints/`**:
   - Auto-generated directory for Jupyter Notebook checkpoints (safe to ignore).

## API Endpoints
Here are the available API routes provided by the `app.py`:

### 1. `/`
- **Description**: Displays a list of all available API routes with descriptions.
- **Method**: GET

### 2. `/api/v1.0/precipitation`
- **Description**: Returns the last 12 months of precipitation data as JSON.
- **Output Example**:
  ```json
  {
      "2016-08-23": 0.0,
      "2016-08-24": 0.08,
      ...
  }


