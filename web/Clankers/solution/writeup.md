# Clankers

Hopefully the anti-AI message is enough to signpost you to `robots.txt`!

This is a text file that dictates the permissions of search engines and similar to trawl the contents of a website.

Using `Disallow: ...` stops them from indexing that page (supposedly!)

---

Inside `robots.txt`, there are two `Disallow` parameters:
- `wp_admin`: default WordPress admin portal
- `oP97hIdqgRNCftlvfwqWFqmBlAJF08Ub.html`: unknown HTML file

Given that the wordpress admin portal doesn't even exist, you need to open the other HTML file. That's where you can find the flag.

---

Peter Walker