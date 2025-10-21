import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { API_ENDPOINT } from "../constants";

export const useQuote = () => {
  return useQuery({
    queryKey: ["quotes"],
    queryFn: () => getQuoteVariables(),
    refetchInterval: 5 * 60 * 1000, // automatically refetch every 5 minutes
    refetchIntervalInBackground: true, // keeps refetching even if tab is not focused
  });
};

export const getQuoteVariables = async () => {
  const response = await axios.get(`${API_ENDPOINT}/quotes`);
  return response.data;
};
