import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import SignUp from './pages/SignUp';
import EmailSent from './pages/EmailSent';
import EmailConfirmed from './pages/EmailConfirmed';
import Login from './pages/Login';
import AuthCallback from './pages/AuthCallback';

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/signup" element={<SignUp />} />
      <Route path="/email-sent" element={<EmailSent />} />
      <Route path="/confirm-email" element={<EmailConfirmed />} />
      <Route path="/login" element={<Login />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="*" element={<Navigate to="/signup" />} />
    </Routes>
  </BrowserRouter>
);
