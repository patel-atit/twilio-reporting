function getTwilioMessagesStatsPerPhoneNumberForPreviousWeek() {
  const baseUrl = `https://api.twilio.com/2010-04-01/Accounts/${accountSid}`;

  // Encode credentials for basic authentication
  const credentials = Utilities.base64Encode(accountSid + ':' + authToken);

  // Set up the request options for authentication
  const options = {
    method: 'get',
    headers: {
      Authorization: 'Basic ' + credentials,
    },
    muteHttpExceptions: true // To prevent the script from throwing exceptions for non-2xx responses
  };

  // Calculate dates for the previous week
  let now = new Date();
  let dayOfWeek = now.getDay(); // Day of week (0 for Sunday, 1 for Monday, etc.)
  let prevMonday = new Date(now);
  prevMonday.setDate(now.getDate() - dayOfWeek - 6); // Set to previous week's Monday
  let prevSunday = new Date(prevMonday);
  prevSunday.setDate(prevMonday.getDate() + 6); // Set to previous week's Sunday

  // Format dates for the API request
  const formatISODate = (date) => {
    return date.toISOString().split('T')[0] + 'T00:00:00Z'; // Format as YYYY-MM-DDT00:00:00Z
  };

  const dateSentAfter = encodeURIComponent(formatISODate(prevMonday)); // Start of the previous week
  const dateSentBefore = encodeURIComponent(formatISODate(prevSunday)); // End of the previous week

  // Fetch incoming phone numbers
  const phoneNumbersResponse = UrlFetchApp.fetch(`${baseUrl}/IncomingPhoneNumbers.json`, options);
  const phoneNumbersStatus = phoneNumbersResponse.getResponseCode();
  const phoneNumbersBody = phoneNumbersResponse.getContentText();

  if (phoneNumbersStatus === 200) {
    const phoneNumbersData = JSON.parse(phoneNumbersBody);

    // Iterate over each incoming phone number
    phoneNumbersData.incoming_phone_numbers.forEach((phoneNumber) => {
      Logger.log(`Phone Number: ${phoneNumber.phone_number} Starting Date[${dateSentAfter}], Ending Date[${dateSentBefore}]`);
      
      // Initialize message counts for each category
      let callersEngagedCount = 0;
      let newReservationCount = 0;
      let modifyReservationCount = 0;

      // Define patterns to match message categories
      const callersEngagedPattern = /Thank you for calling .*\. Please say Hi, and we will present options to gather additional details\./;
      const newReservationPattern = /We have passed your request to our team\. We will get back to you as soon as we can\. This text messaging experience is brought to you by https:\/\/rvspotminder\.com/;
      const modifyReservationPattern = /Do you want to modify or cancel\?\n1\. Modify\n2\. Cancel/;

      // Construct the initial URL for fetching messages
      let messagesUrl = `${baseUrl}/Messages.json?From=${encodeURIComponent(phoneNumber.phone_number)}&DateSent%3E=${dateSentAfter}&DateSent%3C=${dateSentBefore}`;

      // Loop to fetch all pages of messages
      do {
        const messagesResponse = UrlFetchApp.fetch(messagesUrl, options);
        const messagesData = JSON.parse(messagesResponse.getContentText());

        // Classify each message and update counts
        messagesData.messages.forEach(message => {
          if (callersEngagedPattern.test(message.body)) callersEngagedCount++;
          else if (newReservationPattern.test(message.body)) newReservationCount++;
          else if (modifyReservationPattern.test(message.body)) modifyReservationCount++;
        });

        // Prepare URL for next page, if any
        messagesUrl = messagesData.next_page_uri ? `https://api.twilio.com${messagesData.next_page_uri}` : null;

      } while (messagesUrl); // Continue if there's another page

      // Log stats for the current phone number
      Logger.log(`Stats for ${phoneNumber.phone_number}:`);
      Logger.log(`Callers Engaged: ${callersEngagedCount}`);
      Logger.log(`New Reservation: ${newReservationCount}`);
      Logger.log(`Modify Reservation: ${modifyReservationCount}`);
    });
  } else {
    Logger.log(`Failed to fetch phone numbers. Status code: ${phoneNumbersStatus}`);
  }
}
