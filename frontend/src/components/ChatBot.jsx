import { useState } from "react";
import { Box, VStack, Input, Button, Text, Spinner } from "@chakra-ui/react";

export default function ChatBot({ onPipelineComplete }) {
  const [messages, setMessages] = useState([
    { role: "system", content: "Hi! Upload your resume to get started." },
  ]);
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

  return (
    <Box p={4} bg="white" borderRadius="md"  boxShadow="md">
      <VStack align="stretch" spacing={2} mb={3} maxH="90vh" overflowY="auto">
        {messages.map((msg, i) => (
          <Text key={i} color={msg.role === "user" ? "blue.700" : "gray.700"}>
            <b>{msg.role === "user" ? "You" : msg.role === "bot" ? "Bot" : "System"}:</b> {msg.content}
          </Text>
        ))}
        {loading && <Spinner size="sm" />}
      </VStack>
      <Input
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        mb={2}
        isDisabled={loading}
      />
      <Button onClick={sendMessage} colorScheme="blue" isLoading={loading} w="100%">
        Send
      </Button>
    </Box>
  );
}
