import { GenerativeModel } from "google-generativeai";

// Initialize the model
const model = new GenerativeModel("gemini-1.5-flash");

// Define the function to interact with the model
export async function queryAgent(input) {
  try {
    // Use await to handle the promise returned by generate_content
    const response = await model.generate_content(input);

    // Return the response text if available
    return response?.text || "No response received.";
  } catch (error) {
    // Handle any errors and return a message
    console.error("Error querying AI agent:", error.message, error.stack);
    return `Error: Unable to fetch response. Details: ${error.message}`;
  }
}

// Example usage
(async () => {
  const input = "Write a story about a magic backpack.";
  const response = await queryAgent(input);
  console.log("AI Response:", response);
})();
