// This is a js file can control the register page

// Get the password input box and display area
const passwordInput = document.getElementById('password1');
const strengthDisplay = document.getElementById('password-strength');

passwordInput.addEventListener('input', function() {
  const password = passwordInput.value;
  if (password) {
    const result = zxcvbn(password); // we use zxcvbn plugin
    // result.score ranges from 0 to 4
    let strengthText = "";
    let progressClass = "";
    switch(result.score) {
      case 0:
        strengthText = "Very weak";
        progressClass = "bg-danger";
        break;
      case 1:
        strengthText = "Weak";
        progressClass = "bg-danger";
        break;
      case 2:
        strengthText = "Fair";
        progressClass = "bg-warning";
        break;
      case 3:
        strengthText = "Good";
        progressClass = "bg-info";
        break;
      case 4:
        strengthText = "Strong";
        progressClass = "bg-success";
        break;
    }
 // Calculate width (percentage)
    const widthPercent = (result.score + 1) * 20;
    strengthDisplay.innerHTML = `
      <div class="progress">
        <div class="progress-bar ${progressClass}" role="progressbar" style="width: ${widthPercent}%;">
          ${strengthText}
        </div>
      </div>
    `;
  } else {
    strengthDisplay.innerHTML = "";
  }
});
