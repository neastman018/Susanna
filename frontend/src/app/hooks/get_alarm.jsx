import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { API_ENDPOINT } from "../constants";

export const useAlarm = () => {
  return useQuery({
    queryKey: ["alarm"],
    queryFn: () => getAlarmVariables(),
    refetchInterval: 2 * 1000, // automatically refetch every 2 seconds
    refetchIntervalInBackground: true, // keeps refetching even if tab is not focused
  });
};

export const getAlarmVariables = async () => {
  const response = await axios.get(`${API_ENDPOINT}/alarm`);
  return response.data;
};
