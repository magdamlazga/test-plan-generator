# Test Plan: Automation Exercise

## 1. Scope

### In scope
- **Cart:** the supplied `/view_cart` page, including its empty-cart message and subscription form. The landing and product pages also show product add-to-cart controls and an “Added!” confirmation.
- **Authentication:** login and signup forms on `/login`.
- **Contact form:** text fields, message area, file upload, and submit on `/contact_us`.
- **Product listing and browsing:** product names, prices, “Add to cart,” and “View Product” controls on `/products`.
- **Category browsing:** the Women > Dress listing on `/category_products/1`.
- **Brand browsing:** the Allen Solly Junior listing on `/brand_products/Allen%20Solly%20Junior`.
- **Subscription:** the `susbscribe_email` form shown on these pages.

### Out of scope
- Pages and flows not supplied, including product details, checkout, payment, account creation completion, and post-login behavior.
- API Testing, Test Cases, Video Tutorials, and other navigation destinations.
- Behavior that cannot be established from the supplied page contents, such as server-side validation rules or the result of file uploads.

## 2. Test cases

### Cart and subscription flow — highest priority

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| CART-01 | Open cart when empty | Open `/view_cart`. | The page displays “Shopping Cart” and “Cart is empty!” with the “Click here to buy products.” prompt. | High |
| CART-02 | Navigate from empty cart to buy products | On the empty cart page, click “here”. | The page navigates to a buying/browsing destination. The exact destination is not specified in the supplied page contents. | High |
| CART-03 | Subscribe with valid email | Enter a valid email in `susbscribe_email` and submit with `subscribe`. | The form submits and a subscription result is shown. The page text includes “You have been successfully subscribed!”; verify this result. | High |
| CART-04 | Submit subscription with empty email | Leave `susbscribe_email` empty and submit with `subscribe`. | The required email field prevents submission or displays validation; no successful subscription should be recorded. | High |
| CART-05 | Submit subscription with malformed email | Enter an invalid email format in `susbscribe_email` and submit. | The invalid email is rejected by validation; no successful subscription should be recorded. | High |
| CART-06 | Submit subscription with special characters or excessive length | Enter special characters or a very long value in `susbscribe_email` and submit. | The input is validated safely; the page does not report a successful subscription for an invalid email or fail unexpectedly. | Medium |
| CART-07 | Add a listed product to cart | On a supplied product listing, select “Add to cart” for a product such as “Blue Top”. | The page shows “Added!” and “Your product has been added to cart.” with “View Cart” and “Continue Shopping” options. | High |
| CART-08 | Add the same product more than once | Select “Add to cart” for the same listed product multiple times. | Each action is handled without an unexpected error. Quantity and duplicate-item behavior cannot be asserted from the supplied page contents. | Medium |
| CART-09 | Check cart after adding a product | Add a product, then select “View Cart”. | The cart page opens. The supplied cart-page contents show only the empty-cart state, so the expected displayed item and quantity require confirmation. | High |

### Authentication flow

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| AUTH-01 | Log in with valid credentials | On `/login`, enter a valid `email` and `password`, then submit with `Login`. | The login request is submitted and the application responds without an error. The destination and exact success behavior are not supplied. | High |
| AUTH-02 | Submit login with both fields empty | Leave `email` and `password` empty; submit with `Login`. | Required-field validation prevents submission or displays validation. | High |
| AUTH-03 | Submit login with empty email | Leave `email` empty, enter a `password`, and submit. | The required `email` field is rejected; login does not succeed. | High |
| AUTH-04 | Submit login with empty password | Enter an `email`, leave `password` empty, and submit. | The required `password` field is rejected; login does not succeed. | High |
| AUTH-05 | Submit login with malformed email | Enter an invalid email format in `email` and a value in `password`; submit. | The invalid email is rejected by validation; login does not succeed. | High |
| AUTH-06 | Submit login with special characters or very long values | Enter special characters or very long values in `email` and/or `password`; submit. | Inputs are handled safely and validation or an authentication response is shown; no unexpected error occurs. | Medium |
| AUTH-07 | Sign up with valid name and email | Enter a `name` and valid `email` in the signup form; submit with `Signup`. | The signup request is submitted and the application responds. The next step and exact success behavior are not supplied. | High |
| AUTH-08 | Submit signup with required fields empty | Leave `name` and `email` empty; submit with `Signup`. | Required-field validation prevents submission or displays validation. | High |
| AUTH-09 | Submit signup with one required field empty | Test separately with `name` empty and `email` populated, then with `email` empty and `name` populated. | The missing required field is rejected; signup does not succeed. | High |
| AUTH-10 | Submit signup with malformed email | Enter a `name` and malformed `email`; submit with `Signup`. | The invalid email is rejected by validation; signup does not succeed. | High |
| AUTH-11 | Submit signup with special characters or very long values | Enter special characters or very long values in `name` and/or `email`; submit. | Values are handled safely and validation or a response is shown; no unexpected error occurs. | Medium |
| AUTH-12 | Sign up with an already-used email | Submit the signup form using an email already registered, if one is available. | The application handles the duplicate email with a response and does not create an unintended duplicate account. Exact behavior is not supplied. | Medium |
| AUTH-13 | Subscribe from the login page | Submit a valid email in the login page’s `susbscribe_email` field. | The subscription form submits and displays the subscription result. | Medium |

