
schema = {"category": "[category_name]"}

def generate_prompt(url, html_code, schema= schema):
    """Generates the prompt based on the URL and website content."""
    return f"""
    Categorize this website: {url} based on its content: \n```{html_code}\n```
    FROM ONE OF THE FOLLOWING CATEGORIES:

        --Cyberlockers: Websites offering online services for file storage and sharing.
        --Online adult entertainment: Websites providing sexually explicit content or pornography.
        --Online pharmacies: Websites selling prescription medications.
        --Firearms: Websites selling or providing access to firearms.
        --Charity: Non-profit organization websites that raise funds or offer services for a cause, often including donation options.
        --Cryptocurrency: Websites that accept digital currencies like Bitcoin as an alternative payment method.
        --Gambling: Websites facilitating gambling activities.
        --Marijuana-related businesses: Websites involved in marijuana or cannabis cultivation, production, distribution, or sales.
        --Massage parlors: Websites offering massage or spa services.
        --Telemarketing and Call centers: Websites providing telemarketing services or operating call centers.
        --Direct Sales: Businesses selling products directly to consumers, often through eCommerce or independent sales representatives.

    Please follow these guidelines:
        - Evaluate the website as a whole and assign the category that best reflects its main purpose.
        - If the website doesn't fit any of the listed categories, assign "Other."
        - If there is insufficient information or an error message, assign the category "Information Not Enough."
        - Ensure that a category is always assigned.

    Return the result in the following JSON serializable format: {schema}
    """
