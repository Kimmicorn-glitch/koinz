import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brandRed: "#B11226",
        brandSoftRed: "#EE425E",
        brandLight: "#FFF6F7",
      },
      boxShadow: {
        soft: "0 8px 24px rgba(177, 18, 38, 0.12)",
      },
      borderRadius: {
        lg2: "1.25rem",
      },
      keyframes: {
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        slideUp: "slideUp 450ms ease-out",
      },
    },
  },
  plugins: [],
};

export default config;
