import { NextResponse } from 'next/server';

/**
 * Word of the Day API Route
 * Implements exponential backoff as required for API reliability.
 */

const API_KEY = process.env.WORDNIK_API_KEY;
const WORDNIK_URL = `https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key=${API_KEY}`;

export async function GET(request) {
    const maxRetries = 5;
    
    const fetchWithBackoff = async (retries, delay) => {
        try {
            const response = await fetch(WORDNIK_URL);
            
            if (!response.ok) {
                // Only retry on rate limits or server errors
                if (retries > 0 && (response.status === 429 || response.status >= 500)) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                    return fetchWithBackoff(retries - 1, delay * 2);
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            if (retries > 0) {
                await new Promise(resolve => setTimeout(resolve, delay));
                return fetchWithBackoff(retries - 1, delay * 2);
            }
            throw error;
        }
    };

    try {
        const data = await fetchWithBackoff(maxRetries, 1000);
        return NextResponse.json(data, { status: 200 });
    } catch (error) {
        // Log error internally, return friendly message to user
        return NextResponse.json(
            { error: 'Failed to fetch word of the day after multiple attempts.' }, 
            { status: 500 }
        );
    }
}