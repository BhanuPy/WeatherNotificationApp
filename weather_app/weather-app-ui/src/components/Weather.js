import { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col } from 'react-bootstrap';
import './styles.css';

function Weather() {
  const [weatherForecast, setWeatherForecast] = useState([]);

  useEffect(() => {
    axios.get('/api/weather/forecast/')
      .then(response => {
        setWeatherForecast(response.data);
      })
      .catch(error => console.log(error));
  }, []);

  return (
    <Container>
      <Row>
        <Col md={{ span: 6, offset: 3 }}>
          <h1>Weather Forecast</h1>
          <hr />
          {weatherForecast.map(forecast => (
            <div key={forecast.datetime}>
              <p><strong>Date:</strong> {forecast.datetime}</p>
              <p><strong>Temperature:</strong> {forecast.temperature} &deg;C</p>
              <p><strong>Wind Speed:</strong> {forecast.wind_speed} m/s</p>
              <p><strong>Humidity:</strong> {forecast.humidity} %</p>
              <hr />
            </div>
          ))}
        </Col>
      </Row>
    </Container>
  );
}

export default Weather;
