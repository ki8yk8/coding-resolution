import { StrictMode } from "react"
import { createRoot } from "react-dom/client"

import "./index.css"
import App from "./app.tsx"
import { ThemeProvider } from "@/components/theme-provider.tsx"

// using dark theme in the web app
document.body.classList.add("dark")

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>
)
