import config from '@app-config/config.json';

const API_KEY = process.env.OPEN_WEATHER_API_KEY;

export async function GET(req) {
  try {
    const url = new URL(req.url);
    const lat = url.searchParams.get('lat') || config.WEATHER.LATITUDE;
    const lon = url.searchParams.get('lon') || config.WEATHER.LONGITUDE;

    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch weather: ${response.statusText}`);
    }

    const data = await response.json();

    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('Error in weather API:', err);
    return new Response(JSON.stringify({ error: 'Internal Server Error', details: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