### Contact form flow

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| CONTACT-01 | Submit contact form with required email | On `/contact_us`, enter a valid `email`; optionally enter `name`, `subject`, and `message`; submit with `submit`. | The form submits and the application responds. The exact success message or follow-up is not supplied. | High |
| CONTACT-02 | Submit contact form with email only | Enter a valid `email`, leave `name`, `subject`, and `message` empty, then submit. | The form can be submitted because only `email` is marked required; an application response is shown. | High |
| CONTACT-03 | Submit contact form with empty email | Leave `email` empty, optionally populate the other fields, and submit. | Required-field validation prevents submission or displays validation. | High |
| CONTACT-04 | Submit contact form with malformed email | Enter an invalid email in `email`, then submit. | The invalid email is rejected by validation; the form does not submit successfully. | High |
| CONTACT-05 | Submit contact form with special characters | Enter special characters in `name`, `subject`, and `message`, with a valid `email`; submit. | Values are handled safely; no unexpected error occurs. | Medium |
| CONTACT-06 | Submit contact form with very long text | Enter very long values in `name`, `subject`, and `message`, with a valid `email`; submit. | The page handles the values safely, either accepting them or showing validation; no unexpected error occurs. | Medium |
| CONTACT-07 | Upload a file with the contact form | Choose a file in `upload_file`, enter a valid `email`, and submit. | The form submits without an unexpected error. File type, size limits, and upload confirmation are not specified. | Medium |
| CONTACT-08 | Submit contact form without a file | Enter a valid `email`, leave `upload_file` empty, and submit. | The form can be submitted; `upload_file` is optional according to the supplied form. | Medium |
| CONTACT-09 | Subscribe from the contact page | Enter a valid email in `susbscribe_email` and submit with `subscribe`. | The subscription form submits and displays the subscription result. | Medium |

### Product listing and browsing flow

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| PRODUCT-01 | Open all products | Open `/products`. | The page displays “All Products,” category and brand options, and a list of products with prices and controls. | High |
| PRODUCT-02 | Add a listed product to cart | Select “Add to cart” for a product such as “Blue Top”. | The page displays the add-to-cart confirmation and “View Cart” / “Continue Shopping” options. | High |
| PRODUCT-03 | View a listed product | Select “View Product” for a listed product. | A product view opens. Its page content and details are not supplied. | Medium |
| PRODUCT-04 | Browse by category | Select a visible category such as Women > Dress. | The corresponding category listing opens and shows products for that category. | Medium |
| PRODUCT-05 | Browse by brand | Select “Allen Solly Junior” in the brand list. | The brand listing opens and displays “Brand - Allen Solly Junior Products” and its listed items. | Medium |
| PRODUCT-06 | Verify listed product names and prices | Compare visible product entries, such as “Blue Top” at Rs. 500 and “Men Tshirt” at Rs. 400, with the supplied listing. | Product names and prices are displayed as shown in the page contents. | Medium |
| PRODUCT-07 | Add a product repeatedly | Select “Add to cart” repeatedly for the same product. | Each action is handled without an unexpected error. Quantity and duplicate behavior require clarification. | Medium |
| PRODUCT-08 | Subscribe from the products page | Enter a valid email in `susbscribe_email` and submit with `subscribe`. | The subscription form submits and displays the subscription result. | Low |

### Category browsing flow

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| CATEGORY-01 | Open Women > Dress products | Open `/category_products/1`. | The page identifies “Women > Dress” / “Women - Dress Products” and displays the listed dress products. | High |
| CATEGORY-02 | Verify category product names and prices | Check the displayed products, including “Sleeveless Dress” at Rs. 1000, “Stylish Dress” at Rs. 1500, and “Rose Pink Embroidered Maxi Dress” at Rs. 2300. | Product names and prices match the page contents. | Medium |
| CATEGORY-03 | Add a category product to cart | Select “Add to cart” for a listed category product. | The add-to-cart confirmation appears with “View Cart” and “Continue Shopping”. | Medium |
| CATEGORY-04 | Subscribe from the category page | Enter a valid email in `susbscribe_email` and submit with `subscribe`. | The subscription form submits and displays the subscription result. | Low |

### Brand browsing flow

| ID | Title | Steps | Expected result | Priority |
|---|---|---|---|---|
| BRAND-01 | Open Allen Solly Junior products | Open `/brand_products/Allen%20Solly%20Junior`. | The page identifies “Brand - Allen Solly Junior Products” and displays its listed products. | High |
| BRAND-02 | Verify brand product names and prices | Check “Frozen Tops For Kids” at Rs. 278, “Sleeveless Unicorn Patch Gown - Pink” at Rs. 1050, and “Colour Blocked Shirt – Sky Blue” at Rs. 849. | Product names and prices match the page contents. | Medium |
| BRAND-03 | Add a brand product to cart | Select “Add to cart” for a listed brand product. | The add-to-cart confirmation appears with “View Cart” and “Continue Shopping”. | Medium |
| BRAND-04 | Subscribe from the brand page | Enter a valid email in `susbscribe_email` and submit with `subscribe`. | The subscription form submits and displays the subscription result. | Low |

## 3. Risks and open questions

- The supplied cart page shows only an empty-cart state, so item display, quantity updates, removal, and persistence after adding products cannot be fully specified.
- The page contents do not describe checkout, payment, or order placement.
- Login and signup outcomes are not shown. Clarify success destinations, error messages, password rules, and whether duplicate signup email addresses are rejected.
- The contact form’s success behavior, file upload constraints, and handling of submitted feedback are not shown.
- Subscription success text is present in the page contents, but validation messages, duplicate-email behavior, and persistence are not specified.
- No field length limits or detailed validation rules are supplied. Special-character and very-long-input tests should check safe handling, but exact acceptance criteria need confirmation.
- The product listing shows add-to-cart confirmation but does not specify quantity controls or duplicate-item behavior.