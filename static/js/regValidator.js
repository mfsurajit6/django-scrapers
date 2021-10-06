const form = document.getElementById("reg_form");

form.addEventListener("submit", (e) => {
  const username = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const cpassword = document.getElementById("cpassword").value;

  const name_error = document.getElementById("name_error");
  const email_error = document.getElementById("email_error");
  const password_error = document.getElementById("password_error");
  const cpassword_error = document.getElementById("cpassword_error");

  const atPos = email.indexOf("@");
  const dotPos = email.lastIndexOf(".");

  let error = false;

  
  if (username === "" || username == null) {
    name_error.innerHTML = "Name is required";
    error = true;
  } else {
    name_error.innerHTML = "";
  }

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
  } else if (password.length < 6) {
    password_error.innerHTML = "Password must have 6 or more character";
    error = true;
  } else {
    password_error.innerHTML = "";
  }

  if (cpassword === "" || cpassword == null) {
    cpassword_error.innerHTML = "Confirem Password is required";
    error = true;
  } else if (cpassword !== password) {
    cpassword_error.innerHTML = "Password and Confirem Password must be same";
    error = true;
  } else {
    cpassword_error.innerHTML = "";
  }

  if (error) {
    e.preventDefault();
  }
});
