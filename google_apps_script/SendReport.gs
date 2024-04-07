function sendEmailsWithSendGrid() {

  // Example business data obtained from your analysis
  const businesses = [
    { email: 'atitdp@gmail.com', name: "Shady River RV Park", callersEngaged: 10, newReservations: 25, modifyReservations: 2, reportduration: "2024-04-01 to 2024-04-08", currentyear: 2024 },
    //{ email: 'atit10_99@yahoo.com', name: 'Jus Passn Thru RV Park', callersEngaged: 8, newReservations: 4, modifyReservations: 3, reportduration: "2024-04-01 to 2024-04-08", currentyear: 2024  }
    // Add more businesses as needed
  ];

  // SendGrid API endpoint for sending emails
  const sendGridUrl = 'https://api.sendgrid.com/v3/mail/send';

  // Iterate over each business and send an email
  businesses.forEach((business) => {
    const emailBody = {
      personalizations: [
        {
          to: [{ email: business.email }],
          dynamic_template_data: {
            businessName: business.name,
            report_start_end_date: business.reportduration,
            callers_engaged: business.callersEngaged,
            new_reservations: business.newReservations, 
            modify_cancel: business.modifyReservations,
            current_year: business.currentyear,
          }
        }
      ],
      from: { 
        email: 'notification@rvspotminder.com', 
        name: 'RV Spotminder' //
      },
      template_id: templateId
    };

    const options = {
      method: 'post',
      headers: {
        'Authorization': 'Bearer ' + sendGridApiKey,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(emailBody),
      muteHttpExceptions: true // To prevent throwing exceptions for non-2xx responses
    };

    // Make the API request to SendGrid
    const response = UrlFetchApp.fetch(sendGridUrl, options);
    const responseCode = response.getResponseCode();
    
    if (responseCode === 202) {
      Logger.log(`Email successfully sent to ${business.email}`);
    } else {
      Logger.log(`Failed to send email to ${business.email}. Response code: ${responseCode}`);
    }
  });
}


