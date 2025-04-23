import { useState } from "react";
import { Box, VStack, Text, Button, Alert } from "@chakra-ui/react";
import { Radio, RadioGroup } from "@chakra-ui/react";
import Confetti from "react-confetti";
import { motion, AnimatePresence } from "framer-motion";

export default function QuizView({ quizSkill, quizModule, onQuizComplete }) {
  const [quiz, setQuiz] = useState([
    {
      question: "Which of the following is a valid Python variable name?",
      options: ["1var", "var_1", "var-1", "var 1"],
      correct_answer: "var_1",
    },
    {
      question: "What does the 'print' function do in Python?",
      options: [
        "Outputs text to the console",
        "Reads input from the user",
        "Defines a variable",
        "Exits the program",
      ],
      correct_answer: "Outputs text to the console",
    },
    {
      question: "Which symbol is used to comment a single line in Python?",
      options: ["//", "#", "<!-- -->", "/* */"],
      correct_answer: "#",
    },
  ]);
  const [answers, setAnswers] = useState(Array(quiz.length).fill(""));
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);

  const handleSelect = (idx, value) => {
    const newAns = [...answers];
    newAns[idx] = value;
    setAnswers(newAns);
  };

  const handleSubmit = () => {
    let correct = 0;
    quiz.forEach((q, i) => {
      if (answers[i] === q.correct_answer) correct++;
    });
    setScore(correct);
    setSubmitted(true);
    onQuizComplete && onQuizComplete({ score: correct, total: quiz.length });
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -30 }}
        transition={{ duration: 0.5 }}
      >
        <Box
          p={8}
          bgGradient="linear(to-br, blue.50, white)"
          borderRadius="2xl"
          boxShadow="2xl"
          position="relative"
          minH="420px"
        >
          <Text fontSize="2xl" mb={6} fontWeight="extrabold" color="blue.700">
            Quiz: {quizSkill} <span style={{ color: '#888' }}>– {quizModule}</span>
          </Text>
          <VStack spacing={8} align="stretch">
            {quiz.map((q, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: 40 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.08 }}
              >
                <Box mb={2}>
                  <Text fontWeight="semibold" mb={2}>{idx + 1}. {q.question}</Text>
                  <RadioGroup
                    value={answers[idx]}
                    onChange={(val) => handleSelect(idx, val)}
                    isDisabled={submitted}
                  >
                    <VStack align="start">
                      {q.options.map((opt, i) => (
                        <Radio value={opt} key={i} _checked={{ bg: "blue.100", borderColor: "blue.600" }}>
                          {opt}
                        </Radio>
                      ))}
                    </VStack>
                  </RadioGroup>
                </Box>
              </motion.div>
            ))}
          </VStack>
          {!submitted ? (
            <Button
              mt={8}
              colorScheme="blue"
              size="lg"
              fontWeight="bold"
              px={10}
              py={6}
              borderRadius="xl"
              boxShadow="md"
              onClick={handleSubmit}
              isDisabled={answers.includes("")}
              _hover={{ bg: "blue.700", color: "white" }}
            >
              Submit Quiz
            </Button>
          ) : (
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: "spring", stiffness: 200 }}
            >
              <Alert
                status={score === quiz.length ? "success" : "info"}
                mt={8}
                borderRadius="xl"
                fontWeight="bold"
                fontSize="lg"
                bg={score === quiz.length ? "green.100" : "blue.50"}
                color={score === quiz.length ? "green.800" : "blue.800"}
                boxShadow="md"
              >
                {/* icon removed to fix import errors */}
                {score === quiz.length ? "Perfect! " : null}
                You scored {score} out of {quiz.length}!
              </Alert>
            </motion.div>
          )}
          {submitted && score === quiz.length && (
            <Confetti
              width={window.innerWidth / 2}
              height={window.innerHeight / 1.5}
              numberOfPieces={250}
              recycle={false}
              style={{ position: "absolute", top: 0, left: 0, zIndex: 5 }}
            />
          )}
        </Box>
      </motion.div>
    </AnimatePresence>
  );
}
