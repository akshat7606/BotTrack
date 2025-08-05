(function () {
  const logs = [];
  const page = window.location.pathname;
  const userId = localStorage.getItem("bottrack_user") || Date.now().toString();
  localStorage.setItem("bottrack_user", userId);

  window.bottrack = {
    logUser: (msg) => logs.push({ sender: "user", message: msg }),
    logBot: (msg) => logs.push({ sender: "bot", message: msg }),
    send: async () => {
      const payload = {
        user_id: userId,
        page,
        started_at: new Date().toISOString(),
        messages: logs,
        exited_at: new Date().toISOString()
      };
      try {
        await fetch("http://localhost:8000/collect", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        logs.length = 0;
      } catch (e) {
        console.error("BotTrack error:", e);
      }
    }
  };

  window.addEventListener("beforeunload", () => {
    window.bottrack.send();
  });
})();
