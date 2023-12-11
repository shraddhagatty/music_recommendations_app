import React, { Dispatch, SetStateAction, useState } from "react"
import {
    Slider,
    SliderTrack,
    SliderFilledTrack,
    SliderThumb,
    SliderMark,
    Box,
    Tooltip,
  } from '@chakra-ui/react'

  interface Props {
    sliderValue: number;
    setSliderValue: Dispatch<SetStateAction<number>>;
    disappearingToolTip?: boolean;
  }
export default function CustomSlider(props:  Props) {
    const {sliderValue,setSliderValue, disappearingToolTip = true} = props;
    const [showTooltip, setShowTooltip] = React.useState(false)
    const labelStyles = {
      mt: '2',
      ml: '-2.5',
      fontSize: 'sm',
    }
  
    return (
      <Box pt={6} pb={2}>
        <Slider aria-label='slider-ex-6' onChange={(val) => setSliderValue(val)}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        >
          <SliderMark value={25} {...labelStyles}>
            25%
          </SliderMark>
          <SliderMark value={50} {...labelStyles}>
            50%
          </SliderMark>
          <SliderMark value={75} {...labelStyles}>
            75%
          </SliderMark>
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <Tooltip
            hasArrow
            bg='teal.500'
            color='white'
            placement='top'
            isOpen={disappearingToolTip && showTooltip}
            label={`${sliderValue}%`}
          >
          <SliderThumb />
          </Tooltip>
        </Slider>
      </Box>
    )
  }