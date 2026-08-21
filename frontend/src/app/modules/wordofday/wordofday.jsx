'use client';

import React from 'react';
import Typography from '@mui/material/Typography';
import { Box, Stack, Container } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import { useWordOfDay } from '../../hooks/get_wordofday';
import styles from './wordofday.modules.css'; // Import your CSS module for styling


export default function WordOfDay() {
    const { data: wordData, isLoading, isError } = useWordOfDay();

    if (isLoading || !wordData) {
        return (
        <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
            <CircularProgress />
        </Container>
        );
    }

    if (isError || wordData.error) {
        return (
        <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
            <Typography color="error">Could not fetch word of the day.</Typography>
        </Container>
        );
    }

    return (
    <Box
        sx={{
            display: 'inline-block',
            backgroundImage: 'url(/stickynote.png)',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'left',
            backgroundSize: '100% 100%',
            borderTopLeftRadius: 10,
            borderTopRightRadius: 10,
            borderBottomLeftRadius: 10,
            // boxShadow: '2.5px 5px 5px rgba(50,50,50,0.6), 3px 6px 7px rgba(50,50,50,0.4), 4px 8px 15px rgba(50,50,50,0.3)',
            width: '100%',
            padding: 2,
            minHeight: '150px',
            overflow: 'hidden',
        }}
        >
        <Stack spacing={0.5} sx={{ p: 2 }}>
            <Typography variant="h5" color="text.contrast" fontWeight="bold">Word of the Day</Typography>
            <hr className={styles.breakline} />

            <Typography variant="h5" color="text.contrast" fontWeight="bold" sx={{fontFamily: 'fontFamilyComic', textTransform: 'capitalize'}}>{wordData.word}</Typography>
             <Stack spacing={0}>
                {wordData.definitions.map((def, idx) => {
                    let pofs;
                    if (def.partOfSpeech === "noun"){
                        pofs = "(n.)";
                    } else if (def.partOfSpeech === "verb"){
                        pofs = "(v.)";
                    } else if (def.partOfSpeech === "adjective"){
                        pofs = "(adj.)";
                    } else if (def.partOfSpeech === "adverb"){
                        pofs = "(adv.)";
                    } else {
                        pofs = def.partOfSpeech ? `(${def.partOfSpeech})` : '';
                    }
                    const text = def.text ? def.text : 'Definition not available';
                    return (
                        <Typography key={idx} variant="body2" color="text.contrast" sx={{ fontFamily: 'fontFamilyComic' }}>
                            {pofs} {text}
                        </Typography>
                    );

                })}
             </Stack>

        </Stack>
        </Box>
    );
}
