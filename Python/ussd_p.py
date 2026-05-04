#!/usr/bin/env python3
"""
USSD Web Application
A web-based USSD simulator with Bootstrap and hacker-style theme
"""

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hacker_ussd_secret'

# Menu functions (unchanged)
def main_menu():
    return {
        "1": "Account Services",
        "2": "Airtime & Data",
        "3": "Banking Services",
        "4": "Customer Care",
        "5": "Settings"
    }

def account_services_menu():
    return {
        "1": "Check Balance",
        "2": "Transaction History",
        "3": "Account Details",
        "4": "Account Management"
    }

def airtime_data_menu():
    return {
        "1": "Buy Airtime",
        "2": "Buy Data Bundle",
        "3": "Check Balances",
        "4": "Transfer Services"
    }

def banking_services_menu():
    return {
        "1": "Money Transfer",
        "2": "Bill Payments",
        "3": "Airtime for Others",
        "4": "Bank Account Services"
    }

def customer_care_menu():
    return {
        "1": "Contact Information",
        "2": "Help & Support",
        "3": "Report Issues",
        "4": "Service Information"
    }

def settings_menu():
    return {
        "1": "Language Settings",
        "2": "Call Settings",
        "3": "Data Settings",
        "4": "Security Settings"
    }

def check_balance_menu():
    return {
        "1": "Main Account Balance",
        "2": "Data Balance",
        "3": "Airtime Balance",
        "4": "Bonus Balance"
    }

def buy_airtime_menu():
    return {
        "1": "Quick Top-up",
        "2": "Custom Amount",
        "3": "Airtime Plans",
        "4": "Auto Top-up"
    }

def buy_data_menu():
    return {
        "1": "Daily Bundles",
        "2": "Weekly Bundles",
        "3": "Monthly Bundles",
        "4": "Unlimited Plans"
    }

def money_transfer_menu():
    return {
        "1": "Transfer to Mobile",
        "2": "Transfer to Bank",
        "3": "Transfer to Wallet",
        "4": "International Transfer"
    }

def contact_info_menu():
    return {
        "1": "Customer Care Numbers",
        "2": "Emergency Contacts",
        "3": "Email Support",
        "4": "Social Media"
    }

def help_support_menu():
    return {
        "1": "FAQs",
        "2": "Tutorials",
        "3": "Live Chat",
        "4": "Video Guides"
    }

def daily_bundles_menu():
    return {
        "1": "100MB - $1 (24hrs)",
        "2": "500MB - $3 (24hrs)",
        "3": "1GB - $5 (24hrs)",
        "4": "2GB - $8 (24hrs)"
    }

def weekly_bundles_menu():
    return {
        "1": "1GB - $5 (7 days)",
        "2": "3GB - $12 (7 days)",
        "3": "7GB - $25 (7 days)",
        "4": "15GB - $45 (7 days)"
    }

def monthly_bundles_menu():
    return {
        "1": "5GB - $20 (30 days)",
        "2": "15GB - $45 (30 days)",
        "3": "30GB - $80 (30 days)",
        "4": "50GB - $120 (30 days)"
    }

def unlimited_plans_menu():
    return {
        "1": "Unlimited 1GB - $10 (24hrs)",
        "2": "Unlimited 3GB - $25 (7 days)",
        "3": "Unlimited 10GB - $50 (30 days)",
        "4": "Unlimited 30GB - $100 (30 days)"
    }

def transfer_to_mobile_menu():
    return {
        "1": "Same Network",
        "2": "Other Networks",
        "3": "International",
        "4": "Recent Recipients"
    }

def transfer_to_bank_menu():
    return {
        "1": "Local Banks",
        "2": "International Banks",
        "3": "Saved Accounts",
        "4": "New Account"
    }

def language_settings_menu():
    return {
        "1": "English",
        "2": "French",
        "3": "Arabic",
        "4": "Portuguese"
    }

