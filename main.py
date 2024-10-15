import os
import pyperclip
from colorama import init, Fore, Style

# Initialize colorama
init()

def generate_sql(old_domain, new_domain):
    # Remove trailing slashes if present
    old_domain = old_domain.rstrip('/')
    new_domain = new_domain.rstrip('/')

    sql_template = f"""
-- Update WordPress domain references from {old_domain} to {new_domain}

-- Update site URL and home URL
UPDATE wp_options
SET option_value = replace(option_value, '{old_domain}', '{new_domain}')
WHERE option_name IN ('siteurl', 'home');

-- Update guid in wp_posts
UPDATE wp_posts
SET guid = REPLACE (guid, '{old_domain}', '{new_domain}');

-- Update post content
UPDATE wp_posts
SET post_content = REPLACE (post_content, '{old_domain}', '{new_domain}');

-- Update postmeta
UPDATE wp_postmeta
SET meta_value = REPLACE (meta_value, '{old_domain}', '{new_domain}')
WHERE meta_key NOT LIKE '\_%';

-- Update serialized data in wp_options
UPDATE wp_options
SET option_value = REPLACE(
    REPLACE(
        option_value,
        CONCAT('s:', LENGTH('{old_domain}'), ':\"{old_domain}\"'),
        CONCAT('s:', LENGTH('{new_domain}'), ':\"{new_domain}\"')
    ),
    CONCAT('s:', LENGTH('{old_domain}/'), ':\"{old_domain}/\"'),
    CONCAT('s:', LENGTH('{new_domain}/'), ':\"{new_domain}/\"')
);

-- Update non-serialized data in wp_options
UPDATE wp_options
SET option_value = REPLACE(option_value, '{old_domain}', '{new_domain}')
WHERE option_name NOT IN ('siteurl', 'home');

-- IMPORTANT: Go into /wp-admin and manually go to the site's dashboard Settings > General and re-save it.
-- Even if the correct domain shows in the site URL fields, CLICK TO UPDATE/SAVE as this forces the cache to reset.
    """
    return sql_template

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print("WordPress Domain Update SQL Generator")
    print("="*50 + "\n")

    print(Fore.RED + "WARNING: Always backup your database before running any SQL operations!" + Style.RESET_ALL)
    print()

    old_domain = input("Enter the old domain (include http:// and port if applicable): ")
    new_domain = input("Enter the new domain (include https:// if applicable): ")

    sql_script = generate_sql(old_domain, new_domain)

    print("\n" + "="*50)
    print("Generated SQL Script:")
    print("="*50 + "\n")

    print(Fore.GREEN + sql_script + Style.RESET_ALL)

    pyperclip.copy(sql_script)

    print("\n" + "="*50)
    print(Fore.YELLOW + "The SQL script has been copied to your clipboard!" + Style.RESET_ALL)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()