# Week 3 — Decentralized Authentication

## Homework
- [x] Ashish's Week 3 - <a href="https://www.youtube.com/watch?v=tEJIeII66pY&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=39">Decentralized Authentication</a> 
- [ ] Chirag's Week 3 - Spending Considerations
- [x] Setup Cognito User Pool
- [x] Implement Custom Sign-in Page
- [x] Implement Custom Sign-up Page
- [x] Implement Custom Confirmation Page
- [x] Implement Custom Recovery Page
- [x] Watch about different approaches to verifying JWTs

## Homework Challenges
- [ ] Decouple the JWT verify from the application code by writing a Flask Middleware (medium)
- [ ] Decouple the JWT verify by implementing a Container Sidecar pattern using the official AWS aws-jwt-verify.js library (hard)
- [ ] Decouple the JWT verify process by using Envoy as a sidecar (hard)
  - https://www.envoyproxy.io/
- [ ] Implement an IdP login (Amazon, Facebook, Apple, or Google) (hard)
- [ ] Implement MFA that sends SMS (not, this has spend, investigate spend before considering, text messages are not eligible for AWS credits) (easy)
- [ ] Research how to create users with Cognito without temp password 
  - https://stackoverflow.com/questions/64720348/create-new-users-in-aws-cognito-without-a-temp-password-email
  - https://stackoverflow.com/questions/45666794/aws-cognito-user-pool-without-a-password
- [ ] Configure the confirmation page to automatically log the new user into their account
- [ ] Research how to restrict users from resetting their password to a previously used password
- [ ] Fix successful recovery page

# Cognito Security Best Practices
## Authentication
Security Assertion Markup Language (SAML): Uses one credential to log into any service.

OpenID Connect: Allows you to use your social credentials (LinkedIn, Facebook, Twitter, etc.) to authenticate using instead of setting up new credentials every single time you create an account.

## Authorization
OAuth2.0: 


## What is Decentralized Authentication?

## What is AWS Cognito
Service that allows authentication with users stored locally.
- Serves as a user directory with the context of AWS.

2 types of AWS Cognito:

### Cognito User pool
- Authenticates using OAuth
  - Get the trust relationship between social media sites and the app to offload the need for a username & password to be stored locally.
  - Users can directly log in and register themselves.
  - Only allows access to the app itself.

### Cognito Identity Pool
- Allows applications to request temporary credentials.
  - To allow users to have access to other AWS services.
  - Acts as an access broker.

## Why use Cognito?
- User Directory for Customers
- Ability to access AWS Resources for the app being built
- Identity Broker for AWS Resources with temporary credentials
- Can extend users to AWS Resources easily

## User Lifecycle Management
<img src="./assets/week3/user-lifecycle-management.jpg">

## Token Lifecycle Management
<img src="./assets/week3/token-lifecycle-management.jpg">

Tokens can be describe similarly as cookies, but they're different.
- Tokens are primarily used by API services and modern applications.
- Tokens are short-lived.
  - Create
  - Assign
  - Activate
  - Suspend
  - Remove
  - Expire

## Cognito Users

## Application Users

## AWS Cognito Security Best Practices
### User Best Practices
- AWS Services - API Gateway, AWS Resources shared with the App Client (backend or back channels)
- AWS WAF with Web ACLs for rate limiting, allow/deny list, deny access from regions & many other WAF management rules similar to OWASP
- AWS Cognito Compliance standard is what your business requires
- AWS Cognito should only be in the AWS region that you are legally allowed to be holding user data in (follow GRC frameworks; GDPR for example)
- AWS Organizations SCP - to manage user pool deletion, creation, region lock, etc.
- Enable AWS CloudTrail  & monitor to trigger alerts on malicious Cognito behavior by an identity in AWS

### Application Best Practices
- Applications should use industry standard for authentication & authorization (SAML, OpenID Connect, OAuth2.0, etc.)
- App User Lifecycle Management - Create, modify, delete users
- AWS User Access Lifecycle Management - Change of roles/revoke roles
- RBAC to manage how much access to AWS Resources for the app being built
- Token Lifecycle Management - Issue new tokens, revoke compromised tokens, storage location (client/server), etc.
- Security testing - penetration tests
- Access Token Scope - keep limited
- JWT Token best practice - no sensitive information
- Encryption in Transit for API Calls

