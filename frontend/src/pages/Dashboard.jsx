import {
  Box, Heading, Progress, VStack, HStack, Badge, Text, Table, Thead, Tbody, Tr, Th, Td,
  Button, Stack, Drawer, DrawerOverlay, DrawerContent, DrawerHeader, DrawerBody, useDisclosure, Spinner
} from "@chakra-ui/react";
import { useState } from "react";

const MOCK_XP = 120;
const MOCK_BADGES = ["Quiz Master", "Fast Learner"];
const MOCK_PROGRESS = 0.6;
const MOCK_QUIZ_HISTORY = [
  { module: "Intro to Python", score: 3, total: 3, date: "2025-04-20" },
  { module: "Machine Learning 101", score: 2, total: 3, date: "2025-04-21" },
];

export default function Dashboard({ onGoHome }) {
  const [xp] = useState(MOCK_XP);
  const [badges] = useState(MOCK_BADGES);
  const [progress] = useState(MOCK_PROGRESS);
  const [quizHistory] = useState(MOCK_QUIZ_HISTORY);
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const handleTakeQuiz = async (moduleName) => {
    setLoading(true);
    try {
      const res = await fetch("/api/quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "1", current_skill: "yes", module_title: moduleName }),
      });
      if (!res.ok) {
        throw new Error(`Error: ${res.status}`);
      }
      const data = await res.json();
      setQuizData(data.quiz);
      onOpen();
    } catch (error) {
      console.error("Failed to fetch quiz data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFinishQuiz = () => {
    // Process quiz results here
    onClose();
  };

  return (
    <Box
      maxWidth="95vw"
      minHeight="80vh"
      mx="auto"
      mt={{ base: 2, md: 10 }}
      p={{ base: 2, sm: 4, md: 8 }}
      bg={{ base: "white", _dark: "gray.800" }}
      borderRadius="lg"
      boxShadow="xl"
    >
      <Stack direction={{ base: "column", sm: "row" }} justify="space-between" mb={6} spacing={4}>
        <Heading size="lg">🎮 Dashboard</Heading>
        <Button colorScheme="brand" onClick={onGoHome} alignSelf={{ base: "flex-start", sm: "center" }}>
          Back to Learning
        </Button>
      </Stack>
      <VStack align="stretch" spacing={6}>
        <Box>
          <Text fontWeight="bold" mb={2}>XP & Badges</Text>
          <HStack spacing={4} flexWrap="wrap">
            <Badge colorScheme="purple" fontSize="lg">XP: {xp}</Badge>
            {badges.map((b, i) => (
              <Badge key={i} colorScheme="green" fontSize="lg">{b}</Badge>
            ))}
          </HStack>
        </Box>
        <Box>
          <Text fontWeight="bold" mb={2}>Learning Progress</Text>
          <Progress value={progress * 100} colorScheme="brand" borderRadius="md" h={3} />
          <Text mt={1}>{Math.round(progress * 100)}% toward your goal</Text>
        </Box>
        <Box overflowX="auto">
          <Text fontWeight="bold" mb={2}>Quiz History</Text>
          <Table variant="simple" size="sm" minW="350px">
            <Thead>
              <Tr>
                <Th>Module</Th>
                <Th>Score</Th>
                <Th>Date</Th>
                <Th>Take Quiz</Th>
              </Tr>
            </Thead>
            <Tbody>
              {quizHistory.map((q, i) => (
                <Tr key={i}>
                  <Td>{q.module}</Td>
                  <Td>{q.score} / {q.total}</Td>
                  <Td>{q.date}</Td>
                  <Td>
                    <Button size="sm" onClick={() => handleTakeQuiz(q.module)}>
                      Take Quiz
                    </Button>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>

      <Drawer placement="right" onClose={onClose} isOpen={isOpen} size="md">
        <DrawerOverlay />
        <DrawerContent>
          <DrawerHeader borderBottomWidth="1px">Quiz</DrawerHeader>
		<DrawerBody>
  {loading ? (
    <Spinner />
  ) : quizData ? (
    <Box>
      {quizData.map((q, idx) => (
        <Box key={idx} mb={4}>
          <Text fontWeight="bold">{q.question}</Text>
          <VStack align="start" mt={2}>
            {q.options.map((opt, i) => (
              <Button key={i} variant="outline" size="sm">
                {opt}
              </Button>
            ))}
          </VStack>
        </Box>
      ))}
    </Box>
  ) : (
    <Text>No quiz data available.</Text>
  )}
</DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
}

