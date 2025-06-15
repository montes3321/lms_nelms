import React from 'react';
import { Button, Box } from '@mui/material';

export default function EmailSent() {
  return (
    <Box sx={{ textAlign: 'center', mt: 10 }}>
      <p>Confirmation email sent.</p>
      <Button href="mailto:" variant="outlined" sx={{ mr: 1 }}>Open Mail</Button>
      <Button onClick={() => window.location.reload()} variant="contained">Resend</Button>
    </Box>
  );
}
