### eWRT - setup Facebook

* download the facebook Client library for PHP (only needed for creating the infinite session key)
* enter your API_KEY and SECRET_KEY in config_facebook.py
* go to `http://www.facebook.com/code_gen.php?v=1.0&api_key=YOUR_API_KEY`
* generate the code and copy it
* paste the generated code, API-Key and secret-key in ''createInfiniteKey.php''
* run ''createInfiniteKey.php''
* copy the Session-Key to config_facebook.py

### General information on the Facebook API & keys

* [http://stackoverflow.com/questions/6297306/facebook-with-php-api-infinite-session](http://stackoverflow.com/questions/6297306/facebook-with-php-api-infinite-session)
* [http://www.emcro.com/blog/2009/01/facebook-infinite-session-keys-no-more](http://www.emcro.com/blog/2009/01/facebook-infinite-session-keys-no-more/)
* [https://github.com/facebook/php-sdk](https://github.com/facebook/php-sdk)
* [Batch processing using the Facebook graph API](http://developers.facebook.com/docs/reference/api/batch/)