# Setup AWS Cognito
## Create new user pool
- User pools to have login and sign up
- Federated identity providers would use a social identity from another identity provider

NOTE: Required attributes cannot be changed after creating the user pool.

- Log into the AWS Console
- Search for Cognito
- Click on Create user pool

<img src="./assets/week3/cognito-create-user-pool.jpg">

Since we're not using Federated identity providers, we will use the Cognito user pool.

- Select User name and email for sign-in options
- Allow users to sign in with a preferred user name

<img src="./assets/week3/cognito-password-policy.jpg">

- We're selecting a custom password for the security requirements as the default isn't extremely secure. I believe the default was set to 8 characters for the password length.
- After selecting Custom, enter in the minimum password length you want for your users to be required to use.

<img src="./assets/week3/cognito-mfa.jpg">

- To make sure we don't have additional expenses, we are skipping MFA.

<img src="./assets/week3/cognito-account-recovery.jpg">

- To make sure we don't have additional expenses, we will use email only for account recovery messages.
    - SMS incurs additional costs.

<img src="./assets/week3/cognito-signup-experience.jpg">

- We want to allow our users to have a self-service sign up page

<img src="./assets/week3/cognito-verification-confirmation.jpg">

- We want to allow Cognito to automatically send messages to verify & confirm. 
  - Attributes to verify: select Send email message, verify email address
- Verifying attribute changes: select Keep original attribute value active when an update is pending - Recommended
- Active attribute values when an update is pending: select Email address

<img src="./assets/week3/cognito-required-attributes.jpg">

- Required Attributes: 
  - Email
  - name
  - preferred_username

<img src="./assets/week3/cognito-message-delivery.jpg">

- Configure message delivery: Send email with Cognito


<img src="./assets/week3/cognito-integrate-app1.jpg">

- Name the user pool

<img src="./assets/week3/cognito-integrate-app2.jpg">

- App type: Public client
- Name the app client
- Client secret: Don't generate a client secret


## Install AWS Amplify Library
AWS Amplify will allow us to use Cognito

Documentation: https://docs.amplify.aws/lib/auth/getting-started/q/platform/js/

```sh
cd frontend-react-js
npm i aws-amplify --save
```

Adding this as a dependency.
Open `package.json` and we should see `"aws-amplify: ^5.0.16"`

## Provision Cognito User Group
Using the AWS Console we'll create a Cognito User Group

## Configure Amplify
We need to hook up our cognito pool to our code in the `App.js`

```js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```
Edited above Auth region to be 

```js
process.env.REACT_APP_AWS_PROJECT_REGION
```

# Conditionally show components based on logged in or logged out
Inside our `HomeFeedPage.js`

```js
import { Auth } from 'aws-amplify';
```


```js
// set a state
const [user, setUser] = React.useState(null);
```
^^ already in HomeFeedPage.js


Replace the checkAuth in HomeFeedPage.js (41-50)
```js
// check if we are authenticated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};
```


```js
// check when the page loads if we are authenticated
React.useEffect(()=>{
  loadData();
  checkAuth();
}, [])
```
^^ already in HomeFeedPage.js


## Pass user to the following components:

```js
<DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
<DesktopSidebar user={user} />
```

We'll rewrite `DesktopNavigation.js` so that it it conditionally shows links in the left hand column
on whether you are logged in or not.

Notice we are passing the user to ProfileInfo

```js
import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';
export default function DesktopNavigation(props) {
  let button;
  let profile;
  let notificationsLink;
  let messagesLink;
  let profileLink;
  if (props.user) {
    button = <CrudButton setPopped={props.setPopped} />;
    profile = <ProfileInfo user={props.user} />;
    notificationsLink = <DesktopNavigationLink 
      url="/notifications" 
      name="Notifications" 
      handle="notifications" 
      active={props.active} />;
    messagesLink = <DesktopNavigationLink 
      url="/messages"
      name="Messages"
      handle="messages" 
      active={props.active} />
    profileLink = <DesktopNavigationLink 
      url="/@andrewbrown" 
      name="Profile"
      handle="profile"
      active={props.active} />
  }
  return (
    <nav>
      <Logo className='logo' />
      <DesktopNavigationLink url="/" 
        name="Home"
        handle="home"
        active={props.active} />
      {notificationsLink}
      {messagesLink}
      {profileLink}
      <DesktopNavigationLink url="/#" 
        name="More" 
        handle="more"
        active={props.active} />
      {button}
      {profile}
    </nav>
  );
}
```

