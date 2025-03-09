document.getElementById('resumeForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('resume');
    
    formData.append('resume', fileInput.files[0]);
    
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            alert('Error: ' + response.statusText);
            return;
        }
        
        const data = await response.json();
        document.getElementById('name').textContent = data.name;
        document.getElementById('jobDescription').textContent = data.job_description;
        document.getElementById('qualificationScore').textContent = data.qualification_score + '%';
        document.getElementById('resumeScore').textContent = data.resume_score;
        
        document.getElementById('result').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    }
});
