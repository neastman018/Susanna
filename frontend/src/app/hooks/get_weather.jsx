import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export const useWeather = (lat, lon) => {
  return useQuery({
    queryKey: ["weather", lat, lon],
    queryFn: () => getWeatherVariables(lat, lon),
    refetchInterval: 10 * 60 * 1000, // automatically refetch every 10 minutes
    refetchIntervalInBackground: true, // keeps refetching even if tab is not focused
  });
};

export const getWeatherVariables = async (lat, lon) => {
  const params = {};
  if (lat != null) params.lat = lat;
  if (lon != null) params.lon = lon;
  const response = await axios.get("/api/weather", { params });
  return response.data;
};
