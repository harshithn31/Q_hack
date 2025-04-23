import { Box, Flex, Button, Heading, IconButton, useColorMode, useBreakpointValue } from "@chakra-ui/react";
import { SunIcon, MoonIcon } from "@chakra-ui/icons";

export default function NavBar({ onGoHome, onGoDashboard, current, showColorModeToggle }) {
  const { colorMode, toggleColorMode } = useColorMode();
  const isMobile = useBreakpointValue({ base: true, md: false });
  return (
    <Box
      bg={colorMode === "dark" ? "gray.900" : "brand.600"}
      color={colorMode === "dark" ? "gray.100" : "white"}
      py={3}
      px={{ base: 4, md: 8 }}
      boxShadow="sm"
      position="sticky"
      top={0}
      zIndex={10}
    >
      <Flex
        align="center"
        justify="space-between"
        direction={isMobile ? "column" : "row"}
        gap={isMobile ? 2 : 0}
      >
        <Heading size="md" mb={isMobile ? 2 : 0}>Q-Summit Learning</Heading>
        <Flex gap={2} align="center">
          <Button
            colorScheme={current === "home" ? "brand" : "whiteAlpha"}
            variant={current === "home" ? "solid" : "ghost"}
            onClick={onGoHome}
            size={isMobile ? "sm" : "md"}
          >
            Home
          </Button>
          <Button
            colorScheme={current === "dashboard" ? "brand" : "whiteAlpha"}
            variant={current === "dashboard" ? "solid" : "ghost"}
            onClick={onGoDashboard}
            size={isMobile ? "sm" : "md"}
          >
            Dashboard
          </Button>
          {showColorModeToggle && (
            <IconButton
              aria-label="Toggle color mode"
              icon={colorMode === "dark" ? <SunIcon /> : <MoonIcon />}
              onClick={toggleColorMode}
              size={isMobile ? "sm" : "md"}
              variant="ghost"
              color={colorMode === "dark" ? "yellow.300" : "accent.400"}
              ml={2}
            />
          )}
        </Flex>
      </Flex>
    </Box>
  );
}
