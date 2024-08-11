import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Layout from './Components/Layout';
import CardV from './Components/Card';
import Typography from '@mui/joy/Typography';
import { Button } from '@mui/material';
import BasicSwitches from './Components/Switches';
import RightDrawer from './Components/RightDrawer';

const socket = io('http://127.0.0.1:5000');  // Replace with your Flask server's URL

function LiveDetection() {
  const [imageSrc, setImageSrc] = useState('');
  const [detections, setDetections] = useState([]);
  const [drawOpen, setDrawOpen] = useState(false)

  const addLabel = (className, action) => {
    socket.emit("label", { data: className, action: action });
    socket.on('response_event', (data) => {
      console.log("resp", data)
    })
  }
  const handleSwitch = (event) => {
    if (event.target.checked) {
      addLabel(event.target.value, 'add')
    } else {
      addLabel(event.target.value, 'remove')
    }
    console.log(event.target.value, event.target.checked)
  }
  useEffect(() => {
    socket.on('frame', (data) => {
      setImageSrc(`data:image/jpeg;base64,${data.image}`);
      //console.log(data)
      //setDetections(data.detections);
    });
    socket.on('classes', (data) => {
      console.log(data)
      setDetections(Object.entries(data).map((a) => a[1]))
    })

    return () => {
      socket.off('frame');
    };
  }, []);
  const toggleDrawer = (event, open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setDrawOpen(open);
  };

  return (
    <div>
      <Layout handleClasscontrol={() => setDrawOpen(true)} />
      <Typography fontWeight={'bold'} fontSize={20} alignContent={'center'} textAlign={'center'}>Live Object Detection By AJ</Typography>
      {imageSrc && (
        <CardV imgsrc={imageSrc} name_n_loc={{ name: 'Swaminathan Giridharan', loc: "Chennai" }} />
      )}
      {drawOpen && <RightDrawer toggleDrawer={toggleDrawer} open={drawOpen} handleSwitch={handleSwitch} detections={detections} />}
    </div>
  );
}

export default LiveDetection;
