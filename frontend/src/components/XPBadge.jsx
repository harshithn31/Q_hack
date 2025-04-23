import { Box, HStack, Badge, Text } from "@chakra-ui/react";
import { motion, AnimatePresence } from "framer-motion";

export default function XPBadge({ xp = 0, badges = [] }) {
  return (
    <Box
      p={6}
      bgGradient="linear(to-br, purple.50, white)"
      borderRadius="2xl"
      boxShadow="xl"
      textAlign="center"
      minW="240px"
    >
      <Text fontWeight="extrabold" fontSize="lg" mb={3} color="purple.700">
        Your Progress
      </Text>
      <HStack justify="center" spacing={3} mb={2}>
        <Badge colorScheme="purple" fontSize="xl" px={3} py={1} borderRadius="xl" boxShadow="md">
          XP: {xp}
        </Badge>
        <AnimatePresence>
          {badges.map((b, i) => (
            <motion.div
              key={b}
              initial={{ scale: 0.7, opacity: 0 }}
              animate={{ scale: 1.15, opacity: 1 }}
              exit={{ scale: 0.7, opacity: 0 }}
              transition={{ type: "spring", stiffness: 300, damping: 15 }}
              style={{ display: "inline-block" }}
            >
              <Badge
                colorScheme="green"
                fontSize="xl"
                px={3}
                py={1}
                borderRadius="xl"
                boxShadow="md"
                mr={1}
                style={{ fontWeight: "bold", letterSpacing: 1 }}
              >
                {b}
              </Badge>
            </motion.div>
          ))}
        </AnimatePresence>
      </HStack>
    </Box>
  );
}
