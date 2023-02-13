# Week 0 — Billing and Architecture
## Homework
- Destroy your root account credentials, Set MFA, IAM role
- Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
- Review all the questions of each pillars in the Well Architected Tool (No specialized lens)
- Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts
- Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility. 
- Open a support ticket and request a service limit


# Architectural Diagram
## Conceptual Diagram
<img src="./assets/week0/cruddur-conceptual-diagram.jpg">

## Logical Architectural Diagram
<img src="./assets/week0/cruddur-architectural-diagram.jpg">


# Create an admin user with MFA & IAM Roles
## Create admin user + admin user group
Once logged into the AWS console, search IAM to locate the service and click to manage access to AWS resources. (https://console.aws.amazon.com/iam/)

<img src="./assets/week0/search-iam-service.jpg">

From this page, you will see the IAM dashboard which informs you if the Root user has MFA enabled, if any access keys are active, and if you need to update access permissions for AWS Billing, Cost Management, and Account consoles.

You will also be able to manage users, groups, and roles from the IAM dashboard.

<img src="./assets/week0/aws-iam-dashboard.jpg">

On the left-hand side, click Users > Add Users to add a new user.

<img src="./assets/week0/aws-add-users.jpg">

From the next page, we will enter a username, select the Enable console access checkbox (to allow the user to sign in to the AWS Mangement Console), and generate a password before clicking Next to move on to configuring user permissions.

<img src="./assets/week0/aws-specify-user-details.jpg">

We want to create this new user with Admin permissions so we will need to make a new User Group (IAM) with the permissions.

Click Create group. 
- Create a User group name; ex: Administrators.
- Select AdministratorAccess (should be the first option in the Permission policies list).
- Scroll to the bottom of the list and click Create user group.
- Click Next.

<img src="./assets/week0/aws-create-user-group-adminaccess.jpg">

Review the user details to confirm the details are correct, then click Create user.

<img src="./assets/week0/aws-review-create.jpg">

On the next page, you can view & download the user's password or email the users instructions for signing in to the AWS Management Console. 

<img src="./assets/week0/aws-retrieve-password.jpg">

NOTE: You may need to add the user to the new User group you created before the user will be assigned the appropriate permissions. I ran into an issue after signing into the newly created admin account where I saw an error "You don't have permissions" when attempting to setup MFA. When I viewed the user group "Administrators" my user was not assigned for some reason. Assigning the user account to the group resolved the issue.

## Sign into admin user account to enable MFA & access keys
<a href="https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fus-east-2.console.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26region%3Dus-east-2%26state%3DhashArgsFromTB_us-east-2_50d727ee5bfe22a4&client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&forceMobileApp=0&code_challenge=XMwIMrRc4e00A59znlo2b66caHJ6TlAn0XmWTrPrYGI&code_challenge_method=SHA-256">AWS Signin Page</a>

Select IAM user

<img src="./assets/week0/aws-signin-iam-user.jpg">

- Enter the 12 digit Account ID
- Click Next

<img src="./assets/week0/aws-iam-signin.jpg">

- Enter the username & password.
- Click Sign in
- Enter in current/old password
- Enter in a new password
- Confirm new password
- Click Confirm password change

<img src="./assets/week0/aws-change-password.jpg">

Once we have signed in, we will setup MFA by navigating to Security Credentials. You can access this by clicking on your username in the upper-right hand corner, then clicking on Security credentials.

<img src="./assets/week0/aws-user-dropdown.jpg">

From the next page "My security credentials", click Assign MFA. 

<img src="./assets/week0/aws-assign-mfa.jpg">

Specify the MFA device name, then choose an MFA device before clicking Next.

<img src="./assets/week0/aws-mfa-device.jpg">

On the Set up device page, you will set up your authenticator app. 
- Install a compatible app like Google Authenticator, Duo Mobile, or Authy on your phone or computer. 
- Click on Show QR code; open your authenticator app then scan the code
- Fill in 2 consecutive codes from the MFA device
- Click Add MFA

<img src="./assets/week0/aws-setup-mfa-device.jpg">

On the next page you will see the banner below confirming the MFA device was successfully assigned! 

<img src="./assets/week0/aws-mfa-assigned.png">