# Action handlers
def handle_balance_inquiry(balance_type):
    balances = {
        "1": ("Main Account", "$25.50"),
        "2": ("Data", "2.5GB"),
        "3": ("Airtime", "$15.00"),
        "4": ("Bonus", "$5.00")
    }
    if balance_type in balances:
        name, amount = balances[balance_type]
        return f"Your {name.lower()} balance is: {amount}"
    return "Invalid balance type"

def handle_data_purchase(bundle_type):
    bundle_menus = {
        "1": daily_bundles_menu(),
        "2": weekly_bundles_menu(),
        "3": monthly_bundles_menu(),
        "4": unlimited_plans_menu()
    }
    if bundle_type in bundle_menus:
        return bundle_menus[bundle_type]
    return {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ussd_code = request.form.get('ussd_code')
        valid_codes = ["*123#", "*124#", "*125#", "*126#"]
        if ussd_code in valid_codes:
            session['menu_stack'] = []
            session['current_menu'] = main_menu()
            session['menu_title'] = "Main Menu"
            return redirect(url_for('ussd'))
        else:
            return render_template('index.html', error="Invalid USSD code")
    return render_template('index.html')

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    if 'current_menu' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '0':
            if session['menu_stack']:
                prev = session['menu_stack'].pop()
                session['current_menu'] = prev['menu']
                session['menu_title'] = prev['title']
            else:
                session.clear()
                return redirect(url_for('index'))
        elif choice in session['current_menu']:
            # Navigate deeper
            session['menu_stack'].append({
                'menu': session['current_menu'],
                'title': session['menu_title']
            })

            # Determine next menu based on current path
            path = [item['title'] for item in session['menu_stack']] + [session['menu_title']]
            if session['menu_title'] == "Main Menu":
                if choice == "1":
                    session['current_menu'] = account_services_menu()
                    session['menu_title'] = "Account Services"
                elif choice == "2":
                    session['current_menu'] = airtime_data_menu()
                    session['menu_title'] = "Airtime & Data"
                # Add more main menu options
            elif session['menu_title'] == "Account Services" and choice == "1":
                session['current_menu'] = check_balance_menu()
                session['menu_title'] = "Check Balance"
            elif session['menu_title'] == "Airtime & Data" and choice == "2":
                session['current_menu'] = buy_data_menu()
                session['menu_title'] = "Buy Data Bundle"
            elif session['menu_title'] == "Buy Data Bundle":
                bundles = handle_data_purchase(choice)
                if bundles:
                    session['current_menu'] = bundles
                    session['menu_title'] = "Select Bundle"
                else:
                    session['menu_stack'].pop()
            elif session['menu_title'] == "Select Bundle":
                return render_template('ussd.html', menu=session['current_menu'], title=session['menu_title'], message=f"Bundle '{session['current_menu'][choice]}' purchased successfully!")
            # Add more navigation logic
            else:
                # Default back
                session['menu_stack'].pop()
        else:
            return render_template('ussd.html', menu=session['current_menu'], title=session['menu_title'], error="Invalid option")

    return render_template('ussd.html', menu=session['current_menu'], title=session['menu_title'])

if __name__ == '__main__':
    app.run(debug=True)
#         "4": "Bonus Balance"
#     }

# def buy_airtime_menu():
#     """Buy airtime submenu"""
#     return {
#         "1": "Quick Top-up",
#         "2": "Custom Amount",
#         "3": "Airtime Plans",
#         "4": "Auto Top-up"
#     }

# def buy_data_menu():
#     """Buy data bundle submenu"""
#     return {
#         "1": "Daily Bundles",
#         "2": "Weekly Bundles",
#         "3": "Monthly Bundles",
#         "4": "Unlimited Plans"
#     }

# def money_transfer_menu():
#     """Money transfer submenu"""
#     return {
#         "1": "Transfer to Mobile",
#         "2": "Transfer to Bank",
#         "3": "Transfer to Wallet",
#         "4": "International Transfer"
#     }

# def language_settings_menu():
#     """Language settings submenu"""
#     return {
#         "1": "English",
#         "2": "French",
#         "3": "Arabic",
#         "4": "Portuguese"
#     }

# # Level 4 menus (final actions)
# def daily_bundles_menu():
#     """Daily data bundles"""
#     return {
#         "1": "100MB - $1 (24hrs)",
#         "2": "500MB - $3 (24hrs)",
#         "3": "1GB - $5 (24hrs)",
#         "4": "2GB - $8 (24hrs)"
#     }

# def weekly_bundles_menu():
#     """Weekly data bundles"""
#     return {
#         "1": "1GB - $5 (7 days)",
#         "2": "3GB - $12 (7 days)",
#         "3": "7GB - $25 (7 days)",
#         "4": "15GB - $45 (7 days)"
#     }

# def monthly_bundles_menu():
#     """Monthly data bundles"""
#     return {
#         "1": "5GB - $20 (30 days)",
#         "2": "15GB - $45 (30 days)",
#         "3": "30GB - $80 (30 days)",
#         "4": "50GB - $120 (30 days)"
#     }

# def unlimited_plans_menu():
#     """Unlimited data plans"""
#     return {
#         "1": "Unlimited 1GB - $10 (24hrs)",
#         "2": "Unlimited 3GB - $25 (7 days)",
#         "3": "Unlimited 10GB - $50 (30 days)",
#         "4": "Unlimited 30GB - $100 (30 days)"
#     }

# def transfer_to_mobile_menu():
#     """Transfer to mobile options"""
#     return {
#         "1": "Same Network",
#         "2": "Other Networks",
#         "3": "International",
#         "4": "Recent Recipients"
#     }

# def transfer_to_bank_menu():
#     """Transfer to bank options"""
#     return {
#         "1": "Local Banks",
#         "2": "International Banks",
#         "3": "Saved Accounts",
#         "4": "New Account"
#     }

# def contact_info_menu():
#     """Contact information submenu"""
#     return {
#         "1": "Customer Care Numbers",
#         "2": "Emergency Contacts",
#         "3": "Email Support",
#         "4": "Social Media"
#     }

# def help_support_menu():
#     """Help and support submenu"""
#     return {
#         "1": "FAQs",
#         "2": "Tutorials",
#         "3": "Live Chat",
#         "4": "Video Guides"
#     }
#         "3": "Report Issue",
#         "4": "Service Centers",
#         "5": "Network Coverage"
#     }

# # # Handler functions for final actions
# # def handle_balance_inquiry(balance_type):
# #     """Handle balance inquiry"""
# #     balances = {
# #         "1": ("Main Account", "$25.50"),
# #         "2": ("Data", "2.5GB"),
# #         "3": ("Airtime", "$15.00"),
# #         "4": ("Bonus", "$5.00")
# #     }
# #     if balance_type in balances:
# #         name, amount = balances[balance_type]
# #         print(f"\n{name} Balance")
# #         print("=" * (len(name) + 8))
# #         print(f"Your {name.lower()} balance is: {amount}")
# #         if "GB" in amount:
# #             print("Valid until: 2026-12-31")
# #         input("Press Enter to continue...")

# # def handle_airtime_purchase(plan_type):
# #     """Handle airtime purchase"""
# #     plans = {
# #         "1": ("Quick Top-up", ["$5", "$10", "$25", "$50"]),
# #         "2": ("Custom Amount", "custom"),
# #         "3": ("Airtime Plans", ["$20/month", "$50/month", "$100/month"]),
# #         "4": ("Auto Top-up", ["Enable", "Disable", "Settings"])
# #     }
    
# #     if plan_type == "2":
# #         amount = input("Enter custom amount: ").strip()
# #         if amount.isdigit() and int(amount) > 0:
# #             print(f"Airtime of ${amount} purchased successfully!")
# #         else:
# #             print("Invalid amount.")
# #     elif plan_type in plans:
# #         name, options = plans[plan_type]
# #         print(f"\n{name}")
# #         print("=" * len(name))
# #         for i, option in enumerate(options, 1):
# #             print(f"{i}. {option}")
# #         choice = input("Choose option: ").strip()
# #         if choice.isdigit() and 1 <= int(choice) <= len(options):
# #             print(f"{options[int(choice)-1]} selected successfully!")
# #         else:
# #             print("Invalid choice.")
# #     input("Press Enter to continue...")

# # def handle_data_purchase(bundle_type):
# #     """Handle data bundle purchase"""
# #     bundle_menus = {
# #         "1": daily_bundles_menu(),
# #         "2": weekly_bundles_menu(),
# #         "3": monthly_bundles_menu(),
# #         "4": unlimited_plans_menu()
# #     }
    
# #     if bundle_type in bundle_menus:
# #         choice = display_menu("Select Bundle", bundle_menus[bundle_type])
# #         if choice in bundle_menus[bundle_type]:
# #             print(f"Bundle '{bundle_menus[bundle_type][choice]}' purchased successfully!")
# #         else:
# #             print("Invalid choice.")
# #     input("Press Enter to continue...")

# # def handle_money_transfer(transfer_type):
# #     """Handle money transfer"""
# #     if transfer_type == "1":  # Same network
# #         recipient = input("Enter recipient's number: ").strip()
# #         amount = input("Enter amount: ").strip()
# #         if recipient and amount.isdigit():
# #             print(f"Transfer of ${amount} to {recipient} successful!")
# #     elif transfer_type == "2":  # Other networks
# #         network = input("Select network (1.Vodafone 2.Airtel 3.Tigo): ").strip()
# #         recipient = input("Enter recipient's number: ").strip()
# #         amount = input("Enter amount: ").strip()
# #         if network and recipient and amount.isdigit():
# #             print(f"Transfer of ${amount} to {recipient} successful!")
# #     elif transfer_type == "3":  # International
# #         country = input("Enter country code: ").strip()
# #         recipient = input("Enter recipient's number: ").strip()
# #         amount = input("Enter amount: ").strip()
# #         if country and recipient and amount.isdigit():
# #             print(f"International transfer of ${amount} to +{country}{recipient} successful!")
# #     elif transfer_type == "4":  # Recent recipients
# #         print("Recent recipients:")
# #         print("1. 0241234567 - John Doe")
# #         print("2. 0279876543 - Jane Smith")
# #         choice = input("Select recipient: ").strip()
# #         if choice in ["1", "2"]:
# #             amount = input("Enter amount: ").strip()
# #             if amount.isdigit():
# #                 print(f"Transfer successful!")
# #     input("Press Enter to continue...")

# # def handle_contact_info(info_type):
# #     """Handle contact information"""
# #     contacts = {
# #         "1": ("Customer Care", "0800-123-4567"),
# #         "2": ("Emergency", "112"),
# #         "3": ("Email", "support@mtnafrica.com"),
# #         "4": ("Social Media", "@MTNAfrica")
# #     }
# #     if info_type in contacts:
# #         name, contact = contacts[info_type]
# #         print(f"\n{name}")
# #         print("=" * len(name))
# #         print(f"{contact}")
# #     input("Press Enter to continue...")

# # def handle_help_support(support_type):
# #     """Handle help and support"""
# #     if support_type == "1":  # FAQs
# #         print("\nFrequently Asked Questions")
# #         print("1. How to check balance?")
# #         print("2. How to buy data?")
# #         print("3. How to transfer money?")
# #         faq_choice = input("Choose FAQ: ").strip()
# #         answers = {
# #             "1": "Dial *123# and select Account Services > Check Balance",
# #             "2": "Dial *123# and select Airtime & Data > Buy Data Bundle",
# #             "3": "Dial *123# and select Banking Services > Money Transfer"
# #         }
# #         if faq_choice in answers:
# #             print(answers[faq_choice])
# #     elif support_type == "2":  # Tutorials
# #         print("Tutorials available:")
# #         print("1. Getting Started")
# #         print("2. Advanced Features")
# #         print("3. Troubleshooting")
# #     elif support_type == "3":  # Live Chat
# #         print("Connecting to live chat...")
# #         print("Chat support available 24/7")
# #     elif support_type == "4":  # Video Guides
# #         print("Video guides:")
# #         print("1. Balance Check Tutorial")
# #         print("2. Data Purchase Guide")
# #         print("3. Money Transfer Walkthrough")
# #     input("Press Enter to continue...")

# # def ussd_app():
# #     """Main USSD application loop with 4-layer navigation"""
# #     menu_stack = []  # Stack to track navigation path
    
# #     while True:
# #         if not menu_stack:
# #             # Main menu
# #             choice = display_menu("Main Menu", main_menu())
# #             if choice == "0":
# #                 print("Thank you for using MTN service. Goodbye!")
# #                 break
# #             elif choice in main_menu():
# #                 menu_stack.append(("main", choice))
# #             else:
# #                 print("Invalid option. Please try again.")
        
# #         elif len(menu_stack) == 1:
# #             # Level 2 menus
# #             current_menu = menu_stack[-1][1]
# #             if current_menu == "1":  # Account Services
# #                 choice = display_menu("Account Services", account_services_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in account_services_menu():
# #                     menu_stack.append(("account", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif current_menu == "2":  # Airtime & Data
# #                 choice = display_menu("Airtime & Data", airtime_data_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in airtime_data_menu():
# #                     menu_stack.append(("airtime", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif current_menu == "3":  # Banking Services
# #                 choice = display_menu("Banking Services", banking_services_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in banking_services_menu():
# #                     menu_stack.append(("banking", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif current_menu == "4":  # Customer Care
# #                 choice = display_menu("Customer Care", customer_care_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in customer_care_menu():
# #                     menu_stack.append(("care", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif current_menu == "5":  # Settings
# #                 choice = display_menu("Settings", settings_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in settings_menu():
# #                     menu_stack.append(("settings", choice))
# #                 else:
# #                     print("Invalid option.")
        
# #         elif len(menu_stack) == 2:
# #             # Level 3 menus
# #             menu_type, menu_choice = menu_stack[-1]
# #             if menu_type == "account" and menu_choice == "1":  # Check Balance
# #                 choice = display_menu("Check Balance", check_balance_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in check_balance_menu():
# #                     handle_balance_inquiry(choice)
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "airtime" and menu_choice == "1":  # Buy Airtime
# #                 choice = display_menu("Buy Airtime", buy_airtime_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in buy_airtime_menu():
# #                     handle_airtime_purchase(choice)
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "airtime" and menu_choice == "2":  # Buy Data
# #                 choice = display_menu("Buy Data Bundle", buy_data_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in buy_data_menu():
# #                     menu_stack.append(("data", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "banking" and menu_choice == "1":  # Money Transfer
# #                 choice = display_menu("Money Transfer", money_transfer_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in money_transfer_menu():
# #                     menu_stack.append(("transfer", choice))
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "care" and menu_choice == "1":  # Contact Info
# #                 choice = display_menu("Contact Information", contact_info_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in contact_info_menu():
# #                     handle_contact_info(choice)
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "care" and menu_choice == "2":  # Help & Support
# #                 choice = display_menu("Help & Support", help_support_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in help_support_menu():
# #                     handle_help_support(choice)
# #                 else:
# #                     print("Invalid option.")
# #             elif menu_type == "settings" and menu_choice == "1":  # Language Settings
# #                 choice = display_menu("Language Settings", language_settings_menu())
# #                 if choice == "0":
# #                     menu_stack.pop()
# #                 elif choice in language_settings_menu():
# #                     languages = {"1": "English", "2": "French", "3": "Arabic", "4": "Portuguese"}
# #                     if choice in languages:
# #                         print(f"Language changed to {languages[choice]}.")
# #                     input("Press Enter to continue...")
# #                 else:
# #                     print("Invalid option.")
# #             else:
# #                 # Handle other level 3 menus with simple actions
# #                 print(f"Option {menu_choice} selected in {menu_type}")
# #                 input("Press Enter to continue...")
# #                 menu_stack.pop()
        
# #         elif len(menu_stack) == 3:
# #             # Level 4 menus (final actions)
# #             menu_type, menu_choice, sub_choice = menu_stack[-1]
# #             if menu_type == "data":
# #                 handle_data_purchase(menu_choice)
# #                 menu_stack.pop()  # Go back to level 3
# #             elif menu_type == "transfer":
# #                 handle_money_transfer(menu_choice)
# #                 menu_stack.pop()  # Go back to level 3
# #             else:
# #                 print("Action completed.")
# #                 input("Press Enter to continue...")
# #                 menu_stack.pop()

# # if __name__ == "__main__":
# #     print("Welcome to MTN USSD Service")
# #     print("==========================")
# #     if check_ussd_code():
# #         ussd_app()


# ...existing code...

def main_menu():
    """Main menu (Layer 1)"""
    return {
        "1": "Balance Inquiry",
        "2": "Transfer Money", 
        "3": "Contact Info",
        "4": "Help & Support"
    }

def balance_inquiry_menu():
    """Balance inquiry submenu (Layer 2)"""
    return {
        "1": "Main Account",
        "2": "Data Balance",
        "3": "Airtime Balance",
        "4": "Bonus Balance"
    }

def transfer_menu():
    """Transfer submenu (Layer 2)"""
    return {
        "1": "To Mobile",
        "2": "To Bank",
        "3": "To Wallet",
        "4": "History"
    }

def mobile_transfer_menu():
    """Mobile transfer submenu (Layer 3)"""
    return {
        "1": "Enter Number",
        "2": "Recent Contacts",
        "3": "Favorites",
        "4": "Back"
    }

def recent_contacts_menu():
    """Recent contacts submenu (Layer 4)"""
    return {
        "1": "Contact 1",
        "2": "Contact 2", 
        "3": "Contact 3",
        "4": "Back"
    }

def bank_transfer_menu():
    """Bank transfer submenu (Layer 3)"""
    return {
        "1": "Enter Account",
        "2": "Saved Banks",
        "3": "Back"
    }

# ...existing code... (contact_info_menu, help_support_menu, etc.)

def run_ussd():
    """Simulate USSD navigation without functions in menus"""
    menu_stack = []  # Track menu path as list of (menu_name, choice)
    current_menu = main_menu()
    menu_name = "main"
    
    while True:
        print(f"\n{menu_name.replace('_', ' ').title()}")
        for key, value in current_menu.items():
            print(f"{key}. {value}")
        print("0. Exit")
        
        choice = input("Choose an option: ").strip()
        if choice == "0":
            break
        elif choice in current_menu:
            if choice == "4" and menu_name != "main":  # Back option
                if menu_stack:
                    menu_name, current_menu = menu_stack.pop()
                continue
            
            # Handle actions based on menu path
            if menu_name == "main":
                if choice == "1":
                    menu_stack.append((menu_name, current_menu))
                    current_menu = balance_inquiry_menu()
                    menu_name = "balance_inquiry"
                elif choice == "2":
                    menu_stack.append((menu_name, current_menu))
                    current_menu = transfer_menu()
                    menu_name = "transfer"
                # Add similar for other main options
            elif menu_name == "balance_inquiry":
                if choice == "1":
                    print("Balance: $25.50")
                    input("Press Enter...")
                # Add for other balance options
            elif menu_name == "transfer":
                if choice == "1":
                    menu_stack.append((menu_name, current_menu))
                    current_menu = mobile_transfer_menu()
                    menu_name = "mobile_transfer"
                # Add for other transfer options
            elif menu_name == "mobile_transfer":
                if choice == "2":
                    menu_stack.append((menu_name, current_menu))
                    current_menu = recent_contacts_menu()
                    menu_name = "recent_contacts"
                # Add for other mobile options
            elif menu_name == "recent_contacts":
                if choice == "1":
                    print("Transferred to Contact 1")
                    input("Press Enter...")
                # Add for other contacts
            # Add more elif blocks for other menus
        else:
            print("Invalid option")

# Run the USSD simulation
if __name__ == "__main__":
    run_ussd()




