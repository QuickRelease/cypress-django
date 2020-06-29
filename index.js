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


Cypress.Commands.add("resetDB", (fixture, mutable) => {
    cy.exec(`python -m cypress_db_helper ${mutable ? "--clearcache" : ""} --flush cypress/db/fixtures/${fixture}`);
});
