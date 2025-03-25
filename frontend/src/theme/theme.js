import { extendTheme } from "@chakra-ui/react";

const customTheme = extendTheme({
  config: {
    initialColorMode: "light", // Default to light mode
    useSystemColorMode: false, // Disable system preference
  },
  colors: {
    brand: {
      50: "#eef2ff",
      100: "#d4e0ff",
      200: "#aac4ff",
      300: "#7fa8ff",
      400: "#558dff",
      500: "#326dff", // Vibrant yet soft blue
      600: "#2657cc",
      700: "#1b4199",
      800: "#102c66",
      900: "#081733",
    },
    gray: {
      50: "#f9fafb",
      100: "#f3f4f6",
      200: "#e5e7eb",
      300: "#d1d5db",
      400: "#9ca3af",
      500: "#6b7280", // Neutral gray
      600: "#4b5563",
      700: "#374151",
      800: "#1f2937",
      900: "#111827",
    },
    accent: {
      50: "#fdf2f8",
      100: "#fce7f3",
      200: "#fbcfe8",
      300: "#f9a8d4",
      400: "#f472b6",
      500: "#ec4899", // Modern pink accent
      600: "#db2777",
      700: "#be185d",
      800: "#9d174d",
      900: "#831843",
    },
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === "dark" ? "gray.900" : "gray.50", // Soft background
        color: props.colorMode === "dark" ? "gray.100" : "gray.800", // Comfortable contrast
      },
      "*::selection": {
        bg: props.colorMode === "dark" ? "brand.500" : "brand.300",
        color: "white",
      },
      a: {
        color: props.colorMode === "dark" ? "brand.400" : "brand.600",
        _hover: {
          textDecoration: "underline",
        },
      },
    }),
  },
});

export default customTheme;
