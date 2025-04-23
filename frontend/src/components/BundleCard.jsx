import { Box, Heading, Text, Badge, HStack, VStack } from "@chakra-ui/react";

// BundleCard now supports module-level fields: subtopics (array) and rationale (string)
export default function BundleCard({ title, description, skills = [], price, time_hours, subtopics = [], rationale }) {
  return (
    <Box bg="gray.50" borderRadius="lg" boxShadow="md" p={5} mb={4}>
      <Heading size="md" mb={1}>{title}</Heading>
      <Text mb={2} color="gray.600">{description}</Text>
      {skills.length > 0 && (
        <HStack spacing={2} mb={2}>
          {skills.map((s, i) => (
            <Badge key={i} colorScheme="blue">{s}</Badge>
          ))}
        </HStack>
      )}
      {subtopics.length > 0 && (
        <VStack align="start" spacing={0} mb={2}>
          <Text fontWeight="bold">Subtopics:</Text>
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {subtopics.map((sub, i) => <li key={i}>{sub}</li>)}
          </ul>
        </VStack>
      )}
      {rationale && (
        <Text mt={2} fontSize="sm" color="gray.500"><b>Why this module?</b> {rationale}</Text>
      )}
      <VStack align="start" spacing={1} fontSize="sm" mt={2}>
        {price !== undefined && <Text>Price: <b>€{price}</b></Text>}
        {time_hours !== undefined && <Text>Duration: <b>{time_hours}h</b></Text>}
      </VStack>
    </Box>
  );
}

