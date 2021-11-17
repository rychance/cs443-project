

var poolData = {
  UserPoolId: 'us-east-2_JqwTHCjLy',
  ClientId: '5dhh8r608bdv8up0r0edp3bdp1'
}


function signIn () {

var username = document.getElementById('username-field').value;
var password = document.getElementById('password-field').value;

var authenticationData = {
	Username: username,
	Password: password,
};

var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);
var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

var userData = {
	Username: username,
	Pool: userPool,
};
var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
cognitoUser.authenticateUser(authenticationDetails, {
	onSuccess: function(result) {
	window.location.href = "/index"

	},

	onFailure: function(err) {
		alert(err.message || JSON.stringify(err));
	},
});
}