## Update `ProfileInfo.js`
Replace 
```js
import Cookies from 'js-cookie'
```

With the following:

```js
import { Auth } from 'aws-amplify';
```

Replace 
```js
  const signOut = async () => {
    console.log('signOut')
    // [TODO] Authenication
    Cookies.remove('user.logged_in')
    //Cookies.remove('user.name')
    //Cookies.remove('user.username')
    //Cookies.remove('user.email')
    //Cookies.remove('user.password')
    //Cookies.remove('user.confirmation_code')
    window.location.href = "/"
  }
```

With the following:

```js
const signOut = async () => {
  try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
  } catch (error) {
      console.log('error signing out: ', error);
  }
}
```

We'll rewrite `DesktopSidebar.js` so that it conditionally shows components in case you are logged in or not.

```js
import './DesktopSidebar.css';
import Search from '../components/Search';
import TrendingSection from '../components/TrendingsSection'
import SuggestedUsersSection from '../components/SuggestedUsersSection'
import JoinSection from '../components/JoinSection'
export default function DesktopSidebar(props) {
  const trendings = [
    {"hashtag": "100DaysOfCloud", "count": 2053 },
    {"hashtag": "CloudProject", "count": 8253 },
    {"hashtag": "AWS", "count": 9053 },
    {"hashtag": "FreeWillyReboot", "count": 7753 }
  ]
  const users = [
    {"display_name": "Andrew Brown", "handle": "andrewbrown"}
  ]
  let trending;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
  }
  let suggested;
  if (props.user) {
    suggested = <SuggestedUsersSection users={users} />
  }
  let join;
  if (props.user) {
  } else {
    join = <JoinSection />
  }
  return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="#">About</a>
        <a href="#">Terms of Service</a>
        <a href="#">Privacy Policy</a>
      </footer>
    </section>
  );
}
```

Tested app and the frontend resulted in a blank page.

<img src="./assets/week3/frontend-console-errors.jpg">

Made changes to `App.js` auth region
```js
process.env.REACT_APP_AWS_PROJECT_REGION
```
# Sign-in Page
Replace ```import Cookies from 'js-cookie'``` with the following:

```js
import { Auth } from 'aws-amplify';
```

```js
const [cognitoErrors, setCognitoErrors] = React.useState('');

const onsubmit = async (event) => {
  setErrors('')
  event.preventDefault();
  try {
    Auth.signIn(email, password)
      .then(user => {
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(err => { console.log('Error!', err) });
  } catch (error) {
    if (error.code == 'UserNotConfirmedException') {
      window.location.href = "/confirm"
    }
    setErrors(error.message)
  }
  return false
}

let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}
// just before submit component
{errors}
```

<img src="./assets/week3/sign-in-page.jpg">

Upon testing the sign-in page, no error displayed publicly. Edited the code to be what's shown below and the error displayed!

```js
  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
    .then(user => {
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => {
      if (error.code == 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    });
    return false
  }
```

<img src="./assets/week3/sign-in-page-error.jpg">

# Create User in AWS Cognito

- Go into AWS Cognito User pools
- Open the User pool we created from earlier

<img src="./assets/week3/cognito-create-user.jpg">

- Click Create user
- Select the Email checkbox
- Create a username
- Enter a valid email
- Set a password

<img src="./assets/week3/cognito-create-user-2.jpg">

- Click Create user

<img src="./assets/week3/created-user.jpg">

- Could not confirm user within AWS Cognito.
- Attempting to sign in with the newly created user account resulted in the following error

<img src="./assets/week3/null-access-token.jpg">

