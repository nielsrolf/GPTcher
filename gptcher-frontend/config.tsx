const config = {
    backendUrl: process.env.NODE_ENV === 'production'
      ? 'https://api.gptcher.com'
      : 'http://localhost:5555',
  };
export default config;
  