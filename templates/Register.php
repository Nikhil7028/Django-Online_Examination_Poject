
<?php
$notMatch="";
if($_SERVER['REQUEST_METHOD']== "POST" && isset($_POST['registration'])){
	
    include 'include/DbConnect.php';

	
    $rollno = $_POST["rollno"];
    $Fname = $_POST["fname"];
	$Lname = $_POST["lname"];
    $Gender = $_POST["gender"];
	$Institute = $_POST["instit"];
    $Course = $_POST["course"];
	$MobNo = $_POST["mobno"];
    $email = $_POST["email"];
	$password= $_POST['psw'];
	$repassword= $_POST['psw-repeat'];
	if($password == $repassword)
	{
		$notMatch="";
		$sql="INSERT INTO candidate(Rollno,Fname,Lname, Gender,Institute,Course,MobNo,email,password) VALUES ('$rollno', '$Fname', '$Lname', '$Gender', '$Institute', '$Course', '$MobNo', '$email', '$password')";
		if ($conn->query($sql) === TRUE) {

			echo "<script>alert('New record created successfully. Login again')</script>";
		  } else {
			echo"<script>alert('Roll number is already exist')</script>";
		  }
		  
		  
	}
	else{
		$notMatch="Password and repeat password is not match";
	}
    $conn->close();
		  

    
}

?>



<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Registration Form</title>

	<!-- pattern="^(?=.*\d)(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9])\S{4,}$" -->
	<style>
		bodyd {
			font-family: Arial, sans-serif;
			background-color: #f3f3f3;
			margin: 0;
			padding: 0;
			display: flex;
			justify-content: center;
			align-items: left;
			height: 100vh;
		}

		.main {
			/* background-color: #fff; */
			border-radius: 15px;
			box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
			padding: 20px;
			width: 300px;
		}

		.main h2 {
			color: #4caf50;
			margin-bottom: 20px;
		}

		label {
			display: block;
			margin-bottom: 5px;
			color: black;
			font-weight: bold;
			font-size: 20px;
		}

		input[type="text"],
		input[type="email"],
		input[type="password"],
		select {
			width: 25%;
			margin-bottom: 15px;
			padding: 10px;
			size: 50%;
			border: 1px solid green;
			border-radius: 5px;
		}
		

		button[type="submit"] {
			padding: 15px;
			border-radius: 10px;
			border: none;
			background-color: #4caf50;
			color: white;
			cursor: pointer;
			width: 45%;
			font-size: 16px;
		}
		button[type="reset"] {
			padding: 15px;
			border-radius: 10px;
			border: none;
			background-color: blue;
			color: white;
			cursor: pointer;
			width: 45%;
			font-size: 16px;
		}
		.rightin{
			margin-left: 93px;
		}
		#cors{
			margin-left: 117px;
		}
		#colab{
			font-size: large;
		}
		#msgerror{color: red;}
		#msgok{color: #4caf50;}

	</style>

	<link rel="stylesheet" href="http://localhost/OnlineEx/css/StyleNav.css">
	<link rel="stylesheet" href="http://localhost/OnlineEx/css/StyRegistration.css">
	<!-- for icon -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"> 

	


</head>

