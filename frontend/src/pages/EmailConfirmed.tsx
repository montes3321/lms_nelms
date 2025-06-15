import React, { useEffect } from 'react';

export default function EmailConfirmed() {
  useEffect(() => {
    setTimeout(() => {
      window.location.href = '/login';
    }, 3000);
  }, []);

  return <p>Email confirmed. Redirecting to login...</p>;
}
