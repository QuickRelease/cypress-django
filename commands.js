// `cy.login()` will programmatically login using the `USERNAME` and `PASSWORD` environment
// variables defined in `cypress.json` (or with `CYPRESS_` prefix if defined elsewhere)
// Recommended way to use is to put `cy.login()` in `beforeEach`
// If it is necessary to login as a different user, for example to test behaviour for users with
// limited permissions, simply provide the appropriate username and password as arguments
Cypress.Commands.add("login", (username, password) => {
    return cy.request({
        url: '/accounts/login/',
        method: 'GET'
    }).then(() => {
        cy.getCookie('csrftoken').then((csrftoken) => {
            cy.request({
                url: '/accounts/login/',
                method: 'POST',
                form: true,
                followRedirect: false, // No need to retrieve the page after login
                body: {
                    // Use parameters if provided, otherwise use enviroment variables
                    username: username || Cypress.env("USERNAME"),
                    password: password || Cypress.env("PASSWORD"),
                    csrfmiddlewaretoken: csrftoken.value
                }
            }).then(() => {
                // Assert that we now have a `sessionid` to confirm we are logged in
                // Note: current version asserts twice in `should` form:
                //   cy.getCookie('sessionid').should('exist');
                // so we are using the more verbose `expect` form instead
                cy.getCookie("sessionid").then((cookie) => {
                    expect(cookie).to.exist;
                });
            });
        });
    });
});

// `cy.resetDB` will flush the test database and load in a fixture
// If the test will write to the database, `mutable` should be set to `true`,
// otherwise `false` to allow early exit from the script if no fixture loading
// is necessary
Cypress.Commands.add("resetDB", (fixture, mutable) => {
    cy.exec(
        `python -m cypress_db_helper ${mutable ? "--clearcache" : ""} --flush`
            `${Cypress.env("DB_FIXTURE_DIR") || "cypress/db/fixtures"}/${fixture}`
    );
});