<body class="remain">

	<ul>
		<li><a href="/index.php">Home</a></li>
		<li><a href="Welcome.php">Welcome</a></li>
		<li><a href="#contact">About</a></li>
		<li><a href="#about">Contact us</a></li>
		<li><a class="active" href="">Register</a></li>
		<li><a href="http://localhost/onlineEx/">Login</a></li>
	</ul>

	<img src="reg.jpeg" alt="Registration img">


	<div class="inre">
		<form action="" method="post">
			<div class="container">
				<h1>Register</h1>
				<p>Please fill in this form to create an account. *all feilds are mandatory. </p>
				<hr>
				<label for="rollno"><b>Roll no</b></label>
				<input type="text" placeholder="Enter roll no" pattern="^[a-zA-Z]{2}\d{6}$" name="rollno" id="rollno" title="Enter valid roll no" style="width: 30%; " required>
				<small>Enter full roll no. e.g. MC232501</small>

				<label for="name"><b>Student name</b></label>
				<input type="text" placeholder="Enter first name" pattern="^[a-zA-Z]{2,}$" name="fname" id="fname"
				title="Enter valid name" required>
				<input type="text"  placeholder="Enter last name" pattern="^[a-zA-Z]{2,}$" name="lname" id="lname" class="rightin" title="Enter valid name" required >
				<br>	
				<label for="Gender" style="display:contents;"><b>Gender: </b></label>
					<input type="radio" name="gender" value="Male" id="male" required><b>Male</b>
					<input type="radio" name="gender" value="Female" id="female"><b>Female</b> 
					
				<br><br>		
				
				
				<label for="institute" style="Display:inline;"><b>Institute <i class="fas fa-university"></i></b></label> <!-- <p id="colab">Course</p> -->

				<label for="course" style="Display:inline; margin-left:27% ;"><b>Course </b></label>
				<br>

				<select name="instit" required>      
					<option value="">---Select Institute---</option>
					<option value="ZIBACAR">ZIBACAR</option>
					<option value="ZIMCA">ZIMCA</option>
					<option value="ZGMI">ZGMI</option>
					<option value="ZCOER">ZCOER</option>
					<option value="other">Other</option>
				</select>
				
				
				<select  id="cors" name="course" required>
					<option value="">---Select Course---</option>
					<option value="MCA">MCA</option>
					<option value="MBA">MBA</option>
					<option value="other">Other</option>
				</select>

				<br><br>
				<label for="mobno" style="Display:inline;"><b>Mobile No.: <i class="fas fa-mobile"></i></b></label> <!-- <p id="colab">Course</p> -->

				<label for="mail" style="Display:inline; margin-left:25% ;"><b>Email <i class="fas fa-envelope"></i></b></label>
				<br>

				<input type="text" placeholder="Enter Mobile no." pattern="^[0-9]{10}$" maxlength="10" name="mobno" id="mobno" 
				title="Enter valid Mobile number" required>
				
				<input type="email" placeholder="Enter email" name="email" pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" id="email" class="rightin" title="Enter valid email" required>
				
				<!-- <label for="psw"><b>Password <i class="fas fa-lock"></i></b></label> -->
				<br>
				<label for="psw" style="Display:inline;"><b>Password   .<i class="fas fa-lock">   </i></b></label>

				<label for="psw-repeat" style="Display:inline; margin-left:25% ;"><b>Repeat Password </b></label>
				<br>

				<input type="password" placeholder="Enter strong Password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{7,}$" 
				name="psw" id="psw" title="Make strong password must contain at least one number and one uppercase, lowercase letter, special symbol and at least 7 or more characters"  required>
				
				<input type="password" placeholder="Repeat Password" name="psw-repeat" id="psw-repeat" class="rightin" onkeyup="checkPassMatch();" required> <span id="msgerror">.</span><span id="msgok">.</span>

				<p style="color:red;"><?php echo $notMatch ?></p>
				<hr>
				<input type="checkbox" required>    <p style="display:inline;">By creating an account you agree to our <a href="#">Terms & Privacy</a>.</p> <br><br>

				<button type="reset" class="resetbtn">Reset</button>
				<button type="submit" name="registration" class="registerbtn">Register</button>
			</div>

			<div class="container signin">
				<p>Already have an account? <a href="http://localhost/onlineEx/">Sign in</a>.</p>
			</div>
	</div>

	</form>





	<!-- footer -->
	<?php include 'include/Footer.php'; ?>

	<!-- java script to match password -->
	<script>
	function checkPassMatch() {
    	var password = document.getElementById("psw").value;
    	var confirmPassword = document.getElementById("psw-repeat").value;

    	if (password === confirmPassword) {
        document.getElementById("msgerror").innerHTML = "";
        document.getElementById("msgok").innerHTML = "Passwords match!";
    	} else {
		document.getElementById("msgok").innerHTML = "";
        document.getElementById("msgerror").innerHTML = "Passwords do not match!";

    	}
	}

	</script>