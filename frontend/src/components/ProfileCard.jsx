
import { Avatar, Box, Heading, Text, VStack, Tag, Wrap, WrapItem } from "@chakra-ui/react";

export default function ProfileCard({
  name = "Jane Doe",
  avatarUrl = "https://bit.ly/broken-link",
  summary = "A passionate learner exploring tech and career growth.",
  skills = ["Python", "React", "Machine Learning", "Career Planning"],
}) {
  return (
    <Box p={6} bg="white" borderRadius="lg" boxShadow="md" textAlign="center" minHeight="80vh">
      <Avatar size="2xl" src={avatarUrl} mb={4} />
      <Heading size="md">{name}</Heading>
      <Text color="gray.500" mb={4}>Learner</Text>

      <VStack align="start" spacing={3}>
        <Box>
          <Text fontWeight="bold" mb={1}>Summary</Text>
          <Text color="gray.600" fontSize="sm">{summary}</Text>
        </Box>

        <Box w="100%">
          <Text fontWeight="bold" mb={1}>Skills</Text>
          <Wrap>
            {skills.map((skill, idx) => (
              <WrapItem key={idx}>
                <Tag colorScheme="blue">{skill}</Tag>
              </WrapItem>
            ))}
          </Wrap>
        </Box>
      </VStack>
    </Box>
  );
}

