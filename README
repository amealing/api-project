# Companies House API layered with email

My first project in python! 

This project allows non-coders (perhaps a financial analyst) to query
the Companies House API for company profile data and insolvency history.
The user sends a textfile containing a list of company identification
numbers to a designated gmail address. The script will check this gmail
for new requests, use the attached data to make the API query and then
return the results (as an attachment) via email back to the user.

The trickiest part of the project was handling incoming emails. This
involved:
- Checking if the user was a permitted user
- Verifying that the email contained an attachment
- Checking if the attachment was formatted correctly (1 column only)
- Handling multiple attachments (and returning multiple attachments)
- Acknowledging receipt of the email by replying with a confirmation email
- Communicating with the user if there were any issues with the request
- Handling errors from the API (which occasionally returned a timeout)

Overall, a tough but really fun experience. This project was really
fulfilling to complete because it feels like something genuinely useful.