After reviewing the steps taken while creating a user in Cognito, I noticed we didn't select "Send an email invitation". This may be why we couldn't confirm the user account, and why no email was received after creating the account.

<img src="./assets/week3/recreate-user.jpg">

Recreated user with the checkbox selected and the email arrived in my inbox shortly after.
- The email that was received, however, presents a security issue. I will be adding this into my homework challenges to see how I can make this more secure.

After recreating the user in Cognito, the same error message appeared.

The line below appears to be part of the problem (in `app.js`)

```js
localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
```

AWS CLI should have a command that will help us confirm this user account.

```
aws
aws cognito-idp admin-set-user-password --username <username> --password <password> --user-pool-id <userpoolID> --permanent
```

<img src="./assets/week3/cruddur-active-user.jpg">

## Set Name and Handle
- Go into AWS Cognito User Pools
- Edit the user we created from earlier

<img src="./assets/week3/edit-user.jpg">

- The name section will be the display name
- The preferred_username will be the handle

<img src="./assets/week3/edit-display-and-handle.jpg">

- Save changes

<img src="./assets/week3/display-handle-updated.jpg">

# Sign-up Page
Replace `import Cookies from 'js-cookie'` with the following in `SignupPage.js`: 

```js
import { Auth } from 'aws-amplify';
```

Below is already included in the `SignupPage.js` code:
```js
const [cognitoErrors, setCognitoErrors] = React.useState('');
```

Replace const onsubmit with the following:

```js
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
            name: name,
            email: email,
            preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
            enabled: true,
        }
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
  return false
}
```

Replaced `setCognitoErrors` with `setErrors`

```js
let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}
//before submit component
{errors}
```

# Confirmation Page
Replace `import Cookies from 'js-cookie'` with the following in `ConfirmationPage.js`

```js
import { Auth } from 'aws-amplify';
```

Replace resend_code with the following:

```js
const resend_code = async (event) => {
  setErrors('')
  try {
    await Auth.resendSignUp(email);
    console.log('code resent successfully');
    setCodeSent(true)
  } catch (err) {
    // does not return a code
    // does cognito always return english
    // for this to be an okay match?
    console.log(err)
    if (err.message == 'Username cannot be empty'){
      setErrors("You need to provide an email in order to send Resend Activiation Code")   
    } else if (err.message == "Username/client id combination not found."){
      setErrors("Email is invalid or cannot be found.")   
    }
  }
}
```

Replaced `setCognitoErrors` with `setErrors`


Replace const onsubmit with the following:

```js
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    await Auth.confirmSignUp(email, code);
    window.location.href = "/"
  } catch (error) {
    setErrors(error.message)
  }
  return false
}
```

<img src="./assets/week3/signup-page-errors.jpg">

Hit an error after accidentally deleting 5 lines of code from `SignupPage.js`

<img src="./assets/week3/signup-page-email-format.jpg">

Recreating the Cognito User Pool should resolve this error as we have discovered that we accidentally selected both Username and Email during the setup.

<img src="./assets/week3/confirmation-page.jpg">

Successfully setup confirmation page and received the confirmation code via email.

<img src="./assets/week3/confirmation-page-url.jpg">

HW challenge idea: remove the user information from the URL and implement email field autofill

# Recovery Page
Add the following to `RecoverPage.js`

```js
import { Auth } from 'aws-amplify';
```

```js
const onsubmit_send_code = async (event) => {
  event.preventDefault();
  setErrors('')
  Auth.forgotPassword(username)
  .then((data) => setFormState('confirm_code') )
  .catch((err) => setErrors(err.message) );
  return false
}
```

```js
const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setErrors(err.message) );
  } else {
    setErrors('Passwords do not match')
  }
  return false
}
```

<img src="./assets/week3/recovery-page-reset.jpg">

<img src="./assets/week3/recovery-successful.jpg">

# Authenticating Server Side
Add in the `HomeFeedPage.js` a header to pass along the access token

```js
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  },
```

```js
request.headers.get('your-header-name')
```

<img src="./assets/week3/authenticate-backend-console-errors.jpg">

^^ Hit CORS error, needing to update CORS to resolve.
# 
Replace `cors` with the following in `app.py`

```js
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```

