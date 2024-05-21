# Intellistride-Internship

### Project Title: Real-Time Energy Meter Dashboard

## Overview

The Real-Time Energy Meter Dashboard project is designed to provide a live visualization of energy parameters such as voltage, current, power, and energy. This project integrates a Modbus-based data acquisition system with a MySQL database and a Dash web application to offer an interactive and real-time monitoring solution.

## Components

1. **Modbus Data Acquisition System**: This component reads energy data from a Modbus device using the PyModbus library.
  
2. **MySQL Database**: A relational database is used to store the energy data fetched from the Modbus device.
 
3. **Dash Web Application**: A web dashboard created using Dash (Plotly) to visualize the stored energy data in real-time.

## Features

- **Real-Time Data Collection**: Energy parameters are read from the Modbus device every 10 seconds.
  
- **Data Storage**: Collected data is stored in a MySQL database for persistent storage and historical analysis.
  
- **Interactive Dashboard**: The Dash web application provides a user-friendly interface to view instantaneous readings and time series graphs of the energy parameters.
  
- **Parameter Selection**: Users can select which parameters to view on the dashboard.
  
- **Automatic Updates**: The dashboard automatically updates every 10 seconds to reflect the latest data.

## Workflow

1. **Data Acquisition**: The Modbus client connects to the energy meter device via a serial connection, reads the required registers, and converts the binary data to floating-point values.
 
2. **Data Storage**: The acquired data is then inserted into the MySQL database with a timestamp.
   
3. **Data Visualization**: The Dash application queries the database at regular intervals to fetch the latest data and updates the graphs and readings on the dashboard.

## Installation and Setup

1. **Hardware Setup**: Connect the Modbus device to your computer via the appropriate serial port.
 
2. **Database Setup**: Install MySQL and create a database to store the energy data.
 
3. **Python Environment**: Install the necessary Python libraries including PyModbus, mysql-connector-python, Dash, and Plotly.
 
4. **Configuration**: Configure the serial port, Modbus settings, and MySQL connection details in the Python scripts.

## Running the Project

1. **Start Data Acquisition**: Run the real-time data acquisition script to start collecting and storing data in the MySQL database.
   
2. **Start the Dashboard**: Launch the Dash web application to start the real-time visualization of the energy parameters.

## Use Cases

- **Industrial Monitoring**: Real-time monitoring of energy consumption in industrial setups.
 
- **Home Energy Management**: Track and optimize energy usage in residential settings.
  
- **Educational Purposes**: Demonstrate real-time data acquisition and visualization concepts in academic projects.

## Future Enhancements

- **Alert System**: Implement alerts for threshold breaches in energy parameters.
  
- **Historical Data Analysis**: Add features for detailed historical data analysis and reporting.
 
- **Multi-Device Support**: Extend support for multiple Modbus devices and aggregate their data.

This project provides a comprehensive solution for real-time monitoring and visualization of energy data, offering insights and aiding in efficient energy management.
