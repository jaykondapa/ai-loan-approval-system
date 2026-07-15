CHECKING_ACCOUNT_LABELS = {
    1: "No checking account",
    2: "Checking account balance below 0 DM",
    3: "Checking account balance from 0 to below 200 DM",
    4: "Checking account balance at least 200 DM or salary account for at least one year",
}

CREDIT_HISTORY_LABELS = {
    0: "Past delays in repayment",
    1: "Critical account or other credits elsewhere",
    2: "No previous credits or all previous credits paid back duly",
    3: "Existing credits paid back duly so far",
    4: "All credits at this bank paid back duly",
}

LOAN_PURPOSE_LABELS = {
    0: "Other",
    1: "New car",
    2: "Used car",
    3: "Furniture or equipment",
    4: "Radio or television",
    5: "Domestic appliances",
    6: "Repairs",
    7: "Education",
    8: "Vacation",
    9: "Retraining",
    10: "Business",
}

SAVINGS_ACCOUNT_LABELS = {
    1: "Unknown or no savings account",
    2: "Savings below 100 DM",
    3: "Savings from 100 to below 500 DM",
    4: "Savings from 500 to below 1,000 DM",
    5: "Savings at least 1,000 DM",
}

EMPLOYMENT_DURATION_LABELS = {
    1: "Unemployed",
    2: "Employed for less than 1 year",
    3: "Employed for 1 to below 4 years",
    4: "Employed for 4 to below 7 years",
    5: "Employed for at least 7 years",
}

INSTALLMENT_RATE_LABELS = {
    1: "Installment rate at least 35% of income",
    2: "Installment rate from 25% to below 35% of income",
    3: "Installment rate from 20% to below 25% of income",
    4: "Installment rate below 20% of income",
}

PERSONAL_STATUS_LABELS = {
    1: "Male, divorced or separated",
    2: "Female, non-single or male, single",
    3: "Male, married or widowed",
    4: "Female, single",
}

GUARANTOR_LABELS = {
    1: "No other debtor",
    2: "Co-applicant",
    3: "Guarantor",
}

RESIDENCE_DURATION_LABELS = {
    1: "Present residence for less than 1 year",
    2: "Present residence for 1 to below 4 years",
    3: "Present residence for 4 to below 7 years",
    4: "Present residence for at least 7 years",
}

PROPERTY_LABELS = {
    1: "Unknown or no property",
    2: "Car or other property",
    3: "Building society savings agreement or life insurance",
    4: "Real estate",
}

OTHER_INSTALLMENT_PLAN_LABELS = {
    1: "Other installment plan with a bank",
    2: "Other installment plan with stores",
    3: "No other installment plan",
}

HOUSING_LABELS = {
    1: "Living for free",
    2: "Renting",
    3: "Owns housing",
}

EXISTING_CREDIT_LABELS = {
    1: "One existing credit",
    2: "Two to three existing credits",
    3: "Four to five existing credits",
    4: "Six or more existing credits",
}

JOB_LABELS = {
    1: "Unemployed or unskilled non-resident",
    2: "Unskilled resident",
    3: "Skilled employee or official",
    4: "Manager, self-employed, or highly qualified employee",
}

DEPENDENTS_LABELS = {
    1: "Three or more people financially liable",
    2: "Zero to two people financially liable",
}

TELEPHONE_LABELS = {
    1: "No telephone",
    2: "Telephone registered under the customer name",
}

FOREIGN_WORKER_LABELS = {
    1: "Foreign worker",
    2: "Not a foreign worker",
}


def build_readable_application(application: dict) -> dict:
    return {
        "checking_account": CHECKING_ACCOUNT_LABELS[
            application["checking_account"]
        ],
        "loan_duration_months": application["loan_duration_months"],
        "credit_history": CREDIT_HISTORY_LABELS[
            application["credit_history"]
        ],
        "loan_purpose": LOAN_PURPOSE_LABELS[
            application["loan_purpose"]
        ],
        "loan_amount": application["loan_amount"],
        "savings_account": SAVINGS_ACCOUNT_LABELS[
            application["savings_account"]
        ],
        "employment_duration": EMPLOYMENT_DURATION_LABELS[
            application["employment_years"]
        ],
        "installment_rate": INSTALLMENT_RATE_LABELS[
            application["installment_rate_percent"]
        ],
        "personal_status": PERSONAL_STATUS_LABELS[
            application["personal_status"]
        ],
        "other_debtors": GUARANTOR_LABELS[
            application["guarantors"]
        ],
        "present_residence": RESIDENCE_DURATION_LABELS[
            application["years_at_residence"]
        ],
        "property": PROPERTY_LABELS[
            application["property_assets"]
        ],
        "age": application["age"],
        "other_installment_plans": OTHER_INSTALLMENT_PLAN_LABELS[
            application["other_installment_plans"]
        ],
        "housing": HOUSING_LABELS[
            application["housing_type"]
        ],
        "existing_credits": EXISTING_CREDIT_LABELS[
            application["existing_credit_count"]
        ],
        "job": JOB_LABELS[
            application["job"]
        ],
        "people_financially_liable": DEPENDENTS_LABELS[
            application["dependents"]
        ],
        "telephone": TELEPHONE_LABELS[
            application["telephone_available"]
        ],
        "foreign_worker": FOREIGN_WORKER_LABELS[
            application["foreign_worker"]
        ],
    }