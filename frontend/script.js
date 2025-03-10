document
  .getElementById("resume-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("resume");
    const file = fileInput.files[0];
    formData.append("resume", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        document.getElementById("output").innerHTML = `
                        <h2>Analysis Result:</h2>
                        <p><strong>Job Description:</strong> ${
                          result.job_description
                        }</p>
                        <p><strong>Name:</strong> ${result.name}</p>
                        <p><strong>Qualifications:</strong> ${result.qualifications.join(
                          ", "
                        )}</p>
                        <p><strong>Resume Score:</strong> ${
                          result.resume_score
                        }</p>
                        <h3>Resume Text Preview:</h3>
                        <p>${result.resume_preview}</p>
                    `;
      } else {
        document.getElementById(
          "output"
        ).innerHTML = `<p style="color:red;">${result.error}</p>`;
      }
    } catch (error) {
      document.getElementById(
        "output"
      ).innerHTML = `<p style="color:red;">An error occurred while processing the resume.</p>`;
    }
  });
