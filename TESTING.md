
# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.


### HTML

I used the [W3C Nu HTML Checker](https://validator.w3.org/nu/) to validate the rendered HTML of each page by direct input. Screenshots of the successful validation results are provided below.

| Directory | File | Screenshot |
| --- | --- | --- |
| artworks | [artwork_detail.html](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/templates/artworks/artwork_detail.html) | ![screenshot](documentation/validation/html-artworks-artwork_detail.png) |
| artworks | [artworks.html](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/templates/artworks/artworks.html) | ![screenshot](documentation/validation/html-artworks-artworks.png) |
| artworks | [collections.html](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/templates/artworks/collections.html) | ![screenshot](documentation/validation/html-artworks-collections.png) |
| commissions | [checkout.html](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/templates/commissions/checkout.html) | ![screenshot](documentation/validation/html-commissions-checkout.png) |
| commissions | [checkout_success.html](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/templates/commissions/checkout_success.html) | ![screenshot](documentation/validation/html-commissions-checkout_success.png) |
| commissions | [commission.html](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/templates/commissions/commission.html) | ![screenshot](documentation/validation/html-commissions-commission.png) |
| commissions | [customer_details.html](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/templates/commissions/customer_details.html) | ![screenshot](documentation/validation/html-commissions-customer_details.png) |
| dashboard | [artwork_delete.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/artwork_delete.html) | ![screenshot](documentation/validation/html-dashboard-artwork_delete.png) |
| dashboard | [artwork_form.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/artwork_form.html) | ![screenshot](documentation/validation/html-dashboard-artwork_form.png) |
| dashboard | [artwork_list.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/artwork_list.html) | ![screenshot](documentation/validation/html-dashboard-artwork_list.png) |
| dashboard | [artwork_overview.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/artwork_overview.html) | ![screenshot](documentation/validation/html-dashboard-artwork_overview.png) |
| dashboard | [collection_delete.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/collection_delete.html) | ![screenshot](documentation/validation/html-dashboard-collection_delete.png) |
| dashboard | [collection_form.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/collection_form.html) | ![screenshot](documentation/validation/html-dashboard-collection_form.png) |
| dashboard | [collection_list.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/collection_list.html) | ![screenshot](documentation/validation/html-dashboard-collection_list.png) |
| dashboard | [collection_overview.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/collection_overview.html) | ![screenshot](documentation/validation/html-dashboard-collection_overview.png) |
| dashboard | [commission_list.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/commission_list.html) | ![screenshot](documentation/validation/html-dashboard-commission_list.png) |
| dashboard | [message_list.html](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/templates/dashboard/message_list.html) | ![screenshot](documentation/validation/html-dashboard-message_list.png) |
| pages | [about.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/about.html) | ![screenshot](documentation/validation/html-pages-about.png) |
| pages | [collaborations.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/collaborations.html) | ![screenshot](documentation/validation/html-pages-collaborations.png) |
| pages | [contact.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/contact.html) | ![screenshot](documentation/validation/html-pages-contact.png) |
| pages | [in-situ.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/in-situ.html) | ![screenshot](documentation/validation/html-pages-in-situ.png) |
| pages | [index.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/index.html) | ![screenshot](documentation/validation/html-pages-index.png) |
| pages | [retail.html](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/templates/pages/retail.html) | ![screenshot](documentation/validation/html-pages-retail.png) |
| profiles | [my_account.html](https://github.com/angela64711/fourth-milestone-project/blob/main/profiles/templates/profiles/my_account.html) | ![screenshot](documentation/validation/html-profiles-my_account.png) |
| templates | [403.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/403.html) | ![screenshot](documentation/validation/html-templates-403.png) |
| templates | [404.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/404.html) | ![screenshot](documentation/validation/html-templates-404.png) |
| templates/account | [email_confirm.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/account/email_confirm.html) | ![screenshot](documentation/validation/html-templates-email_confirm.png) |
| templates/account | [login.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/account/login.html) | ![screenshot](documentation/validation/html-templates-login.png) |
| templates/account | [logout.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/account/logout.html) | ![screenshot](documentation/validation/html-templates-logout.png) |
| templates/account | [signup.html](https://github.com/angela64711/fourth-milestone-project/blob/main/templates/account/signup.html) | ![screenshot](documentation/validation/html-templates-signup.png) |


### CSS

I used the recommended [W3C Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/) to validate all seven custom CSS stylesheets. All files passed with zero errors. The remaining warnings relate to CSS custom properties (`var()`), which the validator cannot statically check due to their dynamic nature.

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| static | [art.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/art.css) | ![screenshot](documentation/validation/css-static-art.png) | Validated by direct input |
| static | [base.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/base.css) | ![screenshot](documentation/validation/css-static-base.png) | Validated by direct input |
| static | [commissions.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/commissions.css) | ![screenshot](documentation/validation/css-static-commissions.png) | Validated by direct input |
| static | [home.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/home.css) | ![screenshot](documentation/validation/css-static-home.png) | Validated by URL |
| static | [pages.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/pages.css) | ![screenshot](documentation/validation/css-static-pages.png) | Validated by direct input |
| static | [profile.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/profile.css) | ![screenshot](documentation/validation/css-static-profile.png) | Validated by direct input |
| static | [dashboard.css](https://github.com/angela64711/fourth-milestone-project/blob/main/static/css/dashboard.css) | ![screenshot](documentation/validation/css-static-dashboard.png) | Validated by direct input |



### JavaScript


I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files. All files passed validation without errors or warnings. Screenshots of the validation results are provided below.


| Directory | File | Screenshot |
| --- | --- | --- |
| static | [commission_pricing.js](https://github.com/angela64711/fourth-milestone-project/blob/main/static/js/commission_pricing.js) | ![screenshot](documentation/validation/js-static-commission_pricing.png) |
| static | [commissions.js](https://github.com/angela64711/fourth-milestone-project/blob/main/static/js/commissions.js) | ![screenshot](documentation/validation/js-static-commissions.png) |
| static | [commission_payment.js](https://github.com/angela64711/fourth-milestone-project/blob/main/static/js/commission_payment.js) | ![screenshot](documentation/validation/js-static-commission_payment.png) |
| static | [collection_cover.js](https://github.com/angela64711/fourth-milestone-project/blob/main/static/js/collection_cover.js) | ![screenshot](documentation/validation/js-static-collection_cover.png) |
| static | [homepage.js](https://github.com/angela64711/fourth-milestone-project/blob/main/static/js/homepage.js) | ![screenshot](documentation/validation/js-static-homepage.png) |


### Python


I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.


| Directory | File | URL | Screenshot | 
| --- | --- | --- | --- | 
| artworks | [admin.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/admin.py) | ![screenshot](documentation/validation/py-artworks-admin.png) | 
| artworks | [import_artworks.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/management/commands/import_artworks.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/management/commands/import_artworks.py) | ![screenshot](documentation/validation/py-artworks-import_artworks.png) |
| artworks | [models.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/models.py) | ![screenshot](documentation/validation/py-artworks-models.png) |
| artworks | [test_models.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/test_models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/test_models.py) | ![screenshot](documentation/validation/py-artworks-test_models.png) | 
| artworks | [test_views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/test_views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/test_views.py) | ![screenshot](documentation/validation/py-artworks-test_views.png) | 
| artworks | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/urls.py) | ![screenshot](documentation/validation/py-artworks-urls.png) | 
| artworks | [views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/artworks/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/artworks/views.py) | ![screenshot](documentation/validation/py-artworks-views.png) | 
| commissions | [admin.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/admin.py) | ![screenshot](documentation/validation/py-commissions-admin.png) | 
| commissions | [emails.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/emails.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/emails.py) | ![screenshot](documentation/validation/py-commissions-emails.png) | 
| commissions | [forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/forms.py) | ![screenshot](documentation/validation/py-commissions-forms.png) | 
| commissions | [models.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/models.py) | ![screenshot](documentation/validation/py-commissions-models.png) | 
| commissions | [pricing.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/pricing.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/pricing.py) | ![screenshot](documentation/validation/py-commissions-pricing.png) | 
| commissions | [test_emails.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/test_emails.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/test_emails.py) | ![screenshot](documentation/validation/py-commissions-test_emails.png) | 
| commissions | [test_forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/test_forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/test_forms.py) | ![screenshot](documentation/validation/py-commissions-test_forms.png) | 
| commissions | [test_models.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/test_models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/test_models.py) | ![screenshot](documentation/validation/py-commissions-test_models.png) | 
| commissions | [test_pricing.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/test_pricing.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/test_pricing.py) | ![screenshot](documentation/validation/py-commissions-test_pricing.png) | 
| commissions | [test_views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/test_views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/test_views.py) | ![screenshot](documentation/validation/py-commissions-test_views.png) | 
| commissions | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/urls.py) | ![screenshot](documentation/validation/py-commissions-urls.png) | 
| commissions | [views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/commissions/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/commissions/views.py) | ![screenshot](documentation/validation/py-commissions-views.png) | 
| dashboard | [admin.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/admin.py) | ![screenshot](documentation/validation/py-dashboard-admin.png) | 
| dashboard | [context_processors.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/context_processors.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/context_processors.py) | ![screenshot](documentation/validation/py-dashboard-context_processors.png) | 
| dashboard | [forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/forms.py) | ![screenshot](documentation/validation/py-dashboard-forms.png) | 
| dashboard | [models.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/models.py) | ![screenshot](documentation/validation/py-dashboard-models.png) | 
| dashboard | [test_artwork_crud.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_artwork_crud.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_artwork_crud.py) | ![screenshot](documentation/validation/py-dashboard-test_artwork_crud.png) | 
| dashboard | [test_artwork_list.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_artwork_list.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_artwork_list.py) | ![screenshot](documentation/validation/py-dashboard-test_artwork_list.png) |
| dashboard | [test_collection_crud.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_collection_crud.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_collection_crud.py) | ![screenshot](documentation/validation/py-dashboard-test_collection_crud.png) |
| dashboard | [test_collection_list.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_collection_list.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_collection_list.py) | ![screenshot](documentation/validation/py-dashboard-test_collection_list.png) | 
| dashboard | [test_commissions.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_commissions.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_commissions.py) | ![screenshot](documentation/validation/py-dashboard-test_commissions.png) | 
| dashboard | [test_forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_forms.py) | ![screenshot](documentation/validation/py-dashboard-test_forms.png) | 
| dashboard | [test_messages.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_messages.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_messages.py) | ![screenshot](documentation/validation/py-dashboard-test_messages.png) | 
| dashboard | [test_permissions.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/test_permissions.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/test_permissions.py) | ![screenshot](documentation/validation/py-dashboard-test_permissions.png) | 
| dashboard | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/urls.py) | ![screenshot](documentation/validation/py-dashboard-urls.png) | 
| dashboard | [views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/dashboard/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/dashboard/views.py) | ![screenshot](documentation/validation/py-dashboard-views.png) | 
| frank_moth | [settings.py](https://github.com/angela64711/fourth-milestone-project/blob/main/frank_moth/settings.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/frank_moth/settings.py) | ![screenshot](documentation/validation/py-frank_moth-settings.png) | 
| frank_moth | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/frank_moth/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/frank_moth/urls.py) | ![screenshot](documentation/validation/py-frank_moth-urls.png) | 
| root | [manage.py](https://github.com/angela64711/fourth-milestone-project/blob/main/manage.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/manage.py) | ![screenshot](documentation/validation/py-root-manage.png) | 
| pages | [forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/pages/forms.py) | ![screenshot](documentation/validation/py-pages-forms.png) | 
| pages | [test_forms.py](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/test_forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/pages/test_forms.py) | ![screenshot](documentation/validation/py-pages-test_forms.png) | 
| pages | [test_views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/test_views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/pages/test_views.py) | ![screenshot](documentation/validation/py-pages-test_views.png) | 
| pages | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/pages/urls.py) | ![screenshot](documentation/validation/py-pages-urls.png) | 
| pages | [views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/pages/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/pages/views.py) | ![screenshot](documentation/validation/py-pages-views.png) | 
| profiles | [tests.py](https://github.com/angela64711/fourth-milestone-project/blob/main/profiles/tests.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/profiles/tests.py) | ![screenshot](documentation/validation/py-profiles-tests.png) | 
| profiles | [urls.py](https://github.com/angela64711/fourth-milestone-project/blob/main/profiles/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/profiles/urls.py) | ![screenshot](documentation/validation/py-profiles-urls.png) | 
| profiles | [views.py](https://github.com/angela64711/fourth-milestone-project/blob/main/profiles/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/angela64711/fourth-milestone-project/main/profiles/views.py) | ![screenshot](documentation/validation/py-profiles-views.png) | 




## Responsiveness


I've tested my deployed project to check for responsiveness issues.


| Page | Mobile | Tablet | Desktop | Notes |
| --- | --- | --- | --- | --- |
| Home | ![screenshot](documentation/responsiveness/mobile-home.png) | ![screenshot](documentation/responsiveness/tablet-home.png) | ![screenshot](documentation/responsiveness/desktop-home.png) | Works as expected |
| Art | ![screenshot](documentation/responsiveness/mobile-art.png) | ![screenshot](documentation/responsiveness/tablet-art.png) | ![screenshot](documentation/responsiveness/desktop-art.png) | Works as expected |
| Artworks | ![screenshot](documentation/responsiveness/mobile-artworks.png) | ![screenshot](documentation/responsiveness/tablet-artworks.png) | ![screenshot](documentation/responsiveness/desktop-artworks.png) | Works as expected |
| Artwork Detail | ![screenshot](documentation/responsiveness/mobile-artwork-detail.png) | ![screenshot](documentation/responsiveness/tablet-artwork-detail.png) | ![screenshot](documentation/responsiveness/desktop-artwork-detail.png) | Works as expected |
| In Situ | ![screenshot](documentation/responsiveness/mobile-in-situ.png) | ![screenshot](documentation/responsiveness/tablet-in-situ.png) | ![screenshot](documentation/responsiveness/desktop-in-situ.png) | Works as expected |
| About | ![screenshot](documentation/responsiveness/mobile-about.png) | ![screenshot](documentation/responsiveness/tablet-about.png) | ![screenshot](documentation/responsiveness/desktop-about.png) | Works as expected |
| Collaborations | ![screenshot](documentation/responsiveness/mobile-collaborations.png) | ![screenshot](documentation/responsiveness/tablet-collaborations.png) | ![screenshot](documentation/responsiveness/desktop-collaborations.png) | Works as expected |
| Where to Buy | ![screenshot](documentation/responsiveness/mobile-where-to-buy.png) | ![screenshot](documentation/responsiveness/tablet-where-to-buy.png) | ![screenshot](documentation/responsiveness/desktop-where-to-buy.png) | Works as expected |
| Commissions | ![screenshot](documentation/responsiveness/mobile-commissions.png) | ![screenshot](documentation/responsiveness/tablet-commissions.png) | ![screenshot](documentation/responsiveness/desktop-commissions.png) | Works as expected |
| Commission Checkout | ![screenshot](documentation/responsiveness/mobile-commission-checkout.png) | ![screenshot](documentation/responsiveness/tablet-commission-checkout.png) | ![screenshot](documentation/responsiveness/desktop-commission-checkout.png) | Works as expected |
| Commission Success | ![screenshot](documentation/responsiveness/mobile-commission-success.png) | ![screenshot](documentation/responsiveness/tablet-commission-success.png) | ![screenshot](documentation/responsiveness/desktop-commission-success.png) | Works as expected |
| Contact | ![screenshot](documentation/responsiveness/mobile-contact.png) | ![screenshot](documentation/responsiveness/tablet-contact.png) | ![screenshot](documentation/responsiveness/desktop-contact.png) | Works as expected |
| Register | ![screenshot](documentation/responsiveness/mobile-register.png) | ![screenshot](documentation/responsiveness/tablet-register.png) | ![screenshot](documentation/responsiveness/desktop-register.png) | Works as expected |
| Login | ![screenshot](documentation/responsiveness/mobile-login.png) | ![screenshot](documentation/responsiveness/tablet-login.png) | ![screenshot](documentation/responsiveness/desktop-login.png) | Works as expected |
| Logout | ![screenshot](documentation/responsiveness/mobile-logout.png) | ![screenshot](documentation/responsiveness/tablet-logout.png) | ![screenshot](documentation/responsiveness/desktop-logout.png) | Works as expected |
| Account | ![screenshot](documentation/responsiveness/mobile-account.png) | ![screenshot](documentation/responsiveness/tablet-account.png) | ![screenshot](documentation/responsiveness/desktop-account.png) | Works as expected |
| Manage Artworks | ![screenshot](documentation/responsiveness/mobile-manage-artworks.png) | ![screenshot](documentation/responsiveness/tablet-manage-artworks.png) | ![screenshot](documentation/responsiveness/desktop-manage-artworks.png) | Works as expected |
| Artwork Overview | ![screenshot](documentation/responsiveness/mobile-artwork-overview.png) | ![screenshot](documentation/responsiveness/tablet-artwork-overview.png) | ![screenshot](documentation/responsiveness/desktop-artwork-overview.png) | Works as expected |
| Add Artwork | ![screenshot](documentation/responsiveness/mobile-add-artwork.png) | ![screenshot](documentation/responsiveness/tablet-add-artwork.png) | ![screenshot](documentation/responsiveness/desktop-add-artwork.png) | Works as expected |
| Edit Artwork | ![screenshot](documentation/responsiveness/mobile-edit-artwork.png) | ![screenshot](documentation/responsiveness/tablet-edit-artwork.png) | ![screenshot](documentation/responsiveness/desktop-edit-artwork.png) | Works as expected |
| Delete Artwork | ![screenshot](documentation/responsiveness/mobile-delete-artwork.png) | ![screenshot](documentation/responsiveness/tablet-delete-artwork.png) | ![screenshot](documentation/responsiveness/desktop-delete-artwork.png) | Works as expected |
| Manage Collections | ![screenshot](documentation/responsiveness/mobile-manage-collections.png) | ![screenshot](documentation/responsiveness/tablet-manage-collections.png) | ![screenshot](documentation/responsiveness/desktop-manage-collections.png) | Works as expected |
| Collection Overview | ![screenshot](documentation/responsiveness/mobile-collection-overview.png) | ![screenshot](documentation/responsiveness/tablet-collection-overview.png) | ![screenshot](documentation/responsiveness/desktop-collection-overview.png) | Works as expected |
| Add Collection | ![screenshot](documentation/responsiveness/mobile-add-collection.png) | ![screenshot](documentation/responsiveness/tablet-add-collection.png) | ![screenshot](documentation/responsiveness/desktop-add-collection.png) | Works as expected |
| Edit Collection | ![screenshot](documentation/responsiveness/mobile-edit-collection.png) | ![screenshot](documentation/responsiveness/tablet-edit-collection.png) | ![screenshot](documentation/responsiveness/desktop-edit-collection.png) | Works as expected |
| Delete Collection | ![screenshot](documentation/responsiveness/mobile-delete-collection.png) | ![screenshot](documentation/responsiveness/tablet-delete-collection.png) | ![screenshot](documentation/responsiveness/desktop-delete-collection.png) | Works as expected |
| Manage Commissions | ![screenshot](documentation/responsiveness/mobile-manage-commissions.png) | ![screenshot](documentation/responsiveness/tablet-manage-commissions.png) | ![screenshot](documentation/responsiveness/desktop-manage-commissions.png) | Works as expected |
| Messages | ![screenshot](documentation/responsiveness/mobile-messages.png) | ![screenshot](documentation/responsiveness/tablet-messages.png) | ![screenshot](documentation/responsiveness/desktop-messages.png) | Works as expected |
| 404 | ![screenshot](documentation/responsiveness/mobile-404.png) | ![screenshot](documentation/responsiveness/tablet-404.png) | ![screenshot](documentation/responsiveness/desktop-404.png) | Works as expected |
| 403 | ![screenshot](documentation/responsiveness/mobile-403.png) | ![screenshot](documentation/responsiveness/tablet-403.png) | ![screenshot](documentation/responsiveness/desktop-403.png) | Works as expected |



## Browser Compatibility

Browser compatibility was tested using Google Chrome, Mozilla Firefox and Microsoft Edge. The [FireShot browser extension](https://getfireshot.com/) was used to capture full-page screenshots, providing evidence of how the complete page layouts render across the three browsers, including content beyond the visible viewport.

| Page | Chrome | Firefox | Edge | Notes |
| --- | --- | --- | --- | --- |
| Home | ![screenshot](documentation/browsers/chrome-home.png) | ![screenshot](documentation/browsers/firefox-home.png) | ![screenshot](documentation/browsers/edge-home.png) | Works as expected |
| Art | ![screenshot](documentation/browsers/chrome-art.png) | ![screenshot](documentation/browsers/firefox-art.png) | ![screenshot](documentation/browsers/edge-art.png) | Works as expected |
| Artworks | ![screenshot](documentation/browsers/chrome-artworks.png) | ![screenshot](documentation/browsers/firefox-artworks.png) | ![screenshot](documentation/browsers/edge-artworks.png) | Works as expected |
| Artwork Detail | ![screenshot](documentation/browsers/chrome-artwork-detail.png) | ![screenshot](documentation/browsers/firefox-artwork-detail.png) | ![screenshot](documentation/browsers/edge-artwork-detail.png) | Works as expected |
| In Situ | ![screenshot](documentation/browsers/chrome-in-situ.png) | ![screenshot](documentation/browsers/firefox-in-situ.png) | ![screenshot](documentation/browsers/edge-in-situ.png) | Works as expected |
| About | ![screenshot](documentation/browsers/chrome-about.png) | ![screenshot](documentation/browsers/firefox-about.png) | ![screenshot](documentation/browsers/edge-about.png) | Works as expected |
| Collaborations | ![screenshot](documentation/browsers/chrome-collaborations.png) | ![screenshot](documentation/browsers/firefox-collaborations.png) | ![screenshot](documentation/browsers/edge-collaborations.png) | Works as expected |
| Where to Buy | ![screenshot](documentation/browsers/chrome-where-to-buy.png) | ![screenshot](documentation/browsers/firefox-where-to-buy.png) | ![screenshot](documentation/browsers/edge-where-to-buy.png) | Works as expected |
| Commissions | ![screenshot](documentation/browsers/chrome-commissions.png) | ![screenshot](documentation/browsers/firefox-commissions.png) | ![screenshot](documentation/browsers/edge-commissions.png) | Works as expected |
| Contact | ![screenshot](documentation/browsers/chrome-contact.png) | ![screenshot](documentation/browsers/firefox-contact.png) | ![screenshot](documentation/browsers/edge-contact.png) | Works as expected |
| Register | ![screenshot](documentation/browsers/chrome-register.png) | ![screenshot](documentation/browsers/firefox-register.png) | ![screenshot](documentation/browsers/edge-register.png) | Works as expected |
| Login | ![screenshot](documentation/browsers/chrome-login.png) | ![screenshot](documentation/browsers/firefox-login.png) | ![screenshot](documentation/browsers/edge-login.png) | Works as expected |
| Logout | ![screenshot](documentation/browsers/chrome-logout.png) | ![screenshot](documentation/browsers/firefox-logout.png) | ![screenshot](documentation/browsers/edge-logout.png) | Works as expected |
| Account | ![screenshot](documentation/browsers/chrome-account.png) | ![screenshot](documentation/browsers/firefox-account.png) | ![screenshot](documentation/browsers/edge-account.png) | Works as expected |
| Manage Artworks | ![screenshot](documentation/browsers/chrome-manage-artworks.png) | ![screenshot](documentation/browsers/firefox-manage-artworks.png) | ![screenshot](documentation/browsers/edge-manage-artworks.png) | Works as expected |
| Artwork Overview | ![screenshot](documentation/browsers/chrome-artwork-overview.png) | ![screenshot](documentation/browsers/firefox-artwork-overview.png) | ![screenshot](documentation/browsers/edge-artwork-overview.png) | Works as expected |
| Add Artwork | ![screenshot](documentation/browsers/chrome-add-artwork.png) | ![screenshot](documentation/browsers/firefox-add-artwork.png) | ![screenshot](documentation/browsers/edge-add-artwork.png) | Works as expected |
| Edit Artwork | ![screenshot](documentation/browsers/chrome-edit-artwork.png) | ![screenshot](documentation/browsers/firefox-edit-artwork.png) | ![screenshot](documentation/browsers/edge-edit-artwork.png) | Works as expected |
| Delete Artwork | ![screenshot](documentation/browsers/chrome-delete-artwork.png) | ![screenshot](documentation/browsers/firefox-delete-artwork.png) | ![screenshot](documentation/browsers/edge-delete-artwork.png) | Works as expected |
| Manage Collections | ![screenshot](documentation/browsers/chrome-manage-collections.png) | ![screenshot](documentation/browsers/firefox-manage-collections.png) | ![screenshot](documentation/browsers/edge-manage-collections.png) | Works as expected |
| Collection Overview | ![screenshot](documentation/browsers/chrome-collection-overview.png) | ![screenshot](documentation/browsers/firefox-collection-overview.png) | ![screenshot](documentation/browsers/edge-collection-overview.png) | Works as expected |
| Add Collection | ![screenshot](documentation/browsers/chrome-add-collection.png) | ![screenshot](documentation/browsers/firefox-add-collection.png) | ![screenshot](documentation/browsers/edge-add-collection.png) | Works as expected |
| Edit Collection | ![screenshot](documentation/browsers/chrome-edit-collection.png) | ![screenshot](documentation/browsers/firefox-edit-collection.png) | ![screenshot](documentation/browsers/edge-edit-collection.png) | Works as expected |
| Delete Collection | ![screenshot](documentation/browsers/chrome-delete-collection.png) | ![screenshot](documentation/browsers/firefox-delete-collection.png) | ![screenshot](documentation/browsers/edge-delete-collection.png) | Works as expected |
| Manage Commissions | ![screenshot](documentation/browsers/chrome-manage-commissions.png) | ![screenshot](documentation/browsers/firefox-manage-commissions.png) | ![screenshot](documentation/browsers/edge-manage-commissions.png) | Works as expected |
| Messages | ![screenshot](documentation/browsers/chrome-messages.png) | ![screenshot](documentation/browsers/firefox-messages.png) | ![screenshot](documentation/browsers/edge-messages.png) | Works as expected |
| 404 | ![screenshot](documentation/browsers/chrome-404.png) | ![screenshot](documentation/browsers/firefox-404.png) | ![screenshot](documentation/browsers/edge-404.png) | Works as expected |


## Accessibility and Colour Contrast

Accessibility was considered throughout the development of the website, with particular attention to colour contrast, keyboard navigation, visible focus indicators and reduced-motion preferences.

### Colour Contrast

The website's colour palette was checked using a colour contrast checker to assess readability against WCAG accessibility guidelines.

The primary text colours, dark blue (`#263E60`) and dark grey (`#383838`), provide strong contrast against the light background (`#F0EFEB`) and off-white (`#FDFCFA`) surfaces.

The accent green (`#80E633`) against the dark blue (`#263E60`) achieves a contrast ratio of approximately **6.84:1**, meeting WCAG AA requirements for normal and large text, as well as AAA requirements for large text. It falls slightly below the AAA requirement for normal text.

Although this combination meets WCAG AA text contrast requirements, green is used sparingly throughout the website, primarily for decorative details, underlines, buttons and hover effects rather than extended passages of text.

During accessibility testing, the large green heading on the Where to Buy page was changed to dark blue, with a decorative green underline, to improve readability while preserving the website's visual identity.

### Keyboard Accessibility

Interactive elements, including navigation links, buttons and form controls, were designed to support keyboard navigation. Visible focus indicators help keyboard users identify the currently focused element.

### Reduced Motion

The website takes user motion preferences into consideration. Where reduced motion is requested through the user's operating system or browser settings, supported animations and motion effects are reduced or disabled to provide a more comfortable experience.




## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues. Some warnings are outside of my control, and mobile results tend to be lower than desktop.

### Performance and Image Quality Considerations

The Frank Moth website is a visually driven artist portfolio, where high-quality artwork images are essential to the user experience. Performance optimisation therefore required balancing efficient image delivery with preserving the visual detail and quality of the artwork.

Images were provided in WebP format, and lazy loading was implemented where appropriate to reduce unnecessary initial downloads. Following the initial Lighthouse audits, several images were further resized and optimised based on the recommendations. **The audits were then repeated, and the results presented above reflect the final performance scores after these improvements.** Lighthouse audits generally achieved strong desktop performance scores, while mobile scores were somewhat lower on image-heavy pages.

Mobile Lighthouse testing simulates more constrained device and network conditions, making image-heavy pages particularly challenging. Further image compression could improve performance scores but may compromise the presentation of the artwork, especially on larger desktop displays.

For this reason, the decision was made to prioritise a reasonable balance between performance, image quality and user experience rather than pursuing a perfect Lighthouse score at the expense of the portfolio's visual presentation.


| Page | Mobile | Desktop |
| --- | --- | --- |
| Home | ![screenshot](documentation/lighthouse/mobile-home.png) | ![screenshot](documentation/lighthouse/desktop-home.png) |
| Art | ![screenshot](documentation/lighthouse/mobile-art.png) | ![screenshot](documentation/lighthouse/desktop-art.png) |
| Artworks | ![screenshot](documentation/lighthouse/mobile-artworks.png) | ![screenshot](documentation/lighthouse/desktop-artworks.png) |
| Artwork Detail | ![screenshot](documentation/lighthouse/mobile-artwork-detail.png) | ![screenshot](documentation/lighthouse/desktop-artwork-detail.png) |
| In Situ | ![screenshot](documentation/lighthouse/mobile-in-situ.png) | ![screenshot](documentation/lighthouse/desktop-in-situ.png) |
| About | ![screenshot](documentation/lighthouse/mobile-about.png) | ![screenshot](documentation/lighthouse/desktop-about.png) |
| Collaborations | ![screenshot](documentation/lighthouse/mobile-collaborations.png) | ![screenshot](documentation/lighthouse/desktop-collaborations.png) |
| Where to Buy | ![screenshot](documentation/lighthouse/mobile-where-to-buy.png) | ![screenshot](documentation/lighthouse/desktop-where-to-buy.png) |
| Commissions | ![screenshot](documentation/lighthouse/mobile-commissions.png) | ![screenshot](documentation/lighthouse/desktop-commissions.png) |
| Contact | ![screenshot](documentation/lighthouse/mobile-contact.png) | ![screenshot](documentation/lighthouse/desktop-contact.png) |
| Register | ![screenshot](documentation/lighthouse/mobile-register.png) | ![screenshot](documentation/lighthouse/desktop-register.png) |
| Login | ![screenshot](documentation/lighthouse/mobile-login.png) | ![screenshot](documentation/lighthouse/desktop-login.png) |
| Logout | ![screenshot](documentation/lighthouse/mobile-logout.png) | ![screenshot](documentation/lighthouse/desktop-logout.png) |
| Account | ![screenshot](documentation/lighthouse/mobile-account.png) | ![screenshot](documentation/lighthouse/desktop-account.png) |
| Manage Artworks | ![screenshot](documentation/lighthouse/mobile-manage-artworks.png) | ![screenshot](documentation/lighthouse/desktop-manage-artworks.png) |
| Artwork Overview | ![screenshot](documentation/lighthouse/mobile-artwork-overview.png) | ![screenshot](documentation/lighthouse/desktop-artwork-overview.png) |
| Add Artwork | ![screenshot](documentation/lighthouse/mobile-add-artwork.png) | ![screenshot](documentation/lighthouse/desktop-add-artwork.png) |
| Edit Artwork | ![screenshot](documentation/lighthouse/mobile-edit-artwork.png) | ![screenshot](documentation/lighthouse/desktop-edit-artwork.png) |
| Delete Artwork | ![screenshot](documentation/lighthouse/mobile-delete-artwork.png) | ![screenshot](documentation/lighthouse/desktop-delete-artwork.png) |
| Manage Collections | ![screenshot](documentation/lighthouse/mobile-manage-collections.png) | ![screenshot](documentation/lighthouse/desktop-manage-collections.png) |
| Collection Overview | ![screenshot](documentation/lighthouse/mobile-collection-overview.png) | ![screenshot](documentation/lighthouse/desktop-collection-overview.png) |
| Add Collection | ![screenshot](documentation/lighthouse/mobile-add-collection.png) | ![screenshot](documentation/lighthouse/desktop-add-collection.png) |
| Edit Collection | ![screenshot](documentation/lighthouse/mobile-edit-collection.png) | ![screenshot](documentation/lighthouse/desktop-edit-collection.png) |
| Delete Collection | ![screenshot](documentation/lighthouse/mobile-delete-collection.png) | ![screenshot](documentation/lighthouse/desktop-delete-collection.png) |
| Manage Commissions | ![screenshot](documentation/lighthouse/mobile-manage-commissions.png) | ![screenshot](documentation/lighthouse/desktop-manage-commissions.png) |
| Messages | ![screenshot](documentation/lighthouse/mobile-messages.png) | ![screenshot](documentation/lighthouse/desktop-messages.png) |



## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:


| Page | Expectation | Test Performed | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Registration | Users cannot register without completing required fields. | Submit the registration form with all fields empty. | Passed locally | ![Registration validation](documentation/defensive/registration-validation.png) |
| Login | Users cannot log in with invalid credentials. | Attempt to log in with an incorrect password. | Passed locally | ![Invalid login](documentation/defensive/invalid-login.png) |
| Contact | Invalid email addresses are rejected before form submission. | Complete the required fields, enter an email address without the @ symbol, and attempt to submit the form. | Passed locally | ![Contact validation](documentation/defensive/contact-validation.png) |
| Artist Dashboard - Add Artwork | Incomplete artwork records cannot be created. | Submit the Add Artwork form without completing required fields. | Passed locally | ![Artwork validation](documentation/defensive/artwork-validation.png) |
| Artist Dashboard - Add Collection | Incomplete collections cannot be created. | Submit the Add Collection form without completing required fields. | Passed locally | ![Collection validation](documentation/defensive/collection-validation.png) |
| Commissions - Creative Preferences | Invalid or incomplete creative preferences cannot be submitted. | Leave required preferences empty or exceed the permitted selection limits. | Passed locally | ![Creative preferences validation](documentation/defensive/creative-validation.png) |
| Commissions - Customer Details | Physical commission orders require valid customer and shipping information. | Select a physical artwork and attempt to continue without the required shipping details. | Passed locally | ![Shipping validation](documentation/defensive/shipping-validation.png) |
| My Account | Guests cannot access authenticated account pages by entering their URLs directly. | Log out and manually enter the My Account URL. | Passed locally | ![Account access](documentation/defensive/account-access.png) |
| Artist Dashboard | Guests cannot access restricted artist pages directly. | While logged out, manually enter an artist dashboard URL. | Passed locally | ![Guest dashboard access](documentation/defensive/guest-dashboard.png) |
| Artist Dashboard | Registered users without artist permissions cannot access the artist dashboard. | Log in as a regular user and manually enter the dashboard URL. | Passed locally | ![Artist permissions](documentation/defensive/artist-permissions.png) |
| Artist Dashboard - Artwork Management | Regular users cannot access artist-only artwork CRUD operations. | As a regular user, manually enter an Add or Edit Artwork URL. | Passed locally | ![Unauthorized artwork management](documentation/defensive/unauthorized-artwork.png) |
| Artist Dashboard - Collections | Regular users cannot access collection management operations. | As a regular user, manually enter an Add or Edit Collection URL. | Passed locally | ![Unauthorized collection management](documentation/defensive/unauthorized-collection.png) |
| Artist Dashboard - Commissions and Messages | Regular users cannot access incoming commission orders or contact messages. | As a regular user, manually enter the artist commission and message management URLs. | Passed locally | ![Restricted management](documentation/defensive/restricted-management.png) |
| Commission Confirmation | Customers cannot view another customer's paid commission confirmation. | Copy Customer A's paid confirmation URL and open it while logged in as Customer B. | Passed locally | ![Commission ownership](documentation/defensive/commission-ownership.png) |
| Artist Dashboard - Delete Artwork | Artwork deletion requires explicit confirmation. | Open the artwork deletion page, then cancel and verify that the artwork remains. | Passed locally | ![Deletion confirmation](documentation/defensive/delete-confirmation.png) |
| Artist Dashboard - Delete Collection | Collections containing artworks cannot be deleted. | Attempt to delete a collection that still contains artworks. | Passed locally | ![Protected collection deletion](documentation/defensive/protected-collection.png) |
| Artwork and Collections | Invalid artwork and collection URLs are handled without exposing server errors. | Enter a nonexistent artwork or collection URL. | Passed locally | ![Invalid URL](documentation/defensive/invalid-url.png) |
| Commissions - Workflow | Customers cannot bypass required commission ordering stages. | Attempt to access customer details or checkout directly without completing previous stages. | Passed locally — redirected to the Commissions page. | N/A — redirect behaviour cannot be demonstrated meaningfully in a static screenshot. |
| Commissions - Form State Preservation | Previously entered creative preferences are retained when navigating back from customer details. | Complete the creative preferences form, continue to customer details, then click "Back to the Form" and verify all selections and text remain populated. | Passed locally | ![Preserved commission preferences](documentation/defensive/commission-state-preservation.png) |
| Commissions - Checkout | Refreshing checkout does not create duplicate pending orders or lose the order summary. | Refresh the checkout page before payment and inspect the pending order. | Passed locally | N/A — behaviour verified through manual testing and database inspection. |
| Commissions - Payment | A declined Stripe payment does not mark the order as paid. | Attempt payment with Stripe's declined test card and inspect the order status. | Passed locally | ![Declined payment](documentation/defensive/declined-payment.png) |
| Commissions - Confirmation | An unpaid order cannot be accessed through its success URL. | Manually enter the confirmation URL for an unpaid order. | Passed locally | ![Unpaid confirmation](documentation/defensive/unpaid-confirmation.png) |
| Commissions - Completed Payment | Browser navigation after successful payment must not return the customer to an unfinished checkout or initiate another payment. | Complete a test payment, revisit the confirmation page, then use browser Back and Forward navigation. Verify that the existing paid confirmation remains accessible without returning to checkout. | Passed locally — Back returned to the homepage; Forward reopened the existing paid confirmation page. No new payment was initiated.  | N/A — navigation tested manually |


## User Story Testing

| Target | Expectation | Outcome | Screenshot |
| --- | --- | --- | --- |
| As a visitor | I want to understand who Frank Moth are | So I can quickly understand the website's purpose. | ![Homepage](documentation/user-stories/homepage.png) |
| As a visitor | I want intuitive navigation | So I can explore the website easily. | ![Navigation](documentation/user-stories/navigation.png) |
| As a visitor | I want to discover artworks | So I can browse the artists' portfolio. | ![Artworks](documentation/user-stories/artworks.png) |
| As a visitor | I want to view individual artworks | So I can see larger images and artwork details. | ![Artwork detail](documentation/user-stories/artwork-detail.png) |
| As a visitor | I want to explore organised collections | So I can discover related artworks. | ![Collections](documentation/user-stories/art.png) |
| As a visitor | I want to see artwork in real environments | So I can visualise it in different spaces. | ![In Situ](documentation/user-stories/in-situ.png) |
| As a registered user | I want to save favourite artworks | So I can revisit my selections. | ![Favourites](documentation/user-stories/favourites.png) |
| As a visitor | I want to register an account | So I can access member features. | ![Registration](documentation/user-stories/register.png) |
| As a registered user | I want to log in and log out | So I can securely access my account. | ![Login](documentation/user-stories/login.png) |
| As an artist | I want to add new artworks | So I can expand the portfolio. | ![Add artwork](documentation/user-stories/add-artwork.png) |
| As an artist | I want to edit and delete artworks | So I can keep portfolio information accurate. | ![Manage artworks](documentation/user-stories/manage-artworks.png) |
| As an artist | I want to manage artwork collections | So I can organise the portfolio. | ![Manage collections](documentation/user-stories/manage-collections.png) |
| As an artist | I want secure administration | So only authorised artists can manage content. | ![Artist dashboard](documentation/user-stories/manage-artworks.png). See Defensive Programming for access restrictions. |
| As a visitor | I want information about bespoke commissions | So I can understand the available service. | ![Commissions](documentation/user-stories/commissions.png) |
| As a customer | I want to personalise my commission | So I can specify creative preferences or choose Surprise Me. | ![Creative preferences](documentation/user-stories/creative-preferences.png) |
| As a customer | I want to place a commission order | So I can submit my details and review the order. | ![Commission checkout](documentation/user-stories/commission-checkout.png) |
| As a customer | I want secure payment and confirmation | So I know whether my commission was paid for. | ![Payment confirmation](documentation/user-stories/commission-success.png) |
| As a customer | I want to view my commission orders | So I can review previous purchases and payment status. | ![Commission history](documentation/user-stories/commission-history.png) |
| As an artist | I want to manage incoming commissions | So I can review customer requests. | ![Manage commissions](documentation/user-stories/manage-commissions.png) |
| As a visitor | I want to discover the artists' story | So I can learn about their background and creative approach. | ![About](documentation/user-stories/about.png) |
| As a visitor | I want to explore collaborations | So I can discover their professional work. | ![Collaborations](documentation/user-stories/collaborations.png) |
| As a visitor | I want to contact the artists | So I can send an enquiry. | ![Contact confirmation](documentation/user-stories/contact.png) |
| As a visitor | I want to find purchasing options | So I can buy artwork through existing retailers. | ![Where to Buy](documentation/user-stories/where-to-buy.png) |
| As a user | I want a responsive website | So I can use it on different devices. | See [Responsiveness Testing](#responsiveness-testing). |
| As a user | I want an accessible experience | So I can navigate and interact with the website comfortably. | ![Keyboard focus](documentation/user-stories/keyboard-focus.png). See also [Lighthouse Testing](#lighthouse-testing). |
| As an artist | I want to manage incoming contact messages | So I can review enquiries and track their handling status. | ![Messages dashboard](documentation/user-stories/messages.png) |
| As a visitor | I want to connect through social media | So I can follow Frank Moth on other platforms. | ![Social links](documentation/user-stories/social-links.png) |
| As a visitor | I want a striking first impression | So the website immediately communicates the artists' identity. | ![Homepage hero](documentation/user-stories/homepage.png) |
| As an artist | I want to choose collection cover images | So I can control how collections are presented. | ![Collection cover selection](documentation/user-stories/collection-cover.png) |
| As a customer | I want an order confirmation email | So I have a record of my paid commission. | ![Confirmation email](documentation/user-stories/confirmation-email.png) |
| As an artist | I want improved Django Admin artwork management | So I can manage artwork records efficiently. | ![Django Admin artwork management](documentation/user-stories/django-admin-artworks.png) |
| As a website visitor | I want clear error messages when a page cannot be found or accessed | So I can understand the issue and return to the website. | ![Custom error pages](documentation/user-stories/404.png) |


## Automated Testing

I have conducted a series of automated tests on my application.

> [!NOTE]  
> I fully acknowledge and understand that, in a real-world scenario, an extensive set of additional tests would be more comprehensive.

### Python (Unit Testing)

I have used Django's built-in unit testing framework to test the application functionality. In order to run the tests, I ran the following command in the terminal each time:

- `python3 manage.py test name-of-app`

To create the coverage report, I would then run the following commands:

- `pip3 install coverage`
- `pip3 freeze --local > requirements.txt`
- `coverage run --omit="*/site-packages/*,*/migrations/*,*/__init__.py,env.py,.env" manage.py test`
- `coverage report`

To see the HTML version of the reports, and find out whether some pieces of code were missing, I ran the following commands:

- `coverage html`
- `python3 -m http.server`

Below are the results from the full coverage report on my application that I've tested:

![screenshot](documentation/automation/html-coverage.png)


#### Unit Test Issues

**1. Test-Generated Media Files**

**Issue:** While running automated tests involving artwork image uploads, test-generated files were being saved to the project's media directory. Repeated test runs resulted in unnecessary files accumulating alongside the application's media assets.

**Solution:** Django's `@override_settings` decorator was used to configure an isolated `MEDIA_ROOT` for the relevant tests, preventing test uploads from being stored in the application's normal media directory.

**Result:** The tests could run without leaving unwanted image files in the project's media directory.

**2. Difficulties During the Initial TDD Cycle**

**Issue:** During the first Test-Driven Development (TDD) cycle, which focused on enforcing unique artwork titles, difficulties with the test setup and execution made the process more time-consuming than anticipated.

**Resolution:** The testing difficulties were addressed, and the intended red → green → refactor cycle was completed successfully. The experience also helped establish a more manageable approach to automated testing throughout the remainder of the project.

**Result:** Subsequent features were supported by automated tests, while TDD was reserved for selected development scenarios rather than applied to every feature.



## Bugs 


### Fixed Bugs

[![GitHub issue custom search](https://img.shields.io/github/issues-search/angela64711/fourth-milestone-project?query=is%3Aissue%20is%3Aclosed%20label%3Abug&label=Fixed%20Bugs&color=green)](https://www.github.com/angela64711/fourth-milestone-project/issues?q=is%3Aissue+is%3Aclosed+label%3Abug)

I've used [GitHub Issues](https://www.github.com/angela64711/fourth-milestone-project/issues) to track and manage bugs and issues during the development stages of my project.

All previously closed/fixed bugs can be tracked [here](https://www.github.com/angela64711/fourth-milestone-project/issues?q=is%3Aissue+is%3Aclosed+label%3Abug).

![screenshot](documentation/bugs/gh-issues-closed.png)


### Unfixed Bugs

At the time of writing, there are no known unresolved bugs. All six bugs documented during development have been fixed and can be reviewed in the [GitHub Issues tracker](https://github.com/angela64711/fourth-milestone-project/issues?q=is%3Aissue+is%3Aclosed+label%3Abug).

[![GitHub issue custom search](https://img.shields.io/github/issues-search/angela64711/fourth-milestone-project?query=is%3Aissue%2Bis%3Aopen%2Blabel%3Abug&label=Unfixed%20Bugs&color=red)](https://www.github.com/angela64711/fourth-milestone-project/issues?q=is%3Aissue+is%3Aopen+label%3Abug)


 ### Known Limitation — Stripe Webhooks

Stripe webhooks have not been implemented in the current version. Payment confirmation currently relies on the application's checkout flow, which may be interrupted by unexpected browser or network failures. Webhook integration is identified as a future improvement to provide independent payment confirmation and improve order-processing reliability.

> [!IMPORTANT]  
> There are no remaining bugs that I am aware of, though, even after thorough testing, I cannot rule out the possibility.