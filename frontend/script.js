const API_URL = "http://127.0.0.1:8000";

async function askQuestion() {
  const question = document.getElementById("question-input").value.trim();
  if (!question) {
    showError("Please enter a question.");
    return;
  }

  const btn = document.getElementById("ask-btn");
  btn.disabled = true;
  btn.textContent = "Thinking...";

  hideError();
  document.getElementById("results").classList.add("hidden");

  try {
    const response = await fetch(`${API_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.detail || "Something went wrong.");
      return;
    }

    displayResults(data);

  } catch (error) {
    showError("Could not connect to the backend. Make sure it is running.");
  } finally {
    btn.disabled = false;
    btn.textContent = "Ask";
  }
}

function displayResults(data) {
  document.getElementById("sql-output").textContent = data.sql;

  const thead = document.getElementById("table-head");
  const tbody = document.getElementById("table-body");
  thead.innerHTML = "";
  tbody.innerHTML = "";

  if (data.type === "modify") {
    document.getElementById("row-count").textContent =
      `Query executed successfully. ${data.affected_rows} row(s) affected.`;
    document.getElementById("results").classList.remove("hidden");
    return;
  }

  const headerRow = document.createElement("tr");
  data.columns.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);

  data.rows.forEach(row => {
    const tr = document.createElement("tr");
    row.forEach(cell => {
      const td = document.createElement("td");
      td.textContent = cell !== null ? cell : "NULL";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });

  const rowCount = data.rows.length;
  document.getElementById("row-count").textContent =
    `${rowCount} row${rowCount !== 1 ? "s" : ""} returned`;

  document.getElementById("results").classList.remove("hidden");
}

function showError(message) {
  const box = document.getElementById("error-box");
  box.textContent = message;
  box.classList.remove("hidden");
}

function hideError() {
  document.getElementById("error-box").classList.add("hidden");
}

document.getElementById("question-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") askQuestion();
});