from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session based authentication without CSRF protection.

    Session authentication has the server set a record in the session store
    with a UUID key associated with the logged in user. This key is sent to
    the user in a cookie and, therefore, sent with every subsequent request.
    Any request the server receives with a session key will be authenticated
    if the session key exists in the session store.

    This used to open a security vulnerability. Since the session is sent
    with every request, a malicious website could contain code to submit a
    form to the vulnerable website. Since this request would originate from
    victim's browser, the session key would be sent resulting in an
    authenticated request. To prevent this, forms can include a random token
    every time they are rendered. This token is called a CSRF token. The form
    will not be valid if the CSRF token is incorrect. To summarize, the CSRF
    token protects against this attack by requiring the form to be generated
    only by the server accepting the request and not a malicious website.

    Recently, browsers have implemented additional security measures regarding
    cookies. A new attribute "SameSite" can be set on the cookie. A cookie
    policy of "SameSite: Strict" requires that the cookie will only be sent
    when the request originates from a webpage served on the same site. So,
    a "SameSite: Strict" cookie set by `example.com` will be sent to
    `*.example.com` only when the request to `*.example.com` originates from
    a webpage on `*.example.com`. With this implementation, CSRF attacks
    are blocked, unless the malicious site is on a subdomain of `example.com`.
    Read more about "SameSite" here: https://web.dev/samesite-cookies-explained/.

    We use "SameSite: Strict" on the session cookie via the Django setting
    `SESSION_COOKIE_SAMESITE`. Therefore, in supported browsers, we have
    the usability benefits of session cookies without the hassle of managing
    CSRF tokens. A responsible front-end would examine the User-Agent of the
    browser to determine if it supports the "SameSite" cookie. About 90% of
    browsers do. A notable exception is Internet Explorer 11 on Windows 7.

    See which browsers support the "SameSite" cookie attribute here:
    https://caniuse.com/#feat=same-site-cookie-attribute
    """

    def enforce_csrf(self, request):
        """Do not enforce CSRF tokens.

        The subclassed `SessionAuthentication` backend from Django REST
        Framework uses this method to raise an exception if a CSRF token is
        not sent with a session-authenticated request. This security measure
        is not required due to our use of "SameSite: Strict" session cookies.
        """
        pass
