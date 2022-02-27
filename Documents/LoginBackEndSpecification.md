## log in verification

log in details sent in from front end will be compared to data in database to make sure they are all correct. If they are they sign the user in and give them a cookie. Otherwise they get a message detailing the issue and allows them to try again.

## registration page

registration details are checked partly on front end then sent to back end for rest of checks. The email and username are checked to make sure neither are already in use and are valid. If all the tests pass the user is then saved to the player database

## security

the passwords are hashed using sha256 in the back end and stored that way. Further more all the fields are sanitised so they are safe from sql injections and cross site scripting attacks

## ease of access

Some measures are simply to make it easier for the user to use the website. The login field accepts both username or email and is secure for both.

## auto log in

Cookies are made when new users are registered or log in. this cookie is then saved in the database and linked to each user. The cookie stays active for the duration of the session and will update every time they log in again to make sure there can only be 1 active user using the account at a time.

## admin privilages

Make a way to differentiate admins from users in the database. This data can be retrieved using only the unique cookie that each user has. Make it easy to only allow access to pages if the user has the admin role. All will be checked with cookies to make sure only 1 admin is using each admin account.