## log in verification

log in details sent in from front end will be compared to data in database to make sure they are all correct. If they are they sign the user in and give them a cookie. Otherwise they get a message detailing the issue and allows them to try again.

## registration page

registration details are checked partly on front end then sent to back end for rest of checks. The email and username are checked to make sure neither are already in use and are valid. If all the tests pass the user is then saved to the player database

## security

the passwords are hashed using sha256 in the back end and stored that way. Further more all the fields are sanitised so they are safe from sql injections and cross site scripting attacks

## ease of access

Some measures are simply to make it easier for the user to use the website. The login field accepts both username or email and is secure for both.