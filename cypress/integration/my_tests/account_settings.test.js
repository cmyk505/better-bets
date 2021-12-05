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

describe("tests for account settings page", () => {
  beforeEach(() => {
    const randString = generateRandomString(8);

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

  it("shows options to change password and delete account", () => {
    cy.get("a").contains("Change Password");
    cy.get("button").contains("Delete Account");
  });

  it("does not change password if old password is incorrect", () => {
    cy.get("a").contains("Change Password").click();
    cy.get("input[id=old_password]").type("incorrect");
    cy.get("input[id=new_password]").type("tristan1");
    cy.get("input[id=confirm_new_password]").type("tristan1");
    cy.get("input").contains("Submit").click();
    cy.contains("Password change unsuccessful");
  });

  it("lets you change your password if given correct input", () => {
    cy.get("a").contains("Change Password").click();
    cy.get("input[id=old_password]").type("password");
    cy.get("input[id=new_password]").type("tristan1");
    cy.get("input[id=confirm_new_password]").type("tristan1");
    cy.get("input").contains("Submit").click();
  });

  // it("lets you delete your account", () => {
  //   cy.get("button").contains("Delete Account").click();
  //   // click again to confirm deletion on modal

  //   const el = cy.get("#modal-confirm");
  //   el.click();
  //   // link should change indicating redirect and successful deletion
  //   cy.on("url:changed", () => {
  //     cy.contains("Account deleted");
  //   });
  // });

  it("displays bet history", () => {
    cy.contains("Better Bets").click();
    cy.get("a").contains("vs").first().click();
    cy.get("input[id=bet-amt]").type(100);
    cy.get("button").contains("bet").click();

    cy.visit("/account");
    cy.contains("My Bet History");
  });
});
