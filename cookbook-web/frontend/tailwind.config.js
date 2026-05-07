/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Anthropic brand palette (from skills/brand-guidelines)
        ink: "#141413",
        cream: "#faf9f5",
        midGray: "#b0aea5",
        lightGray: "#e8e6dc",
        accent: {
          orange: "#d97757",
          blue: "#6a9bcc",
          green: "#788c5d",
        },
      },
      fontFamily: {
        display: ["Poppins", "Arial", "sans-serif"],
        body: ["Lora", "Georgia", "serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
