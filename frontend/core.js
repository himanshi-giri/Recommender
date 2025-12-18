async function getRecommendations() {
  const query = document.getElementById("query").value;
  const tableBody = document.querySelector("#resultsTable tbody");

  tableBody.innerHTML = "";

  if (!query) {
    alert("Please enter a query.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    });

    const data = await response.json();

    data.recommendations.forEach((item) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${item.assessment_name}</td>
        <td>${item.test_type.join(", ")}</td>
        <td><a href="${item.assessment_url}" target="_blank">View</a></td>
      `;

      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error(error);
    alert("Error connecting to backend");
  }
}
