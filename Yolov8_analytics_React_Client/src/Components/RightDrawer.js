import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import { Box, TextField, Typography } from '@mui/material';
import BasicSwitches from './Switches';
export default function RightDrawer({ toggleDrawer, open, handleSwitch, detections }) {
    const [filtClasess, setFiltclasses] = React.useState(detections)
    const handleSearch = (event) => {
        console.log(event.target.value)
        setFiltclasses(detections.filter((className) => className.includes(event.target.value)))
    }
    return (
        <div>

            <React.Fragment >
                <Drawer
                    anchor={'right'}
                    open={open}
                    onClose={toggleDrawer(false)}
                >

                    <Box
                        sx={{ width: 400 }}
                        role="presentation"
                    //onClick={toggleDrawer(false)}
                    //onKeyDown={toggleDrawer(false)}
                    >
                        <Typography align='center' textAlign={'center'}>Class Controls</Typography>
                        <TextField onChange={handleSearch} focused fullWidth sx={{mx:1}} />
                        <BasicSwitches classes={filtClasess} handleClick={handleSwitch} />
                    </Box>
                </Drawer>
            </React.Fragment>

        </div>
    );
}
