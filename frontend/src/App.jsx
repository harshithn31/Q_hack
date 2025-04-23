import { ChakraProvider, ColorModeScript, Button } from "@chakra-ui/react";
import theme from "./theme";
import { useState } from "react";
import MainPage from "./pages/MainPage";
import Dashboard from "./pages/Dashboard";
import NavBar from "./components/NavBar";

function App() {
  const [page, setPage] = useState("home");
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <NavBar
        current={page}
        onGoHome={() => setPage("home")}
        onGoDashboard={() => setPage("dashboard")}
        showColorModeToggle={true}
      />
      {page === "home" && <MainPage />}
      {page === "dashboard" && <Dashboard onGoHome={() => setPage("home")} />}
    </ChakraProvider>
  );
}

export default App;
