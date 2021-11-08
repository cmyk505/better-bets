describe("home page tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("loads event data", () => {
    cy.get(".event-card").should("be.visible");

    //10 most recent events should be loaded
    expect(cy.get(".event-card").should("have.length", 10));
  });

  it("shows sign in and register links by default", () => {
    cy.get("a").contains("Sign In");
    cy.get("a").contains("Register");
  });

  it("opens an event page if clicked on", () => {
    cy.get(".event-card").find("a").first().click();
    cy.on("url:changed", newUrl => {
      expect(newUrl).to.contain("/event");
    });
  });

  describe("home page logged in", () => {
    beforeEach(() => {
      //hard coding working credentials based on what's in my test database
      cy.get("a").contains("Sign In").click();
      cy.get("input[id=email]").type("tristan@tristan.com");
      cy.get("input[id=password]").type("tristan");
      cy.get("input").contains("Login").click();
    });
    it("shows different content when logged in", () => {
      cy.get("a").contains("Sign In").should("not.exist");
      cy.get("a").contains("Register").should("not.exist");
      cy.get("a").contains("Log out");
    });
  });
});
