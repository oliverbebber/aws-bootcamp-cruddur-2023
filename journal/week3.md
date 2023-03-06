# Week 3 — Decentralized Authentication

## Homework
- [x] Ashish's Week 3 - <a href="https://www.youtube.com/watch?v=tEJIeII66pY&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=39">Decentralized Authentication</a> 
- [ ] Chirag's Week 3 - Spending Considerations
- [ ] Setup Cognito User Pool
- [ ] Implement Custom Signin Page
- [ ] Implement Custom Signup Page
- [ ] Implement Custom Confirmation Page
- [ ] Implement Custom Recovery Page
- [ ] Watch about different approaches to verifying JWTs

## Homework Challenges
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 


# Setup AWS Cognito
## Create new user pool
- User pools to have login and sign up
- Federated identity providers would use a social identity from another identity provider

NOTE: Required attributes cannot be changed after creating the user pool.

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
  "AWS_PROJECT_REGION": process.env.REACT_AWS_PROJECT_REGION,
  "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```
