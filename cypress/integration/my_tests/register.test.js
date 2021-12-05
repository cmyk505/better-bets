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

describe("test user flow for registration", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("a").contains("Register").click();
  });

  it("should allow user to sign up if they enter valid data", () => {
    cy.get("input[id=first_name]").type("First");
    cy.get("input[id=last_name]").type("Last");
    cy.get("input[id=email]").type(`${generateRandomString(8)}@gmail.com`);
    cy.get("input[id=password]").type("password");
    cy.get("input[id=confirm_password]").type("password");
    cy.get("input[id=submit]").click();
    cy.on("url:changed", newUrl => {
      expect(newUrl).to.equal("http://host.docker.internal:5000/login");
    });
  });

  it("should not allow user to sign up if passwords do not match", () => {
    cy.get("input[id=first_name]").type("First");
    cy.get("input[id=last_name]").type("Last");
    cy.get("input[id=email]").type(`${generateRandomString(8)}@gmail.com`);
    cy.get("input[id=password]").type("password");
    cy.get("input[id=confirm_password]").type("password2");
    cy.get("input[id=submit]").click();
    cy.contains("must be equal");
  });
});
