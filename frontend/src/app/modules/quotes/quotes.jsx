'use client';
import { Typography } from "@mui/material";
import React from 'react';
import { useQuote } from "../../hooks/get_quote";
import Card from "@mui/material/Card";
import CircularProgress from '@mui/material/CircularProgress';


export default function Quotes() {
    const {data: quoteData, isLoading, isError} = useQuote();

    return (
        <Card sx = {{ backgroundColor: 'rgba(255, 255, 255, 0.0)', padding:2}}>
        {isError ? (
            <Typography>Error loading quote</Typography>
        ) : isLoading || !quoteData ? (
            <CircularProgress />
        ) : (
            <Typography
                sx={{
                color: "#ece3e3ff",
                fontSize: "2.5rem",
                letterSpacing: "0.025rem",
                fontWeight: 200,
                fontFamily: "Roboto",
                textAlign: "center",
                lineHeight: "2.5rem",
                textShadow:  `
                    2.5px 5px 5px rgba(50, 50, 50, 0.6),
                    3px 6px 7px rgba(50, 50, 50, 0.4),
                    4px 8px 15px rgba(50, 50, 50, 0.3)
                    `,
                padding: "35px",
                }}>
                "{quoteData.quote} - {quoteData.author ? quoteData.author : "Unknown"}"
            </Typography>
        
    )}
    </Card>
    )
}

    