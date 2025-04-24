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

// Animated Quiz component for answer feedback
// Inject keyframes for blinking
const styles = `
@keyframes blink-green {
  0%, 100% { background: #38A169; }
  50% { background: #68D391; }
}
@keyframes blink-red {
  0%, 100% { background: #E53E3E; }
  50% { background: #FEB2B2; }
}`;
if (typeof window !== "undefined" && !document.getElementById("quiz-anim-style")) {
  const styleTag = document.createElement("style");
  styleTag.id = "quiz-anim-style";
  styleTag.innerHTML = styles;
  document.head.appendChild(styleTag);
}

function QuizAnimated({ quizData, onClose }) {
  const [selected, setSelected] = useState({}); // {qIdx: option}
  const [answered, setAnswered] = useState({}); // {qIdx: 'correct'|'wrong'}

  const handleSelect = (qIdx, option) => {
    if (answered[qIdx]) return;
    setSelected((prev) => ({ ...prev, [qIdx]: option }));
    const isCorrect = quizData[qIdx].correct_answer === option;
    setAnswered((prev) => ({ ...prev, [qIdx]: isCorrect ? "correct" : "wrong" }));
  };

  return (
    <Box>
      {quizData.map((q, qIdx) => (
        <Box key={qIdx} mb={6} p={3} borderWidth={1} borderRadius="lg">
          <Text fontWeight="bold" mb={2}>{q.question}</Text>
          <VStack align="stretch" spacing={2}>
            {q.options.map((opt, oIdx) => {
              const isSelected = selected[qIdx] === opt;
              const isAnswered = answered[qIdx];
              const isCorrect = q.correct_answer === opt;
              let bg = "gray.100";
              let anim = "";

              if (isAnswered) {
                if (isSelected && isCorrect) {
                  bg = "green.400";
                  anim = "blink-green 0.6s linear 2";
                } else if (isSelected && !isCorrect) {
                  bg = "red.400";
                  anim = "blink-red 0.6s linear 2";
                } else if (isCorrect) {
                  bg = "green.300";
                }
              }

              return (
                <Button
                  key={oIdx}
                  w="100%"
                  variant="outline"
                  colorScheme={
                    isAnswered
                      ? isCorrect
                        ? "green"
                        : isSelected
                          ? "red"
                          : "gray"
                      : "blue"
                  }
                  bg={bg}
                  style={{ animation: anim }}
                  onClick={() => handleSelect(qIdx, opt)}
                  isDisabled={!!isAnswered}
                  _hover={isAnswered ? {} : undefined}
                >
                  {opt}
                </Button>
              );
            })}
          </VStack>
          {answered[qIdx] && (
            <Text mt={2} color={answered[qIdx] === "correct" ? "green.600" : "red.600"} fontWeight="bold">
              {answered[qIdx] === "correct"
                ? "Correct!"
                : (
                  <>
                    Wrong. Correct answer: <span style={{ color: '#38A169' }}>{q.correct_answer}</span>
                  </>
                )}
            </Text>
          )}
        </Box>
      ))}
      <HStack justify="flex-end" mt={4}>
        <Button colorScheme="blue" onClick={onClose}>Close</Button>
      </HStack>
    </Box>
  );
}

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
      console.log(data);
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
              <QuizAnimated quizData={quizData} onClose={onClose} />
            ) : (
              <Text>No quiz data available.</Text>
            )}
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
}
