import { useRef } from "react";
import { Box, Button, Text, Input, VStack } from "@chakra-ui/react";

export default function ResumeUpload({ onUpload }) {
  const inputRef = useRef();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    }
  };

  return (
    <Box p={6} bg="gray.50" borderRadius="lg" boxShadow="md" textAlign="center">
      <VStack spacing={4}>
        <Text fontSize="lg">Upload your resume (PDF)</Text>
        <Button onClick={() => inputRef.current.click()} colorScheme="blue">
          Choose PDF
        </Button>
        <Input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          display="none"
          onChange={handleFileChange}
        />
      </VStack>
    </Box>
  );
}
