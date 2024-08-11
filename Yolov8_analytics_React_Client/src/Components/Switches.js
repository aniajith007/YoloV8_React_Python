import * as React from 'react';
import Switch from '@mui/material/Switch';
import { Box, FormControlLabel } from '@mui/material';

const label = { inputProps: { 'aria-label': 'Switch demo' } };

export default function BasicSwitches({ classes, handleClick }) {
    return (
        <div>
            {classes && classes.map((cl,index) =>
                <Box key={index}>
                    <FormControlLabel
                        value={cl}
                        control={<Switch onClick={handleClick} {...label} />}
                        label={cl}
                        labelPlacement="start"
                    />
                </Box>
            )
            }
        </div>
    );
}