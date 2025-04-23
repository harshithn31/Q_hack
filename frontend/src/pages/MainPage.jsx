import { useState } from "react";
import { Box, Flex, Stack, Button, SimpleGrid } from "@chakra-ui/react";
import ProfileCard from "../components/ProfileCard";
import ResumeUpload from "../components/ResumeUpload";
import ChatBot from "../components/ChatBot";
import QuizView from "../components/QuizView";
import XPBadge from "../components/XPBadge";
import BundleCard from "../components/BundleCard";
import BudgetSlider from "../components/BudgetSlider";

export default function MainPage() {
  const [stage, setStage] = useState("upload"); // upload | chat | bundle | quiz | done
  const [quizSkill, setQuizSkill] = useState("");
  const [quizModule, setQuizModule] = useState("");
  const [xp, setXp] = useState(0);
  const [badges, setBadges] = useState([]);
  const [bundle, setBundle] = useState([]); // Will be set from backend API
  const [budget, setBudget] = useState(200);
  const [resumeId, setResumeId] = useState(null);

  const handleUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch("/api/upload-resume", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Failed to upload resume");
      const data = await res.json();
      setResumeId(data.resume_id || null);
      setStage("chat");
    } catch (err) {
      alert("Could not upload resume: " + err.message);
    }
  };
  const handlePipelineComplete = async ({ quizSkill, quizModule }) => {
    try {
      const res = await fetch("/api/recommend-bundle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_id: resumeId, chat_transcript: "" })
      });
      if (!res.ok) throw new Error("Failed to fetch bundle");
      const data = await res.json();
      setBundle(data.recommended_modules || []);
      setQuizSkill(quizSkill);
      setQuizModule(quizModule);
      setStage("bundle");
    } catch (err) {
      alert("Could not load personalized bundle: " + err.message);
    }
  };
  const handleQuizStart = () => {
    setStage("quiz");
  };
  const handleQuizComplete = ({ score, total }) => {
    // For prototype, award XP/badge locally
    setXp(score * 10);
    if (score === total) setBadges(["Quiz Master"]);
    setStage("done");
  };

  return (
    <Stack
      direction={{ base: "column", lg: "row" }}
      minH="100vh"
      bg={{ base: "gray.50", md: "gray.100" }}
      _dark={{ bg: { base: "gray.900", md: "gray.800" } }}
      align="stretch"
      justify={{ base: "center", lg: "flex-start" }}
      spacing={{ base: 2, md: 6, lg: 12 }}
      px={{ base: 1, sm: 2, md: 6 }}
      py={{ base: 4, md: 8 }}
      w="full"
      maxW="100vw"
    >
      <Box
        w="100%"
        maxW={{ base: "100%", sm: "480px", lg: "340px" }}
        mb={{ base: 0, lg: 0 }}
        px={{ base: 0, sm: 2 }}
      >
        <ProfileCard name="Jane Doe" avatarUrl="https://bit.ly/broken-link"/>
        {/* <Box mt={6}><XPBadge xp={xp} badges={badges} /></Box> */}
      </Box>
      <Box
        w="100%"
        flex="1"
        maxW="100%"
        mx="auto"
        px={{ base: 0, sm: 2 }}
      >
        {stage === "upload" && <ResumeUpload onUpload={handleUpload} />}
        {stage === "chat" && <ChatBot resumeId={resumeId} onPipelineComplete={handlePipelineComplete} />}
        {stage === "bundle" && (
          <Box>
            <BudgetSlider budget={budget} setBudget={setBudget} />
            <SimpleGrid columns={{ base: 1, sm: 1, md: 2, lg: 3 }} spacing={{ base: 4, md: 6 }} mt={4}>
              {bundle.map((b, i) => (
                <BundleCard key={i} {...b} />
              ))}
            </SimpleGrid>
            <Box textAlign="center" mt={4}>
              <Button
                colorScheme="brand"
                size={{ base: "md", md: "lg" }}
                w="100%"
                maxW="320px"
                mt={4}
                fontWeight="bold"
                borderRadius="lg"
                onClick={handleQuizStart}
              >
                Take Quiz to Unlock Next Module
              </Button>
            </Box>
          </Box>
        )}
        {stage === "quiz" && (
          <QuizView quizSkill={quizSkill} quizModule={quizModule} onQuizComplete={handleQuizComplete} />
        )}
        {stage === "done" && (
          <Box
            p={8}
            bg={{ base: "white", _dark: "gray.800" }}
            borderRadius="lg"
            textAlign="center"
            boxShadow="md"
          >
            🎉 All done! Check your progress on the left.
          </Box>
        )}
      </Box>
    </Stack>
  );
}
