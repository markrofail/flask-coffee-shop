// import * as env from 'env-var';

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'markrofail.eu', // the auth0 domain prefix
    audience: 'coffee-shop-api', // the audience set for the auth0 app
    clientId: '6u0apLVKIEMcPh0XBtWQWQPHfA84wLI0', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
