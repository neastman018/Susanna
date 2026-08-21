import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export const useWordOfDay = () => {
  return useQuery({
    queryKey: ["wordofday"],
    queryFn: () => getWordOfDayVariables(),
    refetchInterval: 60 * 60 * 1000, // automatically refetch every hour
    refetchIntervalInBackground: true, // keeps refetching even if tab is not focused
  });
};

export const getWordOfDayVariables = async () => {
  const response = await axios.get("/api/wordofday");
  return response.data;
};
