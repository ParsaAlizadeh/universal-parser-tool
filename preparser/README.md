# PreParser

This is a pre-written Parser that finds all `<pre>` tags in html format.
It is a good choice for usual judges to find samples. 

This is not a single parser. You can use methods in other parser if you want.

## Methods
- `get_sample(driver)`

After loading web page, this command finds all `<pre>` tags and output list of 
texts in them.

- `load_url(driver, url)`

If your parser depends on `<pre>` tags, it is good to use this method instead of
`driver.get(url)`. In this way, driver just wait for loading `<pre>` tags. So it is
faster than normal mode.