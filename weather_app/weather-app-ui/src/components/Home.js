import React, { useEffect, useState } from 'react';
import api from '../services/api';

const Home = () => {
  const [weatherData, setWeatherData] = useState(null);

  useEffect(() => {
    // Fetch current weather data from the Django REST API
    const fetchWeatherData = async () => {
      try {
        const response = await api.get('/weather-api/');
        setWeatherData(response.data);
      } catch (error) {
        console.log('Failed to fetch weather data:', error);
      }
    };

    fetchWeatherData();
  }, []);

  if (!weatherData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Current Weather</h1>
      <p>Temperature: {weatherData.temperature}</p>
      <p>Wind Speed: {weatherData.wind_speed}</p>
      <p>Humidity: {weatherData.humidity}</p>
      <p>Precipitation: {weatherData.precipitation}</p>
      <p>Country: {weatherData.country}</p>
      <p>City: {weatherData.city}</p>
      <p>Time: {weatherData.timestamp}</p>
      </div>
  );
};

export default Home;
