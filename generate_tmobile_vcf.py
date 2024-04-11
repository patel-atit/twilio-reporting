def generate_vcf(phone_number, business_name):
    # Open or create a VCF file to write the contacts
    with open(f"{business_name} Tmobile Fwd to RV Spotminder.vcf", "w") as vcf_file:
        vcf_file.write("BEGIN:VCARD\n")
        vcf_file.write("VERSION:3.0\n")
        vcf_file.write(f"N:{business_name} Tmobile Fwd to RV Spotminder;;;\n")
        vcf_file.write(f"FN:{business_name} Tmobile Fwd to RV Spotminder\n")
        
        # Define the format of the phone numbers
        phone_numbers = [
            {"type": "No Answer Fwd 15", "number": f"**61*{phone_number}**15#"},
            {"type": "Unreachable Call Fwd", "number": f"**62*{phone_number}#"},
            {"type": "Line Busy Fwd", "number": f"**67*{phone_number}#"},
            {"type": "All Fwd", "number": f"**21*{phone_number}#"}
        ]
        
        # Add each phone number to the contact
        for i, phone in enumerate(phone_numbers, start=1):
            vcf_file.write(f"TEL;TYPE=VOICE;TYPE=pref{i}:{phone['number']}\n")
        
        vcf_file.write("END:VCARD\n")
    
    print(f"VCF file '{business_name} Tmobile Fwd to RV Spotminder.vcf' has been created.")

# Taking user input for phone number and business name
user_phone_number = input("Enter the phone number for forwarding settings: ")
user_business_name = input("Enter the business name: ")

# Calling the function with user inputs
generate_vcf(user_phone_number, user_business_name)
