function generateRandomString(length) {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

describe("home page tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("loads event data", () => {
    cy.get(".event-link").should("be.visible");

    //10 most recent events should be loaded
    expect(cy.get(".event-link").should("have.length", 10));
  });

  it("shows sign in and register links by default", () => {
    cy.get("a").contains("Sign In");
    cy.get("a").contains("Register");
  });

  it("opens an event page if clicked on", () => {
    cy.get(".event-link").first().click();
    cy.on("url:changed", newUrl => {
      expect(newUrl).to.contain("/event");
    });
  });

  describe("home page logged in", () => {
    beforeEach(() => {
      const randString = generateRandomString(10);

      cy.visit("http://host.docker.internal:5000/register");

      cy.get("input[id=first_name]").type("First");
      cy.get("input[id=last_name]").type("Last");
      cy.get("input[id=email]").type(`${randString}@gmail.com`);
      cy.get("input[id=password]").type("password");
      cy.get("input[id=confirm_password]").type("password");
      cy.get("input[id=submit]").click();

      cy.get("input[id=email]").type(`${randString}@gmail.com`);
      cy.get("input[id=password]").type("password");
      cy.get("input").contains("Login").click();
      cy.get("a").contains("Account").click();
      Cypress.on("uncaught:exception", (err, runnable) => {
        // returning false here prevents Cypress from
        // failing the test
        return false;
      });
    });
    it("shows different content when logged in", () => {
      cy.get("a").contains("Login").should("not.exist");
      cy.get("a").contains("Register").should("not.exist");
      cy.get("a").contains("Logout");
    });
    it("works to log out", () => {
      cy.get("a").contains("Logout").click();
    });

    it("shows button to reload balance", () => {
      cy.visit("/");
      cy.get("button").contains("Reload Balance").should("exist");
    });
    it("outputs text when user clicks to reload balance", () => {
      cy.visit("/");
      cy.get("button").contains("Reload Balance").click();
      cy.get("div").contains("balance");
    });
  });
});
