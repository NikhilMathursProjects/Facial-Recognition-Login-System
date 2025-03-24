
import React, { useState, useRef,useContext } from 'react';
import Webcam from 'react-webcam';
import {Button,Box,Typography,CircularProgress} from '@mui/material';
import {CircleOutlined, CircleRounded, Face,Face2,Face2Outlined,LockClockOutlined,LockOpen, LoginOutlined} from '@mui/icons-material';
import axios from 'axios';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme();

const API_URL='http://localhost:5000';

const videoConstraints={
  facingMode: 'user',
  width:'1280',
  height:'720'
};

export default function App(){
  const webcamRef=useRef(null);
  const [mode,setMode]=useState('login');
  const [username,setUsername]=useState('');
  const [message,setMessage]=useState('');
  const [loading,setLoading]=useState(false);

  const capture = async () => {
    setLoading(true);
    try {
      const image = webcamRef.current.getScreenshot();
      if (!image) {
        throw new Error('Failed to capture image');
      }
  
      const payload = mode === 'register' 
        ? { image: image.split(',')[1], username } 
        : { image: image.split(',')[1] };
  
      console.log('Sending payload:', payload);
  
      const { data } = await axios.post(
        `${API_URL}/${mode}`,
        payload,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
  
      console.log('Response:', data);
      setMessage(data.message || (data.success ? 
        `${mode === 'login' ? 'Welcome' : 'Registered'} ${data.user || username}!` : 
        'Authentication Failed'
      ));
    } catch (err) {
      console.error('Error:', err);
      setMessage(err.response?.data?.message || err.message || 'Error occurred');
    } finally {
      setLoading(false);
    }
  };
  return(
    <ThemeProvider theme={theme}>
    <CssBaseline />

    HII wow
    <Box sx={{textAlign:'center',p:4}}>
      <Typography variant='h3' gutterBottom>
        {mode === 'login' ? 'Face Login' : 'Register Face'}
      </Typography>
      <Box sx={{ mb: 4, border: '2px solid #1976d2', borderRadius: 2, overflow: 'hidden' }}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          style={{ width: '100%', maxWidth: 640 }}
          />
      </Box>
      {mode === 'register' && (
        <input
        type="text"
        placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            margin: '16px',
            padding: '12px',
            fontSize: '1.1rem',
            border: '2px solid #1976d2',
            borderRadius: 4
          }}
        />
      )}

      <Box sx={{ '& button': { m: 1 } }}>
        <Button
          variant="contained"
          size="large"
          // startIcon={loading ? <CircleRounded/> : mode === 'login' ? <LockClockOutlined/> :<Face2/> }
          onClick={capture}
          disabled={loading}
          sx={{ px: 4, py: 1.5 }}
          >
          {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Register'}
          </Button>

        <Button
          variant="outlined"
          size="large"
          onClick={() => {
            setMode(mode === 'login' ? 'register' : 'login');
            setMessage('');
          }}
          sx={{ px: 4, py: 1.5 }}
          >
          Switch to {mode === 'login' ? 'Register' : 'Login'}
        </Button>
      </Box>

      {message && (
        <Typography
        variant="h6"
        color={message.includes('Welcome') || message.includes('Registered') ? 'success' : 'error'}
        sx={{ mt: 3 }}
        >
          {message}
        </Typography>
      )}


    </Box>
    </ThemeProvider>
  )
}