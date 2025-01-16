document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.querySelector(".ai-input");
  const outputContent = document.querySelector(".output-content");
  const sendButton = document.querySelector(".send-button");

  const handleInput = async () => {
    const input = inputField.value.trim();
    if (!input) {
      outputContent.innerHTML =
        "<p>Please enter a valid question for Maya.</p>";
      return;
    }

    // Show loading message
    outputContent.innerHTML = "<p>Maya is thinking...</p>";

    try {
      const response = await fetch("http://127.0.0.1:5000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        outputContent.innerHTML = `<p style="color: red;">Error: ${errorData.error}</p>`;
        return;
      }

      const data = await response.json();
      const imageRegex = /(https?:\/\/[^\s]+?\.(?:png|jpe?g|gif|webp))/gi;
      const transformedResponse = data.response.replace(
        imageRegex,
        '<img src="$1" alt="Image from Maya" />',
      );

      outputContent.innerHTML = `<div>${transformedResponse}</div>`;
    } catch (error) {
      console.error("Fetch error:", error);
      outputContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
  };

  sendButton.addEventListener("click", handleInput);
});
