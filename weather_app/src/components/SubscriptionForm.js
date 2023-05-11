import React, { useState } from 'react';
import api from '../services/api';

const SubscriptionForm = () => {
  const [email, setEmail] = useState('');

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    // Make a POST request to subscribe the user
    try {
      await api.post('/subscribe/', { email });
      setEmail('');
      alert('Subscription successful!');
    } catch (error) {
      console.log('Failed to subscribe:', error);
      alert('Subscription failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Subscribe to Weather Notifications</h2>
      <form onSubmit={handleFormSubmit}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Subscribe</button>
      </form>
    </div>
  );
};

export default SubscriptionForm;