<img src="./assets/week3/cors-resolved.jpg">

# Ensure JWT Access Token is Properly Set
Add the following to /api/activities/home to ensure access token is being set

```py
  app.logger.debug("AUTH HEADER")
  app.logger.debug(
    request.headers.get('Authorization')
  )
```

<img src="./assets/week3/access-token-log.jpg">

# Add Dependency
In `requirements.txt` add the following:

Flask-AWSCognito

Install requirements:
```sh
cd backend-flask
pip install -r requirements.txt
```

# Set Env Vars
Add the following in `docker-compose.yml`
```yml
AWS_COGNITO_USER_POOL_ID: "cognito-user-pool-id"
AWS_COGNITO_USER_POOL_CLIENT_ID: "app-client-id"
```


Add the following to `app.py`
```py
from flask_awscognito import AWSCognitoAuthentication
```

Add the following to `app.py` after the @app

```py
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")

aws_auth = AWSCognitoAuthentication(app)
```

<img src="./assets/week3/flask-awscognito-error.jpg">


Add the following to `app.py` under /api/activities/home

```py
@aws_auth.authentication_required


claims = aws_auth.claims
```

<img src="./assets/week3/userpool-client-secret-error.jpg">

There's no user pool client secret to set because we're not using it.

- Client secrets are used by the server-side component of an app to authorize API requests. Using a client secret can prevent a third party from impersonating your client.

We are NOT authorizing API requests.


Remove the following: 
```py
from flask_awscognito import AWSCognitoAuthentication
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")

aws_auth = AWSCognitoAuthentication(app)

@aws_auth.authentication_required
```


# Create `cognito_token_verification.py`
Create a new folder called `lib` under `backend-flask`

This may not be needed, however, there is an error occurring that is preventing me from starting the backend-flask service in gitpod. 
Test changes, rewatch Week 3 Congito JWT Server side Verify Video and try again.

```py
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode

class FlaskAWSCognitoError(Exception):
  pass

class TokenVerifyError(Exception):
  pass

class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

  @classmethod
  def extract_access_token(request_headers):
      access_token = None
      # get header request
      auth_header = request_headers.get("Authorization")
      # split header request
      if auth_header and " " in auth_header:
          _, access_token = auth_header.split()
      return access_token

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims
        return claims
```


Add the following to `app.py`

```py
from lib.cognito_jwt_token import CognitoJwtToken

cognito_token_verification = CognitoJwtToken(
  user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
  user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
)



# place before calling data to allow it to know if the request is authenticated or not
    access_token = CognitoJwtToken.extract_access_token(request.headers)
    try:
      claims = cognito_jwt_token.token_service.verify(access_token)
    except TokenVerifyError as e:
      _ = request.data
      abort(make_response(jsonify(message=str(e)), 401))

    app.logger.debug('claims')
    app.logger.debug(claims)
```

<img src="./assets/week3/argument-error.jpg">

Takes 1 positional argument but 2 were given - regarding (request.headers).
- I need to look into this further to understand the issue but we resolved this by creating a different class.

<img src="./assets/week3/debug-unauthenticated.jpg">

After debugging, we received an error that we were unauthenticated.

<img src="./assets/week3/token-expired.jpg">

Upon debugging again, the token was displaying as expired. This required logging out and back in again.

<img src="./assets/week3/authenticated.jpg">

After logging back in, we were authenticated.

<img src="./assets/week3/signed-out-home-secret.jpg">


When signing out, the token is not getting cleared out. 

Created a "secret" post for authenticated users to see but upon signing out, the token is not getting cleared out. 

# Approaches to Verify JWTs
https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html

https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py

https://github.com/borisrozumnuk/cognitojwt

# Homework Summary
What did I accomplish?

- All required homework assignments, with the exception of Chirag's video. This was not available at the time of submitting homework via the student portal.

Were there any obstacles (did I overcome them)?

- Similar issues as what we experienced in the videos. Some that were different however they were due to forgetting to change the name of variables that other files were calling upon.

What were the homework challenges I attempted?

- This week, time did not permit for me to attempt the homework challenges. I do plan on coming back to each week when time permits and finishing them. 