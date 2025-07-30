<script>
    async function sendMessage() {
        const userInput = document.getElementById("userInput").value;
        if (!userInput.trim()) return;

        document.getElementById("chatBox").innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

        const response = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        document.getElementById("chatBox").innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;
        document.getElementById("userInput").value = "";
    }
</script>
