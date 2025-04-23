import { useState, useRef, useEffect } from "react";
import { Box, VStack, Input, IconButton, Text, Spinner, HStack, Flex, useColorModeValue } from "@chakra-ui/react";
import { FaUser, FaRobot, FaCogs, FaPaperPlane } from "react-icons/fa";

export default function ChatBot({ resumeId, onPipelineComplete }) {
  const [messages, setMessages] = useState(
    resumeId
      ? []
      : [{ role: "system", content: "Hi! Upload your resume to get started." }]
  );
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setLoading(true);
    // Simulate API call, replace with real pipeline call
    setTimeout(() => {
      const botReply = {
        role: "bot",
        content: "Thanks! Here is your personalized learning bundle.",
      };
      setMessages((msgs) => [...msgs, botReply]);
      setLoading(false);
      onPipelineComplete({
        bundle: [{ title: "Intro to Python" }],
        quizSkill: "Python",
        quizModule: "Intro to Python",
      });
    }, 1500);
    setInput("");
  };

  const chatBottomRef = useRef(null);
const userBg = useColorModeValue("blue.100", "blue.800");
const botBg = useColorModeValue("gray.100", "gray.700");
const sysBg = useColorModeValue("yellow.50", "yellow.900");
const userColor = useColorModeValue("blue.800", "blue.100");
const botColor = useColorModeValue("gray.900", "gray.100");
const sysColor = useColorModeValue("yellow.800", "yellow.200");

useEffect(() => {
  chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages, loading]);

return (
  <Flex direction="column" h="80vh" maxH="80vh" bg={useColorModeValue("white", "gray.800")}
    borderRadius="md" boxShadow="md" p={4}>
    <HStack spacing={3} mb={4} justify="center">
      <Box boxSize={10} bgGradient="linear(to-br, blue.400, cyan.300)" borderRadius="full" display="flex" alignItems="center" justifyContent="center" boxShadow="sm">
        <FaRobot size={24} color="white" />
      </Box>
      <Text fontWeight="bold" fontSize="xl" color={useColorModeValue('blue.700', 'cyan.200')}>SkillGuide AI</Text>
    </HStack>
    <VStack align="stretch" spacing={2} flex={1} overflowY="auto" mb={2}>
      {messages.map((msg, i) => {
        let icon, align, bg, color;
        if (msg.role === "user") {
          icon = <FaUser size={20} color="#3182ce" />;
          align = "flex-end";
          bg = userBg;
          color = userColor;
        } else if (msg.role === "bot") {
          icon = <FaRobot size={20} color="#718096" />;
          align = "flex-start";
          bg = botBg;
          color = botColor;
        } else {
          icon = <FaCogs size={20} color="#ECC94B" />;
          align = "center";
          bg = sysBg;
          color = sysColor;
        }
        return (
          <Flex key={i} justify={align}>
            <HStack spacing={2} maxW="80%" bg={bg} color={color} px={4} py={2} borderRadius="lg" boxShadow="sm" alignItems="center">
              {align !== "flex-end" && icon}
              <Text fontSize="md" whiteSpace="pre-line">{msg.content}</Text>
              {align === "flex-end" && icon}
            </HStack>
          </Flex>
        );
      })}
      {loading && (
        <Flex justify="flex-start">
          <HStack spacing={2} maxW="80%" bg={botBg} color={botColor} px={4} py={2} borderRadius="lg" boxShadow="sm" alignItems="center">
            <FaRobot size={20} color="#718096" />
            <Spinner size="sm" />
          </HStack>
        </Flex>
      )}
      <div ref={chatBottomRef} />
    </VStack>
    <HStack spacing={2} mt={2}>
      <Input
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        isDisabled={loading}
        bg={useColorModeValue("gray.50", "gray.700")}
        borderRadius="lg"
      />
      <IconButton
        aria-label="Send"
        icon={<FaPaperPlane />}
        colorScheme="blue"
        onClick={sendMessage}
        isLoading={loading}
        borderRadius="full"
      />
    </HStack>
  </Flex>
);
}
