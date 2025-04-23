import { Box, Avatar, Heading, Text } from "@chakra-ui/react";

export default function ProfileCard({ name = "Jane Doe", avatarUrl = "https://bit.ly/broken-link" }) {
  return (
    <Box p={6} bg="white" borderRadius="lg" boxShadow="md" textAlign="center" minHeight="80vh">
      <Avatar size="2xl" src={avatarUrl} mb={4} />
      <Heading size="md">{name}</Heading>
      <Text color="gray.500">Learner</Text>
    </Box>
  );
}
