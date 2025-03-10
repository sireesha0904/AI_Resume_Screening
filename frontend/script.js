  document
    .getElementById("upload-form")
    .addEventListener("submit", async function (event) {
      event.preventDefault();

      const fileInput = document.getElementById("resume");
      const formData = new FormData();
      formData.append("resume", fileInput.files[0]);

      console.log("File Selected:", fileInput.files[0]); // Debugging

      const loadingSpinner = document.getElementById("loading-spinner");
      const resultDiv = document.getElementById("result");

      loadingSpinner.style.display = "block";
      resultDiv.style.display = "none";

    try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });


      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server Error:", errorText);
        alert("Error: " + errorText);
        return;
      }

      const data = await response.json();
      document.getElementById("name").textContent = data.name;
      document.getElementById("job-description").textContent =
        data.job_description;
      document.getElementById("qualifications").textContent =
        data.qualifications.join(", ");
      document.getElementById("resume-score").textContent = data.resume_score;

      loadingSpinner.style.display = "none";
      resultDiv.style.display = "block";
    } catch (error) {
      console.error("Fetch Error:", error);
      alert("An error occurred while processing the resume.");
    } finally {
      loadingSpinner.style.display = "none";
    }
    });
