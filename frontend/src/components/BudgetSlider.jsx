import { Box, Slider, SliderTrack, SliderFilledTrack, SliderThumb, Text, HStack } from "@chakra-ui/react";

export default function BudgetSlider({ budget, setBudget, min = 100, max = 1000 }) {
  return (
    <Box p={4} bg="white" borderRadius="lg" boxShadow="md" mb={4}>
      <Text mb={2} fontWeight="bold">Adjust Your Budget</Text>
      <HStack>
        <Slider
          aria-label="budget-slider"
          value={budget}
          min={min}
          max={max}
          step={10}
          onChange={setBudget}
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
        <Text ml={4} fontWeight="bold">€{budget}</Text>
      </HStack>
      <Text mt={1} color="gray.500" fontSize="sm">// TODO: Connect this to dynamic pricing logic</Text>
    </Box>
  );
}
