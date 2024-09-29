import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      width: {
        '20': '30vw', // Custom width 1
        '40': '60%',    // Custom width 2
        '35': '80vw',    // Custom width 3
      },

      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        darkbrown: "#6E493A",
        lightbrown: "#D6AC96",
        beige: "#FFF5E0",
        special: "f9b233",
      },
    },
  },
  plugins: [],
};
export default config;
