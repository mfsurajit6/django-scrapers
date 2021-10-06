const loginForm = document.getElementById("login_form");

loginForm.addEventListener("submit", (e) => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const email_error = document.getElementById("email_error");
  const password_error = document.getElementById("password_error");

  const atPos = email.indexOf("@");
  const dotPos = email.lastIndexOf(".");

  let error = false;

  if (email === "" || email == null) {
    email_error.innerHTML = "Email is required";
    error = true;
  } else if (atPos < 2 || dotPos < atPos + 2 || dotPos === email.lenght) {
    email_error.innerHTML = "Please enter a valid email address";
    error = true;
  } else {
    email_error.innerHTML = "";
  }

  if (password === "" || password == null) {
    password_error.innerHTML = "Password is required";
    error = true;
  } else {
    password_error.innerHTML = "";
  }


  if (error) {
    e.preventDefault();
  }
});
