describe("tests for specific event page", () => {
  beforeEach(() => {
    // click on first event listed on home page
    cy.visit("/");
    cy.get(".event-link").first().click();
  });

  it("contains input and text box for betting", () => {
    cy.get("select[id=bet-selection]").should("be.visible");
    cy.get("input[id=bet-amt]").should("be.visible");
    cy.get("button[id=bet-btn").should("be.visible");
  });

  it("does not allow unauthenticated user to place a bet", () => {
    cy.get("input[id=bet-amt]").type(100);
    cy.get("button[id=bet-btn").click();
    cy.get("div[id=bet-details]").should("not.contain", "You bet");
  });

  describe("tests for event page when logged in", () => {
    beforeEach(() => {
      cy.visit("/");
      cy.get("a").contains("Sign In").click();
      cy.get("input[id=email]").type("tristan@tristan.com");
      cy.get("input[id=password]").type("tristan");
      cy.get("input").contains("Login").click();
    });
  });
});